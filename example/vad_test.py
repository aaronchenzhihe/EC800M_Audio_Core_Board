
import Opus
import audio
import utime
from machine import Pin
from usr.logging import getLogger
import osTimer



logger = getLogger(__name__)
volume = 5

# ==================== 音频管理 ====================

class AudioManager(object):

    def __init__(self, channel=0):
        self.rec = audio.Record(channel)
        self.rec.gain_set(4,9)
        self.__skip = 0

    # ========= opus ====================

    def open_opus(self):
        self.pcm = audio.Audio.PCM(0, 1, 16000, 2, 1, 15)  # 5 -> 25
        self.opus = Opus(self.pcm, 0, 6000)  # 6000 ~ 128000
    
    def close_opus(self):
        self.opus.close()
        self.pcm.close()
        del self.opus
        del self.pcm
    
    def opus_read(self):
        return self.opus.read(60)

    def opus_write(self, data):
        return self.opus.write(data)

    # ========= vad & kws ====================

            
    def set_vad_cb(self, cb):
        def wrapper(state):
            # if self.__skip != 2:
            #     self.__skip += 1
            #     return
            return cb(state)
        self.rec.vad_set_callback(wrapper)

    def start_vad(self):
        self.__skip = 0
        self.rec.vad_start()
    
    def stop_vad(self):
        self.rec.vad_stop()


def vad_callback(state):
    print("VAD状态变化:", state)
    # state == 1 表示检测到有人声，0 表示无人声



def main():
    audio_manager = AudioManager()
    audio_manager.set_vad_cb(vad_callback)
    audio_manager.open_opus()
    audio_manager.start_vad()
    print("开始VAD测试，按Ctrl+C退出")
    x=2
    try:
        while True:
            audio_manager.opus_read()
            utime.sleep_ms(10)
    except KeyboardInterrupt:
        print("测试结束")
        audio_manager.stop_vad()
        audio_manager.close_opus()

if __name__ == "__main__":    
    main()