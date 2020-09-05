# RSS Monitor

轮询RSS，有新的条目或者已有条目内容发生变化时，发出提醒。

目前已支持 Dingtak Console方式。

建议结合RSSHub使用。

配置项请参考 [./config.demo.json](./config.demo.json)

使用步骤

```bash
cp config.demo.json config.json
vi config.demo.json
docker-compose up 
```


TODO: 

- diff