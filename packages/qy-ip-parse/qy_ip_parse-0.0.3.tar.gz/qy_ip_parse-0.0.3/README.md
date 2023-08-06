# qy ip parse

qy ip parse.


## Installing

Install and update using `pip`:

```
$ pip install -U qy-ip-parse
```


## A Simple Example

```python
import time

from qy_ip_parse import IpIp
from qy_ip_parse import IpParse

IpIp.init(
    db_name='ip.ipdb',
    oss_config={
        "access_key": "", "access_secret": "",
        "endpoint": "", "bucket_name": "",
        "oss_ip_db_object": ''
    }
)

start = time.time()
a = IpParse('IP地址')
print(a.parse())
print(time.time()-start)
print(a.parse())
print(time.time() - start)
```