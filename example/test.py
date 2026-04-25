# -*- coding: UTF-8 -*-

"""
按键|语音唤醒
唤醒之后播放提示音频
使用vad,检测到有说话把标志1之后的音频数据存放到缓存区
缓存区数据处理，并播放
"""

import audio
import utime
import Opus
import _thread




# ==================== 音频管理 ====================

class AudioManager(object):

    def __init__(self, channel=0, volume=7, pa_number=33):
        self.aud = audio.Audio(channel)  # 初始化音频播放通道
        self.aud.set_pa(pa_number)
        self.aud.setVolume(volume)  # 设置音量
        self.rec = audio.Record(channel)
        self.rec.gain_set(3,9)
        self.__skip = 0
        self.tts = audio.TTS(0)
        
    # ========= opus ====================

    def open_opus(self):
        self.pcm = audio.Audio.PCM(0, 1, 16000, 2, 1, 15)  # 5 -> 25
        self.opus = Opus(self.pcm, 0, 60000)  # 6000 ~ 128000
    
    def close_opus(self):
        self.opus.close()
        self.pcm.close()
        del self.opus
        del self.pcm
    
    def opus_read(self):
        return self.opus.read(60)

    def opus_write(self, data):
        return self.opus.write(data)
    
    def tts_play(self, text):
        self.tts.play(4,0,2,text)

    # ========= vad & kws ====================

    def set_kws_cb(self, cb):
        self.rec.ovkws_set_callback(cb)
        
    def on_keyword_spotting(self, state):
        global flag
        print("on_keyword_spotting: {}".format(state))
        if state[0] == 0:
            if state[1] != 0:
                # 唤醒词触发
                flag = 1
                
    def set_vad_cb(self, cb):
        def wrapper(state):
            return cb(state)
        self._callable = wrapper
        self.rec.vad_set_callback(self._callable)

    def end_cb(self, para):
        if(para[0] == "stream"):
            if(para[2] == 1):
                pass
            elif (para[2] == 3):
                pass
            else:
                pass
        else:
            pass
    def start_kws(self):
        self.rec.ovkws_start("_xiao_yuan_xiao_yuan", 0.7)
   

    def stop_kws(self):
        self.rec.ovkws_stop()
    
    def start_vad(self):
        self.__skip = 0
        self.rec.vad_start()
    
    def stop_vad(self):
        self.rec.vad_stop()

    def on_voice_activity_detection(self, state):
        global state_flag
        state_flag = state
        print("on_voice_activity_detection: {}".format(state))
        if state == 1:
            print("检测到有人声")
        else:
            print("无人声")
            
            
            

flag = 0
state_flag = 0


if __name__ == '__main__':
    audio_manager = AudioManager()
    audio_manager.open_opus()

    if flag == 0:
        audio_manager.start_kws()
        audio_manager.set_kws_cb(audio_manager.on_keyword_spotting)
        
    is_listen_flag = False
        
    while True:
        audio_manager.opus_read()
        utime.sleep_ms(5)
        
        if flag == 1:
            audio_manager.close_opus()
            # audio_manager.stop_kws()
            
            audio_manager.tts_play("你好,我是小远同学")
            utime.sleep(3)
            print("播放完成")
            
            audio_manager.open_opus()
            audio_manager.set_vad_cb(audio_manager.on_voice_activity_detection)
            audio_manager.start_vad()
            print("开始VAD")
            try:
                while True:
                    audio_manager.opus_read()
                    if state_flag == 1:
                        pass
                    utime.sleep_ms(5)
            except KeyboardInterrupt:
                print("测试结束")
                audio_manager.stop_vad()
                audio_manager.close_opus()
            
            # while True:
            #     data = audio_manager.opus_read()

                    
        

      




