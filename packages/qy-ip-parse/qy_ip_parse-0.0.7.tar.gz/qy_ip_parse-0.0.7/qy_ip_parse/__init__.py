import time
import redis
import json
import sys
try:
    from io import BytesIO
except:
    import BytesIO
from ipdb.city import City
from ipdb.database import MetaData
from ipdb.database import Reader
from ipdb.exceptions import DatabaseError
from ipdb.util import bytes2long


class MyReader(Reader):

    def __init__(self, name):
        self._v4offset = 0
        self._v6offsetCache = {}

        if isinstance(name, BytesIO):
            file = name
        else:
            file = open(name, "rb")
        self.data = file.read()
        self._file_size = len(self.data)
        file.close()
        meta_length = bytes2long(self.data[0], self.data[1], self.data[2], self.data[3])
        if sys.version_info < (3, 0):
            meta = json.loads(str(self.data[4:meta_length + 4]))
        else:
            meta = json.loads(str(self.data[4:meta_length + 4], 'utf-8'))

        self._meta = MetaData(**meta)
        if len(self._meta.languages) == 0 or len(self._meta.fields) == 0:
            raise DatabaseError("database meta error")
        if self._file_size != (4 + meta_length + self._meta.total_size):
            raise DatabaseError("database size error")

        self.data = self.data[4 + meta_length:]


class MyCity(City):

    def __init__(self, name):
        self.db = MyReader(name)


class IpIpSingleton(object):

    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 6379
        self.pwd = None
        self.old_db = None
        self.ex = 60 * 10
        self.expire = time.time() + self.ex

    def init(self, host='127.0.0.1', port=6379, pwd=None, ex=60*10):
        self.host = host
        self.port = port
        self.pwd = pwd
        self.ex = ex

    @property
    def _db(self):
        if time.time() > self.expire or self.old_db is None:
            r = redis.Redis(self.host, port=self.port, password=self.pwd)
            self.old_db = MyCity(BytesIO(r.get('ipdb_key')))
            self.expire = time.time() + self.ex
            return self.old_db
        else:
            return self.old_db

    def parse(self, ip_address):
        ip_info = self._db.find_info(ip_address, "CN")
        country_name = ip_info.country_name
        region_name = ip_info.region_name
        city_name = ip_info.city_name
        isp_domain = ip_info.isp_domain
        result = IpResult(country_name, region_name, city_name, isp_domain)
        return result


class IpResult(object):

    def __init__(self, country_name, region_name, city_name, isp_domain):
        self.country_name = country_name
        self.city_name = city_name
        self.region_name = region_name
        self.isp_domain = isp_domain


IP_IP = IpIpSingleton()

