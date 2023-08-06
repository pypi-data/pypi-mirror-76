import os
import time

import ipdb
import oss2
import requests


class IpIpConst(dict):

    def init(self, db_name, oss_config):
        """

        :param db_name: string
        :param oss_config: {"access_key": "", "access_secret": "", "endpoint": "", "bucket_name": "", "oss_ip_db_object": ""}
        :return:
        """
        self.DB_NAME = db_name
        self.OSS_CONFIG = oss_config
        self.EXPIRE = 1
        self.DB = ipdb.City(self.DB_NAME) if os.path.exists(self.DB_NAME) else update_db_cache()

    def __getattr__(self, item):
        return self[item]

    def __setattr__(self, key, value):
        self[key] = value


IpIp = IpIpConst(
    DB_NAME='ip.ipdb',
    DB=None,
    EXPIRE=time.time(),
    OSS_CONFIG=None,
    DB_URL=None,
)


class Oss2(object):

    def __init__(self, access_key, access_secret, endpoint, bucket_name):
        self.access_key = access_key
        self.access_secret = access_secret
        self.endpoint = endpoint
        self.bucket_name = bucket_name
        self.auth = oss2.Auth(self.access_key, self.access_secret)
        self.bucket = oss2.Bucket(self.auth, self.endpoint, self.bucket_name)

    def upload(self, object_name, content):
        result = self.bucket.put_object(object_name, content)
        if result.status == 200:
            return True, result
        else:
            return False, "上传失败"

    def download(self, object_name, filename):
        return self.bucket.get_object_to_file(object_name, filename)


def requests_download(url, filename):
    r = requests.get(url, stream=True)
    with open(filename, "wb") as fd:
        for chunk in r.iter_content(chunk_size=10240):
            if chunk:
                fd.write(chunk)
    return True


def update_db_cache():
    # 一天内不更新
    if (time.time() - IpIp.EXPIRE) < 60 * 60 * 24:
        return IpIp.DB
    # 超过一天
    expire = IpIp.pop('EXPIRE', None)
    if expire:
        # 获取到锁的更新
        try:
            if IpIp.OSS_CONFIG:
                oss_client = Oss2(
                    access_key=IpIp.OSS_CONFIG.get('access_key'),
                    access_secret=IpIp.OSS_CONFIG.get('access_secret'),
                    endpoint=IpIp.OSS_CONFIG.get('endpoint'),
                    bucket_name=IpIp.OSS_CONFIG.get('bucket_name'),
                )
                oss_client.download(IpIp.OSS_CONFIG.get('oss_ip_db_object'), IpIp.DB_NAME)
            else:
                requests_download(IpIp.DB_URL, IpIp.DB_NAME)
            IpIp.DB = ipdb.City(IpIp.DB_NAME)
            # 更新成功,更新锁状态
            IpIp.EXPIRE = time.time()
        except Exception as e:
            # 如果更新失败, 还原更新前状态
            IpIp.EXPIRE = expire
    else:
        # 没有获取锁的不进行任何操作
        pass
    return IpIp.DB


class IpParse(object):

    def __init__(self, ip=None):
        self.ip = ip

    def parse(self):
        update_db_cache()
        ip_info = IpIp.DB.find_info(self.ip, "CN")
        country_name = ip_info.country_name
        region_name = ip_info.region_name
        city_name = ip_info.city_name
        isp_domain = ip_info.isp_domain
        return country_name, region_name, city_name, isp_domain
