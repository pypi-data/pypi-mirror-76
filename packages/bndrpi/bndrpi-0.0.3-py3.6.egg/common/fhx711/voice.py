# coding:utf-8

import os
import sys
# import threading
import importlib 


class Voice:
    def __init__(self):
        pass
    """
    def ILangReadTextAsync(self, cmd):
        try:
            thead_one = threading.Thread(target=self.ILangReadText, args=(cmd,))
            #thead_one = threading.Thread(target=test args=(cmd,))
            thead_one.start()
            #_thread.start_new_thread(self.ILangReadText, (cmd,))
        except Exception as e:
            print(e)
    """
    def ILangReadText(self, cmd):
        if not cmd:
            return

        return
        # 使用ilang读称重结果,需要提前reload一下sys，再设定系统指定参数为UTF-8
        importlib.reload(sys)
        #sys.setdefaultencoding('utf-8')

        cmd = "ilang {0}".format(cmd)
        #print(cmd)
        os.system(cmd)


if __name__ == "__main__":
    
    obj = Voice()

    cmd = "本次称重结果"+str(round(2523,2))+"克，约为"+str(round(2523/1000,2))+"千克"

    obj.ILangReadText(cmd)
    
    
        