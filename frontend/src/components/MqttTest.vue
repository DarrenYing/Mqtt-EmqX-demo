<template>
  <div class="hello">
    <h1>收到的消息:{{ receiveNews }}</h1>
    <button @click="doPublish">发布</button>
    <button @click="doSubscribe">订阅</button>
  </div>
</template>

<script>
import mqtt from "mqtt";

export default {
  name: "MqttTest",
  data() {
    return {
      connection: {
        host: 'broker.emqx.io',
        port: 8083,
        endpoint: '/mqtt',
        clean: true, // 保留会话
        connectTimeout: 4000, // 超时时间
        reconnectPeriod: 4000, // 重连时间间隔
        // 认证信息
        clientId: 'mqttjs_3be2c321',
        username: 'emqx_test',
        password: 'emqx_test',
      },

      subscription: {
        topic: 'topic/browser',
        qos: 0,
      },
      publish: {
        topic: 'topic/browser',
        qos: 0, // Quality of Service, 0 means At most once, 1 means At least once, 2 means exactly once
        payload: '{ "msg": "Hello, I am browser." }',
      },
      receiveNews: '',
      qosList: [
        {label: 0, value: 0},
        {label: 1, value: 1},
        {label: 2, value: 2},
      ],
      client: {
        connected: false,
      },
      subscribeSuccess: false,
    };
  },
  mounted() {
    const {host, port, endpoint, ...options} = this.connection
    const connectUrl = `ws://${host}:${port}${endpoint}`
    try {
      this.client = mqtt.connect(connectUrl, options)
    } catch (error) {
      console.log('mqtt.connect error', error)
    }

    this.client.on("connect", () => {
      console.log("连接成功");
    });

    this.client.on('error', error => {
      console.log('Connection failed', error)
    })

    this.client.on('message', (topic, message) => {
      // message = JSON.parse(message.toString()) # 可以转成字典
      this.receiveNews = message
      console.log(`Received message ${message} from topic ${topic}`)
    })


  },
  methods: {
    // 订阅主题
    doSubscribe() {
      const {topic, qos} = this.subscription
      this.client.subscribe(topic, {qos}, (error, res) => {
        if (error) {
          console.log('Subscribe to topics error', error)
          return
        }
        this.subscribeSuccess = true
        console.log('Subscribe to topics res', res)
      })
    },

    // 发送消息
    doPublish() {
      const {topic, qos} = this.publish
      const payload2 = JSON.stringify({
        'msg': Math.random(),
      })
      this.client.publish(topic, payload2, qos, (error) => {
        if (error) {
          console.log('Publish error', error)
        } else {
          console.log('Publish success')
        }
      })
    },

    // 取消订阅
    doUnSubscribe() {
      const {topic} = this.subscription
      this.client.unsubscribe(topic, error => {
        if (error) {
          console.log('Unsubscribe error', error)
        }
      })
    },

    // 断开连接
    destroyConnection() {
      if (this.client.connected) {
        try {
          this.client.end()
          this.client = {
            connected: false,
          }
          console.log('Successfully disconnected!')
        } catch (error) {
          console.log('Disconnect failed', error.toString())
        }
      }
    },
  }
};
</script>