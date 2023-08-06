cloudgenix_tenant_acl
------

Scripts to Download, Upload, and Optimize a CloudGenix Tenant Access List.

pull_acl[.py]: Download a tenant ACL list.
```text
usage: pull_acl.py [-h] --output OUTPUT [--no-client-login] [--controller CONTROLLER] [--email EMAIL] [--password PASSWORD] [--insecure] [--noregion]
                   [--sdkdebug SDKDEBUG]
```

do_acl[.py]: Upload and activate a tenant ACL list.
```text
usage: do_acl.py [-h] --input INPUT [--archive ARCHIVE] [--no-client-login] [--controller CONTROLLER] [--email EMAIL] [--password PASSWORD] [--insecure] [--noregion]
                 [--sdkdebug SDKDEBUG]
```

optimize_acl[.py]: Optimize a tenant ACL list with a lossy superneting function.
```text
usage: optimize_acl.py [-h] --input INPUT --output OUTPUT [--match-quality MATCH_QUALITY] [--ip-mismatch-limit IP_MISMATCH_LIMIT]
```
