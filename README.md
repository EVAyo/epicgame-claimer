# Epic Games Claimer

自动领取[Epic Games每周免费游戏](https://www.epicgames.com/store/free-games)。脚本会在每天上午9:00自动检查并领取免费游戏。

## 开始

### Windows

[下载](https://github.com/luminoleon/epicgames-claimer/releases)

#### Windwos版本可选参数

见[Python版本可选参数](#Python版本可选参数)

### Docker

``` bash
docker run -it luminoleon/epicgames-claimer
```

按Ctrl + P + Q可切换至后台运行。

#### Docker版本可选参数

| 参数                    | 说明                                 |
|----------------------- | ------------------------------------ |
| `-e TZ=<TimeZone>`     | 设定容器的时区信息（默认Asia/Shanghai, [时区列表](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones#List)） |
| `-v <Path>:/User_Data` | 保存用户数据至本机路径                  |
| `-e run_at=<Time>`     | 设定每日运行时间（默认09:00, 格式HH:MM） |

### Python

要求Python >= 3.6。

``` bash
git clone https://github.com/luminoleon/epicgames-claimer.git
cd epicgames-claimer
pip3 install -r requirements.txt
python3 epicgames_claimer.py
```

#### Python版本可选参数

| 参数                                                 | 说明                                    |
|---------------------------------------------------- | --------------------------------------- |
| `-h`, `--help`                                      | 查看帮助信息                              |
| `-hf`, `--headful`                                  | 显示浏览器界面（有头模式）                  |
| `-c CHROMIUM_PATH`, `--chromium-path CHROMIUM_PATH` | 指定浏览器可执行文件路径                   |
| `-r RUN_AT`, `--run-at RUN_AT`                      | 指定每日运行时间（格式：HH:MM，e.g. 08:30） |
| `-o`, `--once`                                      | 运行一次领取过程后退出                     |

#### 注意事项

在Linux系统中需要安装Chromium依赖。Ubuntu系统可以通过以下命令安装。

``` bash
sudo apt install gconf-service libasound2 libatk1.0-0 libatk-bridge2.0-0 libc6 libcairo2 libcups2 libdbus-1-3 libexpat1 libfontconfig1 libgcc1 libgconf-2-4 libgdk-pixbuf2.0-0 libglib2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libpangocairo-1.0-0 libstdc++6 libx11-6 libx11-xcb1 libxcb1 libxcomposite1 libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 libxss1 libxtst6 ca-certificates fonts-liberation libappindicator1 libnss3 lsb-release xdg-utils wget
```

或者安装Chrome浏览器代替Chromium。

``` bash
curl -LO https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install -y google-chrome-stable_current_amd64.deb
python3 epicgames_claimer.py --chromium-path /usr/bin/google-chrome
```

## FAQ

### 如何登录我的Epic账号

在脚本启动后，如果没有已保存的登录信息则需要输入邮箱、密码以及两步验证代码完成登录。之后启动脚本无须再次登录。

## 已知问题

Windows系统中途结束脚本可能导致浏览器进程留在后台。请检查任务管理器并手动结束浏览器进程。
