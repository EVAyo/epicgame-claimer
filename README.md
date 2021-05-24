# Epic Games Claimer

自动领取[Epic Games每周免费游戏](https://www.epicgames.com/store/free-games)。脚本会在每天上午9:00自动检查并领取免费游戏。

## 开始

### Windows

[下载](https://github.com/luminoleon/epicgames-claimer/releases)

### Docker

``` bash
docker run -it -e TZ=<TimeZone> -v <Path>:/User_Data luminoleon/epicgames-claimer
```

将`<TimeZone>`替换成你所在的时区（Linux时区格式，e.g. Asia/Shanghai），`<Path>`替换成用来保存登录信息的路径（e.g. ~/epicgames-claimer/User_Data）。

按Ctrl + P + Q可切换至后台运行。

`-v`和`-e`参数是非必需的。如果遇到问题，`docker run -it luminoleon/epicgames-claimer`也可以正常运行。

### Python

``` bash
pip3 install schedule pyppeteer
git clone https://github.com/luminoleon/epicgames-claimer.git
cd epicgames-claimer
python3 epicgames_claimer.py
```

在Linux系统中需要安装Chromium依赖。Ubuntu系统可以通过以下命令安装。

```bash
sudo apt install gconf-service libasound2 libatk1.0-0 libatk-bridge2.0-0 libc6 libcairo2 libcups2 libdbus-1-3 libexpat1 libfontconfig1 libgcc1 libgconf-2-4 libgdk-pixbuf2.0-0 libglib2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libpangocairo-1.0-0 libstdc++6 libx11-6 libx11-xcb1 libxcb1 libxcomposite1 libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 libxss1 libxtst6 ca-certificates fonts-liberation libappindicator1 libnss3 lsb-release xdg-utils wget
```

## FAQ

### 如何登录我的Epic账号

在脚本启动后，如果没有已保存的登录信息则需要输入邮箱、密码以及两步验证代码完成登录。之后启动脚本无须再次登录。
