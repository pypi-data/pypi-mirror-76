=========
serverPKI
=========

.. image:: https://img.shields.io/pypi/v/serverpki.svg
    :target: https://pypi.org/project/serverPKI/
    :alt: Latest Version

.. image:: https://readthedocs.org/projects/serverpki/badge/?version=latest
    :target: https://serverpki.readthedocs.io/en/latest/
    :alt: Latest Docs
	
	
:serverPKI:   Python PKI for internet server infrastructure
:Copyright:   Copyright (c) 2015-2020   Axel Rau axel.rau@chaos1.de
:License:     `GPLv3 <http://www.gnu.org/licenses/>`_
:Homepage:    https://github.com/mc3/serverPKI
:Documentation: https://serverpki.readthedocs.io


What
----

serverPKI is a tool to issue, renew and distribute SSL certificates for internet
servers. Distribution to target hosts and reloading of server configuration
is done via ssh/sftp. Configuration and cert/key data is stored in a relational
database.

serverPKI includes support for

- local CA
- LetsEncrypt CA (supports only acme v2 api, see https://letsencrypt.org/docs)
- FreeBSD service jails via ssh access to host
- publishing of DANE RR in DNS, using BIND 9 and TLSA key rollover (see RFC 6698)
- controlling DNS zone info for LetsEncrypt challenges und TLSA RR via dynamic
  DNS updates (recommended) or via zone files.
- unattended operation via cronjob
- extensive logging
- alerting via mail
 


Prerequisites
-------------

- PostgreSQL 12+ server

  - The contrib utilities from the PostgreSQL distribution are required
    (serverPKI needs the citext extension for case insensitive indexes)
  - a DB account with super user privileges [dba] or assistance of a DB admin
    (serverPKI uses a dedicated DB user [pki_op] and a dedicated DB)
  - authentication record in pg_hba.conf to allow access of pki_op from local
    host (client cert authentication recommended)
    
- PostgreSQL 12+ client installation on local host
- bind 9 DNS server (9.16+ should be used)

  - If DNS is handled via zone files,

    - serverPKI must be run on the master (hidden primary) DNS server.

    - signed Zones being maintained by serverPKI must be run in auto-dnssec
      maintain + inline-signing operation mode.

    - Zone files must be writable by serverPKI process to allow publishing of
      acme_challenges and TLSA resource records for DANE

- Python 3.7+ must be installed (tested with Python 3.8.3)
- Running serverPKI in a Python virtual environment is recommended for ease of
  upgrading. The author uses `virtualenvwrapper`.


Sponsored
---------

This project is being developed with the powerful Python IDE PyCharm, which is
particularly useful during remote debugging sessions.
A professional license has been granted by JetBrains, https://www.jetbrains.com/.
