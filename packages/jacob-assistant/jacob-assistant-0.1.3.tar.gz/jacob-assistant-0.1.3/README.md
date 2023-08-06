<h2 align="center">Jacob-Assistant</h2>
Jacob-assistant是基于python开发的telegram机器人，旨在通过命令操作完成大部分的爬虫状态查询以及下载工作，为emby，jellyfin提供良好支持
## 安装
- [ ] docker
- pip
```bash
pip install jacob-assistant
```
- 生产环境需在配置中修改

## 使用

1. 由telegram提供查询入口，查询每天更新，以及分页
2. 对于网站的解析由爬虫模块解析，存入数据库
3. 我的宁夏打卡提醒
4. 可用参数
```text
-p 代理地址
-c --conf 配置文件地址

```
5. 配置文件格式
```ini
[general]
# debug warn info error
log_level = debug 

[telegram]
# 机器人密钥
bot_token = 1230304283:AAGDyZ0AiJNi9r9FP92Sfq10ZU6sAITbkYk
# 通知频道id，用来发布通知
announce_channel_id = -1001285705133
# 管理员id，用来配置管理员专属命令
admin_id = 551322172

[proxy]
proxy = true
url = socks5://127.0.0.1:10808

```
## License

MIT

## 流程



## TODO

- [x] 实现与telegram交互的功能
- [x] 实现爬虫的功能
- [ ] 实现调用aria2的功能
- [ ] 实现显示三天内更新
- [x] 实现打卡提醒
- [x] 区分开发环境与生产环境
- [ ] 引入自动部署
- [x] setup.py搞上
- [ ] github release搞上
- [ ] docker 搞上
- [x] 敏感信息转到配置文件中