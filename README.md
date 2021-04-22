# Epicgames Claimer

自动领取Epic Games上的每周免费游戏。支持多账户。脚本会在启动后以及每天上午9:00自动检查并领取免费游戏。

## Getting started

### Docker

``` bash
docker run -it -e TZ=<TimeZone> luminoleon/epicgames-claimer
```

将`<TimeZone>`替换成你所在的时区（e.g. 中国：Asia/Shanghai）。

按Ctrl + P + Q可切换至后台运行。

### 直接运行

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

只需要在第一次运行添加账户后重启容器或脚本即可。

### 脚本开始运行后我该做些什么？

无论是第一次运行，还是重新启动，都需要输入一些信息才能正常运行。首次运行时需要输入账户和密码（也可能包括二次验证代码），之后重启脚本会看到添加账户、删除账户等选项，手动选择后脚本才会开始正常运行。

## Buy me a coffee

* [支付宝](Assets/Images/1619099359663.jpg)
* [微信](Assets/Images/1619109082376.png)
