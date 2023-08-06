import os
import pathlib
import speech_recognition as sr

from ddm.baidu import RecognizerType, client
from ddm.config import iflytek_text_app, iflytek_audio_app

recognizer = sr.Recognizer()
recognizer.dynamic_energy_threshold = False


def record(file_name: str = "recording.wav", mention: str = '', rate=16000, timeout=10):
    """获取录音信息"""
    if not file_name.endswith('.wav'):
        raise Exception("文件后缀必须为.wav")
    with sr.Microphone(sample_rate=rate) as mic:
        # 处理环境噪声
        recognizer.adjust_for_ambient_noise(mic, 1.5)
        try:
            print(mention)
            audio = recognizer.listen(mic, timeout=timeout)
        except Exception:
            return None
    file_path = os.path.join('/tmp', file_name)
    with open(file_path, "wb") as file:
        file.write(audio.get_wav_data())
    return file_path


def convert_audio_to_text_baidu(file_path: str, rate: int = 16000, dev_pid=RecognizerType.PU_TONG_HUA):
    """采用百度api转换语音"""
    with open(file_path, 'rb') as f:
        audio_data = f.read()

    result = client.asr(audio_data, 'wav', rate, {
        'dev_pid': dev_pid.value,
    })

    if result['err_no'] != 0:
        raise Exception(f"error msg:{result['err_msg']},'err_no':{result['err_no']}")

    result_text = result["result"][0]
    return result_text


def convert_audio_to_text_iflytek(audio_file: str):
    """采用科大讯飞的api转换语音"""
    iflytek_audio_app.send(audio_file)
    return iflytek_audio_app.get_result()


def convert_text_to_audio_iflytek(audio_file: str):
    """采用科大讯飞的api转换文字为语音"""
    iflytek_text_app.send(audio_file)
    file = iflytek_text_app.get_result()
    target = '/tmp/message.wav'
    convert_audio_file_format(file, target)
    return target


def convert_audio_file_format(source, target):
    """转换音频文件的格式"""
    target_path = pathlib.Path(target)
    if target_path.exists():
        target_path.unlink()
    os.system(f'sudo sox {source} {target}')
    return True


def play_audio(audio_file):
    """播放音频"""
    os.system(f'sudo aplay -D hw:Headphones {audio_file}')
