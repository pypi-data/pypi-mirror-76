from epwechat.access.token import Token
import requests
import json


class SendMsg:
    SEND_MSG_BASE_URL = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token="
    HEADERS = {'Content-Type': 'application/json'}

    def __init__(self, corpid: str, corpsecret: str):
        self.corpid = corpid
        self.corpsecret = corpsecret
        self.rds = Token('127.0.0.1', 6379)

    def send_text(self, touser: int, content: str, msgtype='text', agentid=0):
        """
         :param touser:指定接收消息的成员，成员ID列表（多个接收者用‘|’分隔，最多支持1000个）。特殊情况：指定为”@all”，则向该企业应用的全部成员发送
        :param agentid:企业应用的id
        :param content:消息内容，最长不超过2048个字节，超过将截断（支持id转译）
        :param msgtype:消息类型(text:文本消息)
        :return:
        """
        token = self.rds.read_cach_token('token')
        if not token:
            token = Token.get_token(self.corpid, self.corpsecret)
            self.rds.writer_cach_token('token', token)
        data = {'touser': touser, 'agentid': agentid, 'text': {'content': content}, 'msgtype': msgtype}
        errcode = requests.post(url=self.SEND_MSG_BASE_URL + token, data=json.dumps(data, ensure_ascii=False).encode('utf-8'), headers=self.HEADERS).json().get('errcode')
        return errcode
