# Epicgames Claimer

自动领取Epic Games上的每周免费游戏。支持多账户。脚本会在每天上午9:00自动检查并领取免费游戏。

## Getting started

### Docker

``` bash
docker run -it -e TZ=<TimeZone> luminoleon/epicgames-claimer
```

将`<TimeZone>`替换成你所在的时区（e.g. Asia/Shanghai）。

按Ctrl + P + Q可切换至后台运行。

### Python

``` bash
git clone https://github.com/luminoleon/epicgames-claimer.git
cd epicgames-claimer
python claimer.py
```

在Linux系统中需要安装Chromium依赖和桌面环境。

## FAQ

### 为什么不需要输入账户和密码？

账户和密码需要在脚本运行过程中输入。

### 如何添加多个账户？

只需要在第一次运行时，完成添加账户的操作后重新运行容器或脚本即可。重新启动后10分钟内无操作脚本将自动继续运行。

## Buy me a coffee

* [支付宝](Assets/Images/1619099359663.jpg)
* [微信](Assets/Images/1619109082376.png)
