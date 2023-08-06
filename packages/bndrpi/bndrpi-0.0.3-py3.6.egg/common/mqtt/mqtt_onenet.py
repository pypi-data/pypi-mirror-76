#! /usr/bin/env python

# coding: utf-8 

import base64
import hmac
import json
import struct
import time
import random
from multiprocessing import Pool
import paho.mqtt.client as mqtt

from common.view.syncweightview import SyncWeightView

from common.mqtt.action_enum import Action
from common.mqtt.action_service import ActionService
#from upload_weight import UploadWeight

DEV_ID = "612588067"  # 设备ID,和中国移动OneNet平台上的设备ID对应
PRO_ID = "363042"  # 产品ID
DEV_NAME = '测试设备'
accesskey = "/aoGw2iREH9IHE5+f1f1RZKrjLx/tj/36NeXG76Rp7M="
AUTH_INFO = 'pjOrWXRQBajo1kKnbNHlVtwfm0g='

TYPE_JSON = 0x01
TYPE_FLOAT = 0x17

DB_Config = None


# 定义上传数据的json格式  该格式是oneNET规定好的  按格式修改其中变量即可

# dbody = {
#     "datastreams": [
#         {
#             "id": "weight",  # 对应OneNet的数据流名称
#             "datapoints": [
#                 {
#                     # 发货详情数据
#                     # 数据提交时间，这里可通过函数来获取实时时间
#                     "at": int(time.time()),
#                     "value":{
#                         "message_id":random.randint(1,999999999999999),
#                         "type":1,            # 0:收货数据  1:发货单数据  2：发货详情数据
#                         "id":"200730500001", # 发货id|收货编号
#                         "sid": '200730500',  # 发货单编号数据值
#                         "fid": 1,            # 共享工厂编号
#                         "fname":"共享工厂",   # 共享工厂名称
#                         "ffid":1,            # 养殖场编号
#                         "ffname":"",         # 养殖场编号
#                         "cid":1,             # 客户编号
#                         'codeid':'',         # 二维码编号
#                         'spid':1,             # 收货规格编号
#                         "cweight":0,    # 纸箱重量
#                         'rweight':45.4,      # 真是重量
#                         'sweight':38,         # 码数                       
#                     }
                    
#                 }
#             ]
#         }
#     ]
# }

# dbody2 = {
#     "datastreams": [
#         {
#             "id": "rweight",  # 对应OneNet的数据流名称
#             "datapoints": [
#                 {
#                     # 收货详情数据
#                     # 数据提交时间，这里可通过函数来获取实时时间
#                     "at": int(time.time()),
#                     "value":{
#                         "message_id":random.randint(1,999999999999999),
#                         #"type":1,            # 0:收货数据  1:发货单数据  2：发货详情数据
#                         "receiveid":"200730500001", # 收货编号
#                         "factoryid": 1,            # 共享工厂编号
#                         'factoryname': "河北",
#                         "farmid":1,             # 养殖场编号
#                         "farmname":"",           # 养殖场名称
#                         'codeid':'',         # 二维码编号
#                         'specificationid':1,             # 收货规格编号
#                         "cartonweight":3,           # 皮重
#                         'realweight':45.4,      # 真是重量
#                         'standardweight':38         # 码数                       
#                     }
                    
#                 }
#             ]
#         }
#     ]
# }

# dbody3 = {
#     "datastreams": [
#         {
#             "id": "sweight",  # 对应OneNet的数据流名称
#             "datapoints": [
#                 {
#                     # 发货详情数据
#                     # 数据提交时间，这里可通过函数来获取实时时间
#                     "at": int(time.time()),
#                     "value":{
#                         "message_id":random.randint(1,999999999999999),
#                         #"type":1,            # 0:收货数据  1:发货单数据  2：发货详情数据
#                         "id":"200730500001", # 发货id|
#                         "shipmentid": '200730500',  # 发货单编号数据值
#                         "factoryid": 1,            # 共享工厂编号
#                         'factoryname': "河北",
#                         "farmid":1,             # 养殖场编号
#                         "farmname":"",           # 养殖场名称
#                         'codeid':'',         # 二维码编号
#                         'specificationid':1,             # 收货规格编号
#                         "cartonweight":3,           # 皮重
#                         'realweight':45.4,      # 真是重量
#                         'standardweight':38         # 码数                      
#                     }
                    
#                 }
#             ]
#         }
#     ]
# }

# dbody4 = {
#     "datastreams": [
#         {
#             "id": "sorder",  # 对应OneNet的数据流名称
#             "datapoints": [
#                 {
#                     # 发货订单数据
#                     # 数据提交时间，这里可通过函数来获取实时时间
#                     "at": int(time.time()),
#                     "value":{
#                         "message_id":random.randint(1,999999999999999),
#                         #"type":1,            # 0:收货数据  1:发货单数据  2：发货详情数据
#                         "shipmentid": '200730500',  # 发货单编号数据值
#                         "factoryid": 1,            # 共享工厂编号
#                         "customerid": 1,            # 客户编号                    
#                     }
                    
#                 }
#             ]
#         }
#     ]
# }
    

def build_payload(type, payload):
    datatype = type
    packet = bytearray()
    packet.extend(struct.pack("!B", datatype))
    if isinstance(payload, str):
        udata = payload.encode('utf-8')
        length = len(udata)
        packet.extend(struct.pack("!H" + str(length) + "s", length, udata))
    return packet

