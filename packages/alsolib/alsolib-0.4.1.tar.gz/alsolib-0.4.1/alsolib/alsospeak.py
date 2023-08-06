import requests
import time
import pygame
import json,sys
g_gender="female"
g_rate=None
g_pitch=None

#设置语音性别
def setvoicemode(gender):
    if gender != "male" and gender != "female":
        raise Exception("参数必须为male(男人)或者female(女人)")

    global g_gender
    g_gender = gender


#设置语速
def setvoicespeed(rate):
    if not isinstance(rate, int) and not isinstance(rate, float):
        raise Exception("语速设置功能参数范围为0-100")

    if rate < 0 or rate > 100:
        raise Exception("语速设置功能参数范围为0-100")

    global g_rate
    g_rate = rate/50

def gettext():
    cookies = ""
    if len(sys.argv) > 1:
        try:
            cookies = json.loads(sys.argv[1])["cookies"]
        except:
            pass
    return cookies

def jsonLoads(str):
    try:
        return json.loads(str)
    except:
        return None
#设置音高
def sethighvoice():
    global g_pitch
    g_pitch = "high"

def jsonLoads(str):
    try:
        return json.loads(str)
    except:
        return None
#文本转语音
id='''
xesId=6852fcd37ea28ee6c51243cb5581ae0d; is_login=1; stu_id=7821237; stu_name=1355sarz; userGrade=8; xes-code-id=a441e8a7f4347a665cf2827c2e911b70.f6d9d3ceb13884a42b23e4bf524d604f; user-select=python; Hm_lvt_a8a78faf5b3e92f32fe42a94751a74f1=1597499818,1597534498,1597535540,1597535724; Hm_lpvt_a8a78faf5b3e92f32fe42a94751a74f1=1597538097; prelogid=4b104fc73cf4b76afe8c83b6995bdff2; xes_run_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiIuY29kZS54dWVlcnNpLmNvbSIsImF1ZCI6Ii5jb2RlLnh1ZWVyc2kuY29tIiwiaWF0IjoxNTk3NTM4MTAwLCJuYmYiOjE1OTc1MzgxMDAsImV4cCI6MTU5NzU1MjUwMCwidXNlcl9pZCI6Ijc4MjEyMzciLCJ1YSI6Ik1vemlsbGFcLzUuMCAoV2luZG93cyBOVCAxMC4wOyBXaW42NDsgeDY0KSBBcHBsZVdlYktpdFwvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lXC84NC4wLjQxNDcuMTI1IFNhZmFyaVwvNTM3LjM2In0.nGFljlxo_YX3Sgj0pWKp9EDp1wzD7vMpdKwz641I5jk; X-Request-Id=40a0b48ce5e9c29af462871ecd88b884
'''
def speak(text):
    text = text.strip()
    if text == "":
        raise Exception("文本不能为空")

    print("爱搜AI语言服务正在加载中...")

    global g_gender,g_rate,g_pitch
    params = {"text":text,"gender":g_gender,"rate":g_rate,"pitch":g_pitch}
    headers = {"Cookie": gettext()}
    rep = requests.get("https://code.xueersi.com/api/ai/python_tts/tts", params=params, headers=headers)
    repDic = jsonLoads(rep.text)
    if repDic is None:
        raise Exception("爱搜AI微软语言服务请求网络超时，请稍后再试")

    if repDic["stat"] != 1:
        raise Exception(repDic["msg"])

    voiceUrl = repDic["data"]["url"]
    duration = repDic["data"]["duration"]

    #下载语音文件
    r = requests.get(voiceUrl)
    filename = voiceUrl.split("/")[-1]
    with open(filename, "wb") as f:
        f.write(r.content)
    f.close()

    # 调用pygame播放
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

    print("爱搜语言服务处理完毕！")

    time.sleep(duration + 1)


def downloadvoice(text,loadfile):
    text = text.strip()
    if text == "":
        raise Exception("文本不能为空")

    print("爱搜AI语言服务正在加载中...")

    global g_gender, g_rate, g_pitch
    params = {"text": text, "gender": g_gender, "rate": g_rate, "pitch": g_pitch}
    headers = {"Cookie": gettext()}
    rep = requests.get("https://code.xueersi.com/api/ai/python_tts/tts", params=params, headers=headers)
    repDic = jsonLoads(rep.text)
    if repDic is None:
        raise Exception("爱搜AI微软语言服务请求网络超时，请稍后再试")

    if repDic["stat"] != 1:
        raise Exception(repDic["msg"])

    voiceUrl = repDic["data"]["url"]
    duration = repDic["data"]["duration"]

    # 下载语音文件
    r = requests.get(voiceUrl)
    filename = voiceUrl.split("/")[-1]
    try:
        with open(loadfile, "wb") as f:
            f.write(r.content)
        f.close()
        print("爱搜语言AI已下载成功\n")
    except:
        print("请输入正确的绝对路径!\n")