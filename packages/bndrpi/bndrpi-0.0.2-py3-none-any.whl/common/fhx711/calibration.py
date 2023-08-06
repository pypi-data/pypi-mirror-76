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

######################################################################
README:

This version runs in python 3.x. It will first prompt the user to 
empty the scale. Then prompt user to place an item with a known weight
on the scale and input weight as INT. 

The offset and scale will be adjusted accordingly and displayed for
convenience.

The user can choose to [0] exit, [1] recalibrate, or [2] display the 
current offset and scale values and weigh a new item to test the accuracy
of the offset and scale values!
#######################################################################
"""

import RPi.GPIO as GPIO
import time
import sys
from common.fhx711.hx711 import HX711

# Force Python 3 ###########################################################

if sys.version_info[0] != 3:
    raise Exception("请在Python3环境下运行")

############################################################################

class Calibration:
    def __init__(self, timepin=None, datapin=None):
        if not timepin:
            self.timepin = 5
        else:
            self.timepin = timepin

        if not datapin:
            self.datapin = 6
        else:
            self.datapin = datapin
        
        self.hx = HX711(self.timepin, self.datapin, gain=128)

        self.SetUp()

    def CleanAndExit(self):
        #print("Cleaning up...")
        #清除你写的脚本中使用的GPIO通道。也会清除正在使用的引脚编号系统。
        GPIO.cleanup()
        #print("Bye!")
        sys.exit()

    def SetUp(self):
        """
        code run once
        """
        #print("初始化.\n 请确保称是空的.")
        while True:
            if (GPIO.input(hx.DOUT) == 0):
                pass
            if (GPIO.input(hx.DOUT) == 1):
                #print("初始化完成!")
                break

    def CalibrateScale(self):
        readyCheck = input("请确保秤是空的，然后按任意键开始.")
        offset = hx.read_average()
        #print("空值(offset): {}".format(offset))
        hx.set_offset(offset)
        #print("请在称上放上已知重量的物品")

        readyCheck = input("放好物品后，按任意键继续.")
        measured_weight = (hx.read_average()-hx.get_offset())
        item_weight = input("请输入放置的物品的重量，单位：克.\n>")
        scale = int(measured_weight)/int(item_weight)
        hx.set_scale(scale)
        #print("调整比例为: {}".format(scale))
        #print('请将校准后的offset:{0} scale:{1} 值保存到配置文件中'.format(offset, scale))

    def LoopScaleWeight(self):
        
        while True:
            #print('所称重量为:{0} 克 \n'.format(self.hx.get_grams()))

            time.sleep(0.5)


    def ScalageOption(self):
        try:
            while True:
                
                weight = self.hx.get_grams()

                self.hx.power_down()
                time.sleep(0.001)
                self.hx.power_up()

                #print('所称重量为:{0} 克 \n'.format(weight))

                choice = input("请选择：\n"
                                "[1] 重新校准电子秤 \n"
                                "[2] 查看默认offset 和 scale值 \n"
                                "[0] 退出 \n")

                if choice == "1":
                    self.CalibrateScale()
                elif choice == "2":
                    #print("\nOffset: {}\nScale: {}".format(self.hx.get_offset(), self.hx.get_scale()))
                    pass
                elif choice == "0":
                    #self.CleanAndExit()
                    break
                else:
                    #print('请选择正确的选取 \n')
                    pass

        finally:
            self.CleanAndExit()


if __name__ == "__main__":

    obj = Calibration(5, 6)

    obj.ScalageOption()
    
