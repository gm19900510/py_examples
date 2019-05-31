# -*- coding: utf-8 -*-
import paho.mqtt.client as mqtt
import time
MQTTHOST = "192.168.41.249"
MQTTPORT = 1883
mqttClient = mqtt.Client()


# 连接MQTT服务器
def on_mqtt_connect():
    mqttClient.connect(MQTTHOST, MQTTPORT, 60)
    mqttClient.loop_start()
    
def on_subscribe():
    mqttClient.subscribe("service/101001001/configuration/request", 1)  # 主题为"test"
    mqttClient.subscribe("reboot", 1)
    mqttClient.on_message = on_message_come  # 消息到来处理函数

# 消息处理函数
def on_message_come(mqttClient, userdata, msg): 
    topic = msg.topic
    print("产生消息", msg.payload.decode("utf-8"))
    if topic.find('service/101001001/configuration/request') >= 0:
        mqttClient.publish('service/101001001/configuration/response', '{\"baqId\":\"0678a6c7-2549-4fc4-97dc-368c371eb6ae\",\"enabledEvents\":[\"EV_EMERGENCY_BUTTON\",\"EV_HELP\",\"EV_OUT_OF_PROCESS\",\"EV_RetentionRemind\",\"EV_ExitWithBracelet\",\"EV_Collusion\",\"EV_RoomPeopleNumChange\",\"EV_ESCAPE\",\"EV_RetentionAlert\",\"EV_CheckTimeTooShort\",\"EV_UnsupervisedInInquiryRoom\",\"EV_UnsupervisedInWaitingRoomRemind\",\"EV_UnsupervisedInWaitingRoomAlert\",\"EV_UNISEX\",\"EV_WaitingRoomOverloadRemind\",\"EV_WaitingRoomOverloadAlert\",\"EV_NotIsolated\",\"EV_AuxiliaryPoliceInvolveInquiry\",\"EV_Climbing\",\"EV_FallDown\",\"EV_GATHER\",\"ET_ViolentMotion\"]}', 1, False)  
    

        
if __name__ == '__main__':
    on_mqtt_connect()
    on_subscribe()
    '''
    for i in range(0, 101000):
        time.sleep(0.02) 
        #mqttClient.publish('face/album/add', '{"fileAllName":"1552011701316.jpg","faceId":"'+str(i)+'"}', 1, False)
        #mqttClient.publish('face/detection', '1552297814480.jpg', 1, False)
        #{"fileAllName":"1552011701316.jpg","faceId":"2"}
        mqttClient.publish('face/compare', '{"fileNames":"1552297814480.jpg,1552297814480.jpg","requestId":"12312312"}', 1, False)
    '''  
    for i in range(0, 101000):
        time.sleep(1) 
        #mqttClient.publish('people/counting/601028001/192.168.3.234/1', '{\"number\":\"2\",\"areaId\":\"1\",\"deviceId\":\"192.168.3.234\",\"time\":\"2018-11-07 14:30:30\",\"serviceId\":\"服务程序标识符\"}', 1, False)
    
    while True:
        pass  