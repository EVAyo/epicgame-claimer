# Epic Games Claimer

自动领取[Epic Games每周免费游戏](https://www.epicgames.com/store/free-games)。脚本会在每天上午9:00自动检查并领取免费游戏。

## 开始

### Github Actions

1. [关闭Epic账号的双重验证](https://www.epicgames.com/account/password)；
2. Fork本项目；
3. 在自己Fork项目的页面中，添加两条Secrets：EMAIL（你的Epic账号邮箱）、PASSWORD（你的Epic账号密码）；
4. 启用Actions并且手动触发一次。

### Windows

[下载](https://github.com/luminoleon/epicgames-claimer/releases)

### Docker

``` bash
docker run -it -e TZ=<TimeZone> -v <Path>:/User_Data luminoleon/epicgames-claimer
```

将`<TimeZone>`替换成你所在的时区（Linux时区格式，e.g. Asia/Shanghai），`<Path>`替换成用来保存登录信息的路径。

按Ctrl + P + Q可切换至后台运行。

`-v`和`-e`参数是非必需的。如果遇到问题，`docker run -it luminoleon/epicgames-claimer`也可以正常运行。

### Python

``` bash
pip install func_timeout schedule pyppeteer
git clone https://github.com/luminoleon/epicgames-claimer.git
cd epicgames-claimer
python epicgames_claimer.py
```

在Linux系统中需要安装Chromium依赖和桌面环境。

## FAQ

### 如何登录我的Epic账号

在脚本启动后，如果没有已保存的登录信息则需要输入邮箱、密码以及两步验证代码完成登录。之后启动脚本无须再次登录。
