# Epic Games Claimer

自动领取[Epic Games每周免费游戏](https://www.epicgames.com/store/free-games)。脚本会在每天上午9:00自动检查并领取免费游戏。

## 开始

### Windows

[下载](https://github.com/luminoleon/epicgames-claimer/releases)

### Docker

``` bash
docker run -it -e TZ=<TimeZone> luminoleon/epicgames-claimer
```

将`<TimeZone>`替换成你所在的时区（Linux时区格式，e.g. Asia/Shanghai）。

按Ctrl + P + Q可切换至后台运行。

如果你不清楚如何设置时区，`docker run -it luminoleon/epicgames-claimer`同样可以正常运行，只是容器内的时间可能不正确。

### Python

``` bash
pip install func_timeout schedule pyppeteer
git clone https://github.com/luminoleon/epicgames-claimer.git
cd epicgames-claimer
python claimer.py
```

在Linux系统中需要安装Chromium依赖和桌面环境。

## FAQ

### 如何登录我的Epic账号?

在脚本启动后，如果没有cookies则需要输入邮箱、密码以及两步验证代码完成登录。之后启动脚本无须再次登录。

## 赞助

* [支付宝](Assets/Images/1619099359663.jpg)
* [微信](Assets/Images/1619109082376.png)
