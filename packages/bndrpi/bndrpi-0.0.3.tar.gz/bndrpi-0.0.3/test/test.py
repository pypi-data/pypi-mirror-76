"""
HX711 Load cell amplifier Python Library
Original source: https://gist.github.com/underdoeg/98a38b54f889fce2b237
Documentation source: https://github.com/aguegu/ardulibs/tree/master/hx711
Adapted by 2017 Jiri Dohnalek

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.


##################
PYTHON 3 EXAMPLE

This version of example is python 3 compatible
and outputs weight in grams.

Make sure you enter the correct values for offset and scale!
Also, don't forget to set the correct gain, default is 128.
"""

#import RPi.GPIO as GPIO
import time
import os
import sys
import decimal
import importlib 
#from hx711 import HX711

import threading
from time import ctime, sleep,time

################  设定校正固定值   ###############################

offset=  8461286.03125# 8461611.25 #8459770.4375 # 8459893.0625 # 8460192.3125 # 8474319.25
scale= 24.108259109311742# 23.03878048780488 # 28.635853658536586 # 24.30121951219512 # 24.450361445783134 #22.667583333333333

#除皮数量
packedWeight=0


# Force Python 3 ###########################################################

if sys.version_info[0] != 3:
    raise Exception("Python 3 is required.")

############################################################################

# 使用树莓派的5号和6号引脚
hx = HX711(5, 6)


def cleanAndExit():
    print("Cleaning...")
    GPIO.cleanup()
    print("Bye!")
    sys.exit()


def setup():
    """
    code run once
    """
    hx.set_offset(offset)
    hx.set_scale(scale)
# 称重结果最终是需要四舍五入的，这里设定decimal的方式为四舍五入
decimal.getcontext().rounding = "ROUND_HALF_UP"

def loop():
    try:
        print('-----------------------')
        print(time.ctime())
        weight = hx.get_grams(2)
        print(time.ctime())

        read = decimal.Decimal(weight-packedWeight)

        val = float(weight)
        #print(val)
        #  print(val,'grams')
        print('称重结果：',weight,"克,约为：",round(read/1000,2),"千克")
        
#       使用ilang读称重结果,需要提前reload一下sys，再设定系统指定参数为UTF-8
        #importlib.reload(sys)
#       sys.setdefaultencoding('utf-8')
        #cmd = "ilang 称重结果"+str(round(read,2))+"克，约为"+str(round(read/1000,2))+"千克"
        #os.system(cmd)
        time.sleep(1)

        #hx.power_down()
      #  time.sleep(0.001)
        #hx.power_up()

       # time.sleep(0.2)
    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()

def readWe(i):
    try:
        aa = []
        
        w = hx.get_grams(3)

        s = "i:{0} weight:{1} time:{2}".format(i,w, ctime())
        #print(s)
        return s
    except Exception as e:
        return e

def backF(s):
    print(s)
##################################

class MyThread(threading.Thread):

    def __init__(self, func, args=()):
        super(MyThread, self).__init__()
        self.func = func
        self.args = args

    def run(self):
        self.result = self.func(*self.args)

    def get_result(self):
        try:
            return self.result   # 如果子线程不使用join方法，此处可能会报没有self.result的错误
        except Exception:
            return None

if __name__ == "__main__":

    print(int(time.mktime(time.strptime(time.localtime(),"%Y-%m-%d %H:%M:%S"))) )
    # setup()
    # readWe(0)
    # #readWe(10)
    # #readWe(100)
    # d = time()

    # t = MyThread(readWe,args=(1,))
    # t2 = MyThread(readWe,args=(2,))
    # t3 = MyThread(readWe,args=(3,))
    # t4 = MyThread(readWe,args=(4,))

    # t.start()
    # t2.start()
    # t3.start()
    # t4.start()

    # t.join()
    # t2.join()
    # t3.join()
    # t4.join()
    # print(t.get_result())
    # print(t2.get_result())
    # print(t3.get_result())
    # print(t4.get_result())
    # #pool.apply_async(readWe,args=(3,),callback=backF)

    # #pool.close()
    # # 调用join之前，先调用close函数，否则会出错。执行完close后不会有新的进程加入到pool，join函数等待所有子进程结束
    # #pool.join()  
    # d2 = time()

    # print(d2-d)
    #sleep(5)
    """
    while True:
        
        loop()
    """
