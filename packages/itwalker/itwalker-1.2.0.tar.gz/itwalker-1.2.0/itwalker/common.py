import urllib3
import datetime
import pytz
import os
import yaml
import hashlib


class CommonLib:
    def MD5(self, str):
        # ����md5����
        m = hashlib.md5()
        b = str.encode(encoding='utf-8')
        m.update(b)
        str_md5 = m.hexdigest()
        return str_md5

    def deepClone(self, dictValue):
        if isinstance(dictValue, list) or isinstance(dictValue, set):
            return [self.deepClone(v) if type(v).__name__ in ["list", "set", "tuple", "dict"] else v for v in dictValue]
        elif isinstance(dictValue, dict):
            return {k: self.deepClone(v) if type(v).__name__ in ["list", "set", "tuple", "dict"] else v for k, v in
                    dictValue.items()}
        elif isinstance(dictValue, tuple):
            return (self.deepClone(v) if type(v).__name__ in ["list", "set", "tuple", "dict"] else v for k, v in
                    dictValue)
        else:
            raise Exception(
                "type of value must is in [list, set, tuple, dict] ")

    def getRemoteStream(self, url):
        http = urllib3.PoolManager()
        r = http.request('GET', url)
        if r.status == 200:
            return r.data
        else:
            return None

    def getNowTime(self):
        tz = pytz.timezone('Asia/Shanghai')
        dt = datetime.datetime.now(tz)
        return dt.strftime("%Y-%m-%d %H:%M:%S")


class StaticVariable:
    def __init__(self):
        self.basePath = os.path.join(os.getcwd(), 'data')

    def SaveParam(self, result, name):
        filename = os.path.join(self.basePath, f'{name}.yaml')
        with open(filename, 'w', encoding='utf-8') as yaml_file:
            yaml.safe_dump(result, yaml_file, default_flow_style=False,
                           encoding='utf-8', allow_unicode=True)

    def getParam(self, name):
        filename = os.path.join(self.basePath, f'{name}.yaml')
        with open(filename, 'r', encoding='utf-8') as f:
            file_data = f.read()
            data = yaml.safe_load(file_data)
            return True, data
