# RSS Monitor

> 轮询RSS，有新的条目或者已有条目内容发生变化时，发出提醒。

:star: 目前已支持 Dingtak Console方式。

配置项请参考 [./config.demo.json](./config.demo.json), feeds填写feeds链接。建议结合[RSSHub](https://docs.rsshub.app/)使用, 
大多数网页已在Rsshub中提供feed路由链接。 

**使用说明**
1. 使用docker启动, 使用内置的sche定时器执行任务
```bash
cp config.demo.json config.json
vi config.demo.json
docker-compose up 
```
2. 直接运行: `python main.py`, 可拓展为cron、青龙

**更新日志**:
- 2022.05.28: 提供函数式入口
- 2020.09.21: 完成TODO功能, 显示Diff修改

**TODO**: 
- Email提醒