def pack_body(d):
    if d is None:
        return None
    
    print(d.type)
    if d.type=='0':
        return {
            "datastreams": [
                {
                    "id": "rweight",  # 对应OneNet的数据流名称
                    "datapoints": [
                        {
                            # 发货详情数据
                            # 数据提交时间，这里可通过函数来获取实时时间
                            "at": int(time.time()) ,
                            "value":{
                                "message_id":random.randint(1,999999999999999),
                                "receiveid":d.id, # 收货编号
                                "factoryid": d.fid,            # 共享工厂编号
                                "batchid": d.batchid,          # 批次编号
                                'factoryname': d.fname,
                                "farmid": d.ffid,             # 养殖场编号
                                "farmname": d.ffname,           # 养殖场名称
                                'codeid': d.codeid,         # 二维码编号
                                'specificationid': d.spid,             # 收货规格编号
                                "cartonweight": d.cweight,           # 皮重
                                "grossgeight": d.gweight,
                                'realweight': d.rweight,      # 真是重量
                                'standardweight': d.sweight,         # 码数       
                                "receivetime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())           
                            }
                            
                        }
                    ]
                }
            ]
        }
    elif d.type == '1':
        return {
            "datastreams": [
                {
                    "id": "sweight",  # 对应OneNet的数据流名称
                    "datapoints": [
                        {
                            # 发货详情数据
                            # 数据提交时间，这里可通过函数来获取实时时间
                            "at": int(time.time()) ,
                            "value":{
                                "message_id":random.randint(1,999999999999999),     
                                "id": d.id, # 发货id|
                                "shipmentid": d.sid,  # 发货单编号数据值
                                "factoryid": d.fid,            # 共享工厂编号
                                # 'factoryname': d.fname,
                                "farmid": d.ffid,             # 养殖场编号
                                # "farmname": d.ffname,           # 养殖场名称
                                'codeid': d.codeid,         # 二维码编号
                                'specificationid': d.spid,             # 收货规格编号
                                "cartonweight": d.cweight,           # 皮重
                                "grossgeight": d.gweight,
                                'realweight': d.rweight,      # 真是重量
                                'standardweight': d.sweight,         # 码数                                                 
                                "updatetime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())   
                            }
                            
                        }
                    ]
                }
            ]
        }
    else:
        return {
            "datastreams": [
                {
                    "id": "sorder",  # 对应OneNet的数据流名称
                    "datapoints": [
                        {
                            # 发货详情数据
                            # 数据提交时间，这里可通过函数来获取实时时间
                            "at": int(time.time()) ,
                            "value":{
                                "message_id":random.randint(1,999999999999999), 
                                "shipmentid": d.sid,  # 发货单编号数据值
                                "factoryid": d.fid,            # 共享工厂编号
                                "customerid": d.cid,            # 客户编号    
                                "updatetime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())                   
                            }
                            
                        }
                    ]
                }
            ]
        }


def upload_msg(client, d):
    
    pd = pack_body(d)

    # print(pd)
    if pd is None:
        print('is none')
        return

     # 上传数据
    json_body = json.dumps(pd)

    # print(json_body)

    packet = build_payload(TYPE_JSON, json_body)

    client.publish("$dp", packet, qos=1)  # qos代表服务质量


def getClient(**dbConfig):
    DB_Config = dbConfig
    # print(DB_Config)
    client = mqtt.Client(client_id=DEV_ID, protocol=mqtt.MQTTv311)
    
    # client.on_connect = on_connect
    # client.on_publish = on_publish
    # client.on_message = on_message

    client.username_pw_set(username=PRO_ID, password=AUTH_INFO)

    client.on_connect = on_connect2
    client.on_publish = on_publish2
    client.on_message = on_message2
    
    return client

def connect2(client):
    # print('--------------------********************')
    client.connect('183.230.40.39', port=6002, keepalive=120)
    # client.loop_start()
    client.loop_forever()


# 当客户端收到来自服务器的CONNACK响应时的回调。也就是申请连接，服务器返回结果是否成功等
def on_connect2(client, userdata, flags, rc):
    #print(user)
    #print('2*****************')
    print("连接结果:" + mqtt.connack_string(rc))
    
   


# 接收从服务器下发的命令
def on_message2(client, userdata, msg):
    # print('---------------------------')
    print("收到下发命令:"+str(msg.payload,'utf-8'))
    order_str = str(msg.payload, 'utf-8')
    order = json.loads(order_str)
    action = order.get('action')
    # 根据Action指令，做不同的处理
    act = Action(action)
    if act is None:
        print("action is not available")
    else:
        action_service = ActionService(**DB_Config).action
        action_service(act, order)


# 当消息已经被发送给中间人，on_publish()回调将会被触发
def on_publish2(client, userdata, mid):
    print("mid:" + str(mid))

def asy_connect(client):
    pool = Pool(1)
    pool.apply_async(connect, args=(client,)) 

    pool.close()
    pool.join()

def is_connect2(client):
    return client.is_connected()

def reconnect2(client):
    client.reconnect()

def disconnect2(client):
    client.disconnect()

def main():
    
    # client = getClient()
    # connect(client)
    
    # client = mqtt.Client(client_id=DEV_ID, protocol=mqtt.MQTTv311)
    # print(client._last_mid)
    # client.on_connect = on_connect
    # client.on_publish = on_publish
    # client.on_message = on_message


    # client.username_pw_set(username=PRO_ID, password=AUTH_INFO)
    # client.connect('183.230.40.39', port=6002, keepalive=120)
    
    
    # client, message_id, device_id, weight
    # 推送对象
    pushObj = SyncWeightView()
    # type 0:收货数据  1:发货单数据  2：发货详情数据
    pushObj.type = 2
    pushObj.id = '200730151201'
    pushObj.sid = '200730151202'
    pushObj.fid = 1
    pushObj.codeid = '200730151203'
    pushObj.spid = 1
    pushObj.rweight = 45
    pushObj.sweight = 36
    pushObj.cid = 1

    # upload_msg(client, pushObj)

    # client.loop_forever()
    
    


if __name__ == '__main__':
    main()
