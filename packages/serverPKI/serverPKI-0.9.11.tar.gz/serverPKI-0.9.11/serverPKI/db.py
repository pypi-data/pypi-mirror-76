# -*- coding: utf-8 -*-

"""
Copyright (C) 2015-2020  Axel Rau <axel.rau@chaos1.de>

This file is part of serverPKI.

serverPKI is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Foobar is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with serverPKI.  If not, see <http://www.gnu.org/licenses/>.
"""

# database primitives module


# --------------- imported modules --------------

import sys

##import postgresql as pg
from postgresql import open as pg_open
from postgresql import alock
from postgresql import exceptions

# --------------- local imports --------------
from serverPKI.utils import DBAccount, sld, sli, sln, sle

# --------------- db classes --------------
class DbConnection(object):
    """
    Connection handler of DB session with PostgreSQL server
    """

    def __init__(self, service):
        """
        Create a DbConnection instance
    
        @param service:     service name
        @type service:      string
        @rtype:             DbConnection instance
        @exceptions:        None, but does a exit(1) if connection can't be
                            established
        """

        self.lock = None
        self.conn = None
        self.sslcrtfile = None
        try:
            self.host = DBAccount.dbHost
            self.port = str(DBAccount.dbPort)
            self.user = DBAccount.dbUser
            self.dba_user = DBAccount.dbDbaUser
            self.ssl_required = DBAccount.dbSslRequired
            self.database = DBAccount.dbDatabase
            self.search_path = DBAccount.dbSearchPath

            ssl_option = (', sslmode=' + '"require"') if self.ssl_required else ''

            self.dsn = str('host=' + self.host + ', port=' + self.port +
                           ', user=' + self.user + ', database=' + self.database + ssl_option)

            if DBAccount.dbCert:
                self.sslcrtfile = DBAccount.dbCert
                self.sslkeyfile = DBAccount.dbCertKey
                self.dsn = self.dsn + str(', sslcrtfile={}, sslkeyfile={}'.format(self.sslcrtfile, self.sslkeyfile))
        except:
            sle('Config error: Missing or wrong keyword in DBAccount.\n' +
                'Must be dbHost, dbPort, dbUser, , dbDbaUser, dbDatabase, dbSslrequired and dbSearchPath.')
            raise(BaseException())

    def open(self):
        """
        Open the connection to the DB server
    
        @rtype:             DbConnection instance with state 'opened'
        @exceptions:        None, but does a exit(1) if connection can't be
                            established
        """
        if not self.conn:
            try:
                if self.ssl_required:
                    if self.sslcrtfile:
                        self.conn = pg_open(host=self.host, port=self.port, user=self.user, database=self.database,
                                            sslmode="require", sslcrtfile=self.sslcrtfile, sslkeyfile=self.sslkeyfile)
                    else:
                        self.conn = pg_open(host=self.host, port=self.port, user=self.user, database=self.database,
                                            sslmode="require")
                else:
                    self.conn = pg_open(host=self.host, port=self.port, user=self.user, database=self.database)

                self.conn.settings['search_path'] = self.search_path

            except:
                sle('Unable to connect to database %s' % (self.dsn))
                sys.exit(1)

        return self.conn

    def acquire_lock(self, locking_code):
        """
        Try to obtain an advisory lock in the DB, but do not block if lock
        can't be acquired.
    
        @param locking_code:    name of the lock
        @type locking_code:     string
        @rtype:                 True if lock acquired, False otherwise
        """
        if not self.conn:
            self.open()
        self.lock = alock.ExclusiveLock(self.conn, (0, locking_code))
        if not self.lock.acquire(blocking=False):
            return False
        return True

    def unlock(self):
        """
        Release an advisary lock, if one there.
    
        @rtype:                 None
        """
        self.lock.release()


class DBStoreException(Exception):
    """
    Generic exception for INSERT or UPDATE opertions
    """
    pass
