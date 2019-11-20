# 消息队列

## Rocketmq

### 简介

RocketMQ作为一款纯java、分布式、队列模型的开源消息中间件，支持事

务消息、顺序消息、批量消息、定时消息、消息回溯等。

### 专业术语

| 名称           | 用途                                                         |
| -------------- | ------------------------------------------------------------ |
| Producer       | 消息生产者                                                   |
| Producer Group | 多个发送同一类消息的生产者称之为一个生产者组                 |
| Consumer       | 消息消费者                                                   |
| Consumer Group | 消费同一类消息的多个 consumer 实例组成一个消费者组           |
| Topic          | 一级消息类型,标题                                            |
| Tag            | 二级消息类型,标签                                            |
| keys           | Message索引键，多个用空格隔开，RocketMQ可以根据这些key快速检索到消息对消息关键字的提取方便查询，比如一条消息某个关键字是 运单号，之后我们可以使用这个运单号作为关键字进行查询 |
| Message        | 消息载体, 一个 Message 必须指定  topic，相当于寄信的地址。Message 还有一个可选的 tag 设置，以便消费端可以基于 tag 进行过滤消息 |
| Broker         | Broker 接收来自生产者的消息，储存以及为消费者拉取消息的请求做好准备。 |
| NameServer     | 用于管理所有Broker节点信息，接收Broker的注册/注销请求，此外还记录了Topic与Broker、Queue的对应关系，Broker主备信息 |

 

### Springboot 整合rabbitmq

#### 1. 发送消息

创建producer

DefaultMQProducer设置name或 groupname、nameserver地址、实例名称

producer.start()方法 开启生产者

创建message对象

设置消息体、topic、tag、keys

producer.send()方法发送消息

#### 2. 消费消息

 创建consumer

DefaultMQConsumer设置(set) 

name或 groupname、nameserver地址、实例名称、消息模式

consumer.subscribe(topic,tag)

```
consumer .registerMessageListener()触发consumeMsgCallback.onRecive(messages)
 
 
```

### 消息消费模式

　　　集群模式：默认模式，主题下的同一条消息只允许被其中一个消费者消费,消费进度存储在服务端

广播模式：主题下的同一条消息将被集群内的所有消费者消费一次,消费进度存储在消费者本地
