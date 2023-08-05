import paho.mqtt.client as mqtt
import uuid

from pygear3.model.Item import RequestItem
import base64

class MQTTConnector:
    def __init__(self, host, port, username, password, keepalive=60,client_id = str(uuid.uuid1())):
        self.connect_callback = None
        self.host = host
        self.port = port
        self.client = mqtt.Client(client_id)
        self.client.username_pw_set(username, password)
        self.client.on_connect = self.on_connect_callback
        self.client.on_disconnect = self.on_disconnect_callback
        self.client.connect(host, port, keepalive)

    def on_disconnect_callback(self,client, userdata, reasonCode, properties):
        print("断开连接:{},重新连接".format(reasonCode))
        self.client.connect(self.host, self.port, 60)
        print("连接成功")
    def on_connect_callback(self, client, userdata, flags, rc):
        ret = ""
        if rc == 0:
            ret += "MQTT服务器连接成功"
        elif rc == 1:
            ret += "MQTT服务器连接拒绝(无效的版本或协议)"
        elif rc == 2:
            ret += "MQTT服务器连接无效(无效的clientID和identifier标识符)"
        elif rc == 3:
            ret += "MQTT服务器连接拒绝(主机不可用)"
        elif rc == 4:
            ret += "MQTT服务器连接拒绝(无效的用户名或密码)"
        elif rc == 5:
            ret += "MQTT服务器连接拒绝(无效认证)"
        else:
            ret += "其它"
        if self.connect_callback:
            self.connect_callback(client, userdata, flags, rc)
        print(ret)

    def on_connect(self, func):
        self.connect_callback = func

    def on_message(self, func):
        self.client.on_message = func
    def reconnect(self,client_id):
        self.client.reinitialise(client_id)
    def on_disconnect(self, func):
        self.client.on_disconnect = func

    def unsubscribe(self,topic):
        self.client.unsubscribe(topic)
    def subscribe(self, topic):
        self.client.subscribe(topic=topic)

    def publish(self, topic, msg):
        self.client.publish(topic, msg)

    def start(self):
        self.client.loop_start()

    def stop(self):
        self.client.loop_stop()

    def loo(self):
        self.client.loop_forever()

    def publish_to_server(self,topic,task_type,content):
        msg = RequestItem(task_type,content).to_string()
        msg = base64.b64encode(msg.encode('utf-8'))
        self.publish(topic=topic,msg=msg)