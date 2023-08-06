import time
import ssl

import pathlib
import websocket
import datetime
import hashlib
import base64
import hmac
import json
from abc import abstractmethod
from urllib.parse import urlencode
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime
import _thread as thread

STATUS_FIRST_FRAME = 0  # 第一帧的标识
STATUS_CONTINUE_FRAME = 1  # 中间帧标识
STATUS_LAST_FRAME = 2  # 最后一帧的标识


class WebSocketApp(object):
    def __init__(self, app_id, api_key, api_secret):
        self.APPID = app_id
        self.APIKey = api_key
        self.APISecret = api_secret

    @abstractmethod
    def create_url(self):
        """
        创建url
        :return:
        """
        pass

    @abstractmethod
    def send(self, info: str):
        """
        发送信息
        :param info:发送的信息
        :return:
        """
        pass

    @abstractmethod
    def get_result(self):
        """获取结果"""

    @staticmethod
    @abstractmethod
    def on_message(ws, message):
        """收到websocket消息的处理"""
        pass

    @staticmethod
    def on_error(ws, error):
        """收到websocket错误的处理"""
        pass

    @staticmethod
    def on_close(ws):
        """收到websocket关闭的处理"""
        pass

    @staticmethod
    @abstractmethod
    def on_open(ws):
        """收到websocket连接建立的处理"""
        pass


