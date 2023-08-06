import requests
import json
from ..cache.token_cache import RedisInstance


class Token:
    def __init__(self, host: str, port: int):
        self.redis_instance = RedisInstance(host, port).get_instance()

    def writer_cach_token(self, key_name: str, access_token: str, ex=7000):
        self.redis_instance.set(key_name, access_token, ex=ex)

    def read_cach_token(self, key_name: str):
        return self.redis_instance.get(key_name)

    @staticmethod
    def get_token(corpid: str, corpsecret: str) -> str:
        """
        :param corpid:企业ID
        :param corpsecret:应用的凭证密钥
        :return:
        """
        get_token_url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corpid}&corpsecret={corpsecret}"
        ret_token = requests.get(get_token_url).text
        token = json.loads(ret_token).get('access_token')
        return token
