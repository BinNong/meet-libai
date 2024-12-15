# 💐飞花令功能

##  :factory: 功能介绍

飞花令是古时候的一种酒令，在酒桌上，大家轮流吟诗作对，以诗句中的某个字为关键字，进行接龙，谁接不上来，谁就罚酒。

## :gear: 功能实现

飞花令功能主要由`lang_chain/poetry_game.py`实现，实现逻辑如下：

1. 如果用户输入的是退出指令，则结束当前游戏，并结束游戏。
2. 如果用户输入的是飞花令指令，则开始飞花令游戏。
3. 如果用户输入的是其他指令，则正常对话模式。
4. 如果输入重复的诗句,则提示用户已经重复。在玩飞花令的过程中，将所有诗句存储在redis中，如果用户输入的诗句在redis中已经存在，则提示用户已经重复。
5. 如果用户输入的诗句在redis中不存在，则将用户输入的诗句存储在redis中，并提示用户输入成功。
6. 飞花令游戏中有时间限制，超过10分钟游戏，结束游戏。通过在redis中设置过期时间，实现时间限制。
   
## :key: 使用方法

1. 输入`/飞花令`，开始飞花令游戏。
2. 输入`/退出游戏`，结束飞花令游戏。
3. 输入`/游戏结束`，结束飞花令游戏。
4. 输入`/结束游戏`，结束飞花令游戏。

## :sailboat: 依赖安装步骤

1. 安装依赖

```bash
pip install -r requirements.txt
```

2. 安装redis server用于存储飞花令诗句

为了便于快速体验，强烈建议使用docker进行安装, 并设置初始密码
```bash
docker run -d --name redis-server -p 6379:6379 redis redis-server --requirepass "123456"
```

3. 在config文件中的yaml文件中配置redis server的地址和密码
   默认在config/config-local.yaml文件中，第34行，配置redis server的地址和密码
   ```yaml
   redis:
     host: localhost
     port: 6379
     password: 123456
   ```

 4. 可以安装redis可视化工具，便于查看redis中的数据。比如:another-redis-desktop-manager

ssh -p 47398 root@connect.cqa1.seetacloud.com

r298HNLe3/JX
