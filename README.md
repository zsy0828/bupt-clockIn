# bupt_clockIn
北邮疫情自动打卡，支持每日定时打卡，多人打卡，微信推送打卡状态

如果帮到你了就点个:star:吧～

## Framework

```
├── clockIn                   // 代码及配置文件目录
│  ├── clockIn.py             // 打卡脚本，只会执行一次，需要配合类似`cron`等具有支持定时功能的服务实现每日打卡
│  ├── clockIn_timing.py      // 无需定时服务支持，支持每日打卡
│  └── config.json            // 配置文件
├── docker-compose.yml        // docker-compose配置
├── LICENSE
├── README.md 
└── requirements.txt          // 相关依赖
```

## How To Use

### 相关准备

首先拉取项目：

`git clone https://github.com/KaleW515/bupt-clockIn.git`

项目目录中的`config.json`文件是配置文件，首先需要修改配置文件：

```json
{
  "username": "",
  "password": "",
  "time": "09:30",
  "appToken": "",
  "uid": ""
}
```

在`username`后面填上自己的学号，在`password`后面填上自己的密码，`time`可以修改默认自动打卡的时间，默认是`9：30`，如修改为`08：30`则是每天`8：30`进行打卡，这里注意如果时间只有一位数一定要在前面添加`0`，比如`8：30`是错误的，应该改为`08：30`

**注：项目支持多人打卡**

#### 多人打卡配置

多人打卡只需要仿照如下配置写即可，如果只需要单用户打卡需要删去多余用户

```json
{
  "kale": {
    "username": "",
    "password": "",
    "time": "08:00",
    "appToken": "AT_",
    "uid": "UID_"
  },
  "kale2": {
    "username": "",
    "password": "",
    "time": "08:15",
    "appToken": "",
    "uid": ""
  }
}
```

### 微信推送

如果不需要微信推送服务，则可以忽略该节。

本项目的微信推送用到了[WxPusher](https://github.com/wxpusher/wxpusher-client)，微信推送需要用到`config.json`配置文件中的`appToken`和`uid`字段。

1. 根据 [WxPusher](https://wxpusher.zjiecode.com/docs/#/)的文档首先注册并且创建应用，注册时会提示`appToken`，记录到`config.json`文件的`appToken`字段中

2. 创建完成后扫码关注应用，根据文档说明拿到自己的`uid`填到`config.json`文件中的`uid`字段中

3. 微信推送服务配置完成

   例如：

   ```json
   {
     "username": "2021xxxxxx",
     "password": "xxxxxxxxxx",
     "time": "09:30",
     "appToken": "AT_xxxxxxxxxxxxxxxxxxxx",
     "uid": "UID_xxxxxxxxxxxxxxxxxxxx"
   }
   ```

### 开始运行

项目提供了两种打卡的实现方式，项目更推荐第二种方式

#### 使用`cron`配合`clockIn.py`进行每日打卡

- 安装所需依赖：

  `pip install -r requirements.txt`

- 设置定时任务，例如

  `30 9 * * * python /home/kale/bupt-clockIn/clockIn.py`

  即可在每日的9点30分进行自动打卡

#### 使用`docker`完成脚本部署

- 项目根目录下有`docker-compose.yml`文件，输入命令：

  `docker-compose up`

  保持容器后台运行，即可实现每日打卡。**注意关机之后要重新启动执行命令启动容器**

- 也可以直接运行`clockIn_timing.py`文件，也能实现每日自动打卡
