# mschedule
任务调度系统


## agent与master间消息设计

- agent注册消息

```json
{
    "type":"register",
    "payload":{
        "id":"uuid",
        "hostname":"xxx",
        "ip":"[ip1, ip2, ...]"
    }
}
```

- agent发送心跳消息

```json
{
    "type":"heartbeat",
    "payload":{
        "id":"uuid",
        "hostname":"xxx",
        "ip":"[ip1, ip2, ...]"
    }
}
```

- master向agent发送任务消息

```json
{
    "type":"task",
    "payload":{
        "id":"task-uuid",
        "script":"base64 encode",
        "timeout":0,
        "parallel":1,
        "fail_rate":0,
        "fail_count":-1
    }
}
```

parallel: 表示任务并行数量
fail_rate: 表示容忍的失败率，0表示不允许失败
fail_count: 表示失败数，-1表示不关心失败数量

- agent执行结果消息

```json
{
  "type": "result",
  "payload": {
    "id": "task-uuid",
    "agent_id": "agent-uuid",
    "code": 0,
    "output": "base64-encoded"
  }
}
```

id: 表示任务id
agent_id: 表示agent是谁
code: 表示任务执行的状态码，0正常，非零表示错误
output: 表示任务脚本执行的输出结果，以base64编码返回






