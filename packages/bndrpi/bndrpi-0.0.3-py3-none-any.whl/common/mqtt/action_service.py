
import os
import json
from concurrent.futures import ThreadPoolExecutor

from common.mqtt.action_enum import Action
from common.apihelper.localpushhelper import LocalPushHelper

from common.business.devicebusiness import DeviceBusiness

# 根据服务器下发的指令，判断做具体操作
class ActionService():

    def __init__(self, **dbConfig):
        self.deviceBusiness = DeviceBusiness(**dbConfig)
        self.executor = ThreadPoolExecutor(2)

    def update_db(self,message_id,at,data):
        print("update_db")
        
        print("消息ID："+message_id)
        print("发生时间："+at)
        print(data)

    def execute_shell(self,m=0):
        if m==0:    # 更新weight
            # os.system("sh ./scale.sh {0} {1} {2} {3} {4}".format(issend, hascode, fid, cid, smid))
            os.system("sh ./scale.sh")
        elif m==1:  # 更新flask
            pass
        elif m==2:  # 锁设备
            pass
        elif m==3:  # 解锁设备
            pass

    def update_config(self,message_id,at,data):
        self.executor.submit(self.execute_shell, 1)
        print("update_config")


    def start_service(self,message_id,at,data):
        model = self.deviceBusiness.getBaseInfo()
        
        # 判断是否是当前设备
        if data == model.devicecode and data is not None:
            # 杀死称重进程
            pass

        print("start_service")


    def stop_service(self,message_id,at,data):
        model = self.deviceBusiness.getBaseInfo()

        # 判断是否是当前设备
        if data == model.devicecode and data is not None:
            # 杀死称重进程
            helper = LocalPushHelper("http://127.0.0.1:5000/") 
            
            helper.KillWeightProgram()

            print("stop_service")


    def upload_data(self,message_id,at,data):
        print("upload_data")

    # 根据action判断要执行的方法
    def action(self,action, order):
        message_id = order.get('message_id')
        at = order.get('at')
        data = order.get('data')
   
        if action is Action.UPDATEDB:
            self.update_db(message_id,at,data)
        elif action == Action.UPDATECONFIG:
            self.update_config(message_id,at,data)
        elif action == Action.UPLOADDATA:
            self.upload_data(message_id,at,data)
        elif action == Action.STOPSERVICE:
            self.stop_service(message_id,at,data)
        elif action == Action.STARTSERVICE:
            self.start_service(message_id,at,data)