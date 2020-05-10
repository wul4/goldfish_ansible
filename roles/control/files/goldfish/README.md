## Requirements

* Docker (tested: Docker version 19.03.5-ce, build 633a0ea838)
* Docker-compose (tested: docker-compose version 1.25.0)
* Docker-compose is defaults to fixed subnet 192.168.245.0/24

## How to run

Use `make compose-start-clean` to build and start development instance with
Docker-compose.

## Stuff to look for

1. See docker-compose.yml for `DYNACONF_` environment variable, then find the 
   variable in the actual API class and see how it is loaded via shared config
   instance.

2. See `example_api_app/example_api_app/specs/hello_world_api.yml` how to use
   OpenAPI 3.0.0 and map API methods to actual Python modules and function.

3. Look at `example_api_app/uwsgi.ini` and
   `example_api_app/example_api_app/services/api.py` to see where the actual
   loading of the application begins and where the core Connexion and Flask
   instances are created (other places can then import those from there).

4. After starting the application, browse to
   http://192.168.245.100/api/v1/hello/ui/ to see complimentary Swagger UI based
   on your OpenAPI spec!

## Documentation

- https://connexion.readthedocs.io/en/latest/
- https://dynaconf.readthedocs.io/en/latest/
- https://github.com/tiangolo/uwsgi-nginx-flask-docker

## Tools

You can use various tools to design OpenAPI v3 specifications. One
multi-platform GUI option to do this would be https://stoplight.io/studio/

## Docker image security

All systems and images have CVEs present. Using lightweight Alpine image
minimizes the amount of extra libraries and operating system software to lift
around. As a comparison this Alpine based Example API has ~800 MiB smaller
footprint compared to the same image with Debian 9.11 base (226 MiB vs. ~1 GiB).

The Debian 9.11 based image has over 3700 CVEs present
(scanned with [Trivy](https://github.com/aquasecurity/trivy)).
Bellow is the same scan for the final Alpine based image
(which this repository uses):

```
SCAN TIME: Tue 26 Nov 2019 12:40:46 PM EET

$  trivy example-python-rest-api_api
2019-11-26T12:34:22.738+0200	INFO	Reopening vulnerability DB
2019-11-26T12:34:22.738+0200	WARN	You should avoid using the :latest tag as it is cached. You need to specify '--clear-cache' option when :latest image is changed
2019-11-26T12:34:25.819+0200	INFO	Detecting Alpine vulnerabilities...

example-python-rest-api_api (alpine 3.8.4)
==========================================
Total: 11 (UNKNOWN: 0, LOW: 1, MEDIUM: 6, HIGH: 4, CRITICAL: 0)

+-----------+------------------+----------+-------------------+---------------+--------------------------------+
|  LIBRARY  | VULNERABILITY ID | SEVERITY | INSTALLED VERSION | FIXED VERSION |             TITLE              |
+-----------+------------------+----------+-------------------+---------------+--------------------------------+
| bzip2     | CVE-2019-12900   | HIGH     | 1.0.6-r6          | 1.0.6-r7      | bzip2: out-of-bounds write in  |
|           |                  |          |                   |               | function BZ2_decompress        |
+-----------+------------------+----------+-------------------+---------------+--------------------------------+
| e2fsprogs | CVE-2019-5094    | MEDIUM   | 1.44.2-r0         | 1.44.2-r1     | e2fsprogs: crafted             |
|           |                  |          |                   |               | ext4 partition leads to        |
|           |                  |          |                   |               | out-of-bounds write            |
+-----------+------------------+----------+-------------------+---------------+--------------------------------+
| expat     | CVE-2018-20843   | HIGH     | 2.2.5-r0          | 2.2.7-r0      | expat: large number of colons  |
|           |                  |          |                   |               | in input makes parser consume  |
|           |                  |          |                   |               | high amount...                 |
+           +------------------+----------+                   +---------------+--------------------------------+
|           | CVE-2019-15903   | MEDIUM   |                   | 2.2.7-r1      | expat: heap-based buffer       |
|           |                  |          |                   |               | over-read via crafted XML      |
|           |                  |          |                   |               | input                          |
+-----------+------------------+----------+-------------------+---------------+--------------------------------+
| libtasn1  | CVE-2018-1000654 | HIGH     | 4.13-r0           | 4.14-r0       | libtasn1: Infinite loop in     |
|           |                  |          |                   |               | _asn1_expand_object_id(ptree)  |
|           |                  |          |                   |               | leads to memory exhaustion     |
+-----------+------------------+----------+-------------------+---------------+--------------------------------+
| libxslt   | CVE-2019-18197   | MEDIUM   | 1.1.33-r1         | 1.1.33-r2     | libxslt: use after free in     |
|           |                  |          |                   |               | xsltCopyText in transform.c    |
|           |                  |          |                   |               | could lead to information...   |
+-----------+------------------+          +-------------------+---------------+--------------------------------+
| openldap  | CVE-2019-13565   |          | 2.4.46-r0         | 2.4.48-r0     | openldap: ACL restrictions     |
|           |                  |          |                   |               | bypass due to sasl_ssf value   |
|           |                  |          |                   |               | being set permanently          |
+           +------------------+----------+                   +               +--------------------------------+
|           | CVE-2019-13057   | LOW      |                   |               | openldap: Information          |
|           |                  |          |                   |               | disclosure issue in slapd      |
|           |                  |          |                   |               | component                      |
+-----------+------------------+----------+-------------------+---------------+--------------------------------+
| python3   | CVE-2019-16056   | MEDIUM   | 3.6.8-r0          | 3.6.8-r1      | python: email.utils.parseaddr  |
|           |                  |          |                   |               | wrongly parses email addresses |
+           +------------------+          +                   +---------------+--------------------------------+
|           | CVE-2019-16935   |          |                   | 3.6.9-r1      | python: XSS vulnerability      |
|           |                  |          |                   |               | in the documentation XML-RPC   |
|           |                  |          |                   |               | server in server_title field   |
+-----------+------------------+----------+-------------------+---------------+--------------------------------+
| sqlite    | CVE-2019-8457    | HIGH     | 3.25.3-r0         | 3.25.3-r1     | sqlite3: heap out-of-bound     |
|           |                  |          |                   |               | read in function rtreenode()   |
+-----------+------------------+----------+-------------------+---------------+--------------------------------+
```

As you can see using small and lightweight Alpine based images makes it easier
to scan and deal with CVEs really relevant to you. No one will ever browse
through the over 3700 CVEs found in the Debian 9.11 based image and actually
determine whether they might be relevant or not in the context of your
application.

Dealing with backports and numerous vendor provided CVE databases is just not
trivial enough in container ecosystems. Using simple scanners (like Trivy) as
part of your CI/CD process is the only way to ensure you know what CVEs you are 
shipping.
