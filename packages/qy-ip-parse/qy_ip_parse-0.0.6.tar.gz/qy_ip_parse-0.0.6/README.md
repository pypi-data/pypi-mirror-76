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

from qy_ip_parse import IP_IP

IP_IP.init(host='127.0.0.1', port=6379, pwd=None, ex=10)


if __name__ == '__main__':
    s = time.time()
    ip = IP_IP.parse('111.12.33.11')
    print(ip.country_name, ip.region_name, ip.city_name, ip.isp_domain)
    print(time.time() - s)
    time.sleep(5)
    s = time.time()
    ip = IP_IP.parse('111.12.32.11')
    print(ip.country_name, ip.region_name, ip.city_name, ip.isp_domain)
    print(time.time() - s)
    time.sleep(6)
    s = time.time()
    ip = IP_IP.parse('111.12.35.11')
    print(ip.country_name, ip.region_name, ip.city_name, ip.isp_domain)
    print(time.time() - s)
    time.sleep(5)
    s = time.time()
    ip = IP_IP.parse('111.12.55.11')
    print(ip.country_name, ip.region_name, ip.city_name, ip.isp_domain)
    print(time.time() - s)

```