class AudioWebSocketApp(WebSocketApp):
    """将语音转换为文本"""

    def __init__(self, app_id, api_key, api_secret):
        super(AudioWebSocketApp, self).__init__(app_id, api_key, api_secret)
        self.ws = websocket.WebSocketApp(None, on_message=self.on_message, on_error=self.on_error,
                                         on_close=self.on_close)
        self.ws.on_open = self.on_open
        # 公共参数(common)
        self.ws.CommonArgs = {"app_id": self.APPID}
        # 业务参数(business)，更多个性化参数可在官网查看
        self.ws.BusinessArgs = {"domain": "iat", "language": "zh_cn", "accent": "mandarin", "vinfo": 1,
                                "vad_eos": 10000}

        self.infos = []
        self.ws.infos = self.infos

    def create_url(self):
        url = 'wss://ws-api.xfyun.cn/v2/iat'
        # 生成RFC1123格式的时间戳
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        # 拼接字符串
        signature_origin = "host: " + "ws-api.xfyun.cn" + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + "/v2/iat " + "HTTP/1.1"
        # 进行hmac-sha256进行加密
        signature_sha = hmac.new(self.APISecret.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()
        signature_sha = base64.b64encode(signature_sha).decode(encoding='utf-8')

        authorization_origin = "api_key=\"%s\", algorithm=\"%s\", headers=\"%s\", signature=\"%s\"" % (
            self.APIKey, "hmac-sha256", "host date request-line", signature_sha)
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
        # 将请求的鉴权参数组合为字典
        v = {
            "authorization": authorization,
            "date": date,
            "host": "ws-api.xfyun.cn"
        }
        # 拼接鉴权参数，生成url
        url = url + '?' + urlencode(v)
        return url

    def send(self, audio_file):
        websocket.enableTrace(False)
        url = self.create_url()
        self.ws.url = url
        self.ws.audio_file = audio_file

        self.ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

    # 收到websocket消息的处理
    @staticmethod
    def on_message(ws, message):
        try:
            code = json.loads(message)["code"]
            sid = json.loads(message)["sid"]
            if code != 0:
                err_msg = json.loads(message)["message"]
                print("sid:%s call error:%s code is:%s" % (sid, err_msg, code))

            else:
                data = json.loads(message)["data"]["result"]["ws"]
                result = ""
                for i in data:
                    for w in i["cw"]:
                        result += w["w"]
                ws.infos.append(result)
        except Exception as e:
            print("receive msg,but parse exception:", e)

    def get_result(self):
        return ''.join(self.infos)

    @staticmethod
    def on_open(ws):
        def run(*args):
            frame_size = 8000  # 每一帧的音频大小
            interval = 0.04  # 发送音频间隔(单位:s)
            status = STATUS_FIRST_FRAME  # 音频的状态信息，标识音频是第一帧，还是中间帧、最后一帧

            with open(ws.audio_file, "rb") as fp:
                while True:
                    buf = fp.read(frame_size)
                    # 文件结束
                    if not buf:
                        status = STATUS_LAST_FRAME
                    # 第一帧处理
                    # 发送第一帧音频，带business 参数
                    # appid 必须带上，只需第一帧发送
                    if status == STATUS_FIRST_FRAME:

                        d = {"common": ws.CommonArgs,
                             "business": ws.BusinessArgs,
                             "data": {"status": 0, "format": "audio/L16;rate=16000",
                                      "audio": str(base64.b64encode(buf), 'utf-8'),
                                      "encoding": "raw"}}
                        d = json.dumps(d)
                        ws.send(d)
                        status = STATUS_CONTINUE_FRAME
                    # 中间帧处理
                    elif status == STATUS_CONTINUE_FRAME:
                        d = {"data": {"status": 1, "format": "audio/L16;rate=16000",
                                      "audio": str(base64.b64encode(buf), 'utf-8'),
                                      "encoding": "raw"}}
                        ws.send(json.dumps(d))
                    # 最后一帧处理
                    elif status == STATUS_LAST_FRAME:
                        d = {"data": {"status": 2, "format": "audio/L16;rate=16000",
                                      "audio": str(base64.b64encode(buf), 'utf-8'),
                                      "encoding": "raw"}}
                        ws.send(json.dumps(d))
                        time.sleep(1)
                        break
                    # 模拟音频采样间隔
                    time.sleep(interval)
            ws.close()

        thread.start_new_thread(run, ())


class TextWebSocketApp(WebSocketApp):
    """将文本转换为语音"""

    def __init__(self, app_id, api_key, api_secret):
        super(TextWebSocketApp, self).__init__(app_id, api_key, api_secret)
        self.ws = websocket.WebSocketApp(None, on_message=self.on_message, on_error=self.on_error,
                                         on_close=self.on_close)
        self.ws.on_open = self.on_open
        self.ws.audio_file = None
        # 公共参数(common)
        self.ws.CommonArgs = {"app_id": self.APPID}
        # 业务参数(business)，更多个性化参数可在官网查看
        self.ws.BusinessArgs = {"aue": "lame", "sfl": 1, "auf": "audio/L16;rate=16000", "vcn": "xiaoyan", "tte": "utf8"}

    def create_url(self):
        url = 'wss://tts-api.xfyun.cn/v2/tts'
        # 生成RFC1123格式的时间戳
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        # 拼接字符串
        signature_origin = "host: " + "ws-api.xfyun.cn" + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + "/v2/tts " + "HTTP/1.1"
        # 进行hmac-sha256进行加密
        signature_sha = hmac.new(self.APISecret.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()
        signature_sha = base64.b64encode(signature_sha).decode(encoding='utf-8')

        authorization_origin = "api_key=\"%s\", algorithm=\"%s\", headers=\"%s\", signature=\"%s\"" % (
            self.APIKey, "hmac-sha256", "host date request-line", signature_sha)
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
        # 将请求的鉴权参数组合为字典
        v = {
            "authorization": authorization,
            "date": date,
            "host": "ws-api.xfyun.cn"
        }
        # 拼接鉴权参数，生成url
        url = url + '?' + urlencode(v)
        return url

    def send(self, message):
        self.ws.data = {"status": 2, "text": str(base64.b64encode(message.encode('utf-8')), "UTF8")}
        websocket.enableTrace(False)
        url = self.create_url()
        self.ws.url = url

        self.ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

    # 收到websocket消息的处理
    @staticmethod
    def on_message(ws, message):
        try:
            message = json.loads(message)
            code = message["code"]
            sid = message["sid"]
            audio = message["data"]["audio"]
            audio = base64.b64decode(audio)
            status = message["data"]["status"]
            if status == 2:
                ws.close()
            if code != 0:
                err_msg = message["message"]
                print("sid:%s call error:%s code is:%s" % (sid, err_msg, code))
            else:

                with open('/tmp/demo.mp3', 'ab') as f:
                    f.write(audio)
                ws.audio_file = '/tmp/demo.mp3'

        except Exception as e:
            print("receive msg,but parse exception:", e)

    def get_result(self):
        while self.ws.audio_file is None:
            time.sleep(0.1)
        return self.ws.audio_file

    # 收到websocket连接建立的处理
    @staticmethod
    def on_open(ws):
        def run(*args):
            d = {"common": ws.CommonArgs,
                 "business": ws.BusinessArgs,
                 "data": ws.data,
                 }
            d = json.dumps(d)
            ws.send(d)
            path = pathlib.Path('/tmp/demo.mp3')
            if path.exists():
                path.unlink()

        thread.start_new_thread(run, ())


