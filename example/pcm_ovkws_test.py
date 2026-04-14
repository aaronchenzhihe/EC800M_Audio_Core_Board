import audio
import _thread
import utime
import Opus
rec = audio.Record(0)
pcm = audio.Audio.PCM(0, 1, 16000, 2, 1)

def kws_cb(para):
    print("kws cb:", para)
# 唤醒词
list = ["_xiao_zhi_xiao_zhi","_xiao_mu_xiao_mu","_xiao_yuan_xiao_yuan"]
    

rec.ovkws_set_callback(kws_cb)
rec.ovkws_start(list, 0.7)

def pcm_fun_test(para):
    opus = Opus(pcm, 0, 16000)  # 6000 ~ 128000     
    while True:
            opus.read(60)
            utime.sleep_ms(5)


def fun_start(func):
    _thread.start_new_thread(func, (1,))


fun_start(pcm_fun_test)
