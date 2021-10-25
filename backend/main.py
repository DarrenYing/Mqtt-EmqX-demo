# -*- coding: utf-8 -*-

import json
import time

import paho.mqtt.client as mqtt

HOST = "broker.emqx.io"
PORT = 8083
client_id = "backend_test" # 任意写


def on_connect(client, userdata, flags, rc):
    print(userdata, flags)
    print("Connected with result code " + str(rc))
    client.subscribe("data/receive")  # 订阅消息


def on_message(client, userdata, msg):
    print("主题:" + msg.topic + " 消息:" + str(msg.payload.decode('utf-8')))


def on_subscribe(client, userdata, mid, granted_qos):
    print("On Subscribed: qos = %d" % granted_qos)


def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected disconnection %s" % rc)


# 测试数据
data = {
    "type": 2,
    "timestamp": time.time(),
    "messageId": "9fcda359-89f5-4933-xxxx",
    "command": "xx/recommend",
}

if __name__ == '__main__':
    param = json.dumps(data)    # 若是字符串数据就不需要转化
    client = mqtt.Client(client_id, transport="websockets") # 和前端对应，websocket连接
    # client.username_pw_set("xxxxxx", "xxxxxx")
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_subscribe = on_subscribe
    client.on_disconnect = on_disconnect
    client.connect(HOST, PORT, 60)
    client.publish("topic/browser", payload=param, qos=0)  # 发送消息
    client.loop_forever()
