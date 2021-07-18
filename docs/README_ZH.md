# EpicGames Claimer

<!-- [START badges] -->

![](https://img.shields.io/badge/language-python-3572A5.svg) ![](https://img.shields.io/github/license/luminoleon/epicgames-claimer.svg) ![](https://img.shields.io/github/last-commit/luminoleon/epicgames-claimer.svg)

<!-- [END badges] -->

###### 其他语言：[English](../README.md)

> 自动领取Epic游戏商城[每周免费游戏](https://www.epicgames.com/store/free-games)。

非常简单易用，使用过程中几乎不需要输入或修改任何参数，并且自动与GitHub最新版本保持同步。

如果你觉得本项目对你有帮助，请star本项目。

## 开始

### Windows

[下载](https://github.com/luminoleon/epicgames-claimer/releases)

注意：Windows版本目前不支持自动更新。

#### Windows版本可选参数

| 参数                      | 说明                                 |
| ------------------------- | ----------------------------------- |
| `-h`, `--help`            | 查看帮助信息                         |
| `-n`, `--no-headless`     | 显示浏览器的图形界面                 |
| `-c`, `--chromium-path`   | 指定浏览器可执行文件路径             |
| `-r`, `--run-at`          | 指定每日运行时间（HH:MM，默认09:00） |
| `-o`, `--once`            | 运行一次领取过程后退出               |

### Docker

``` bash
docker run -it luminoleon/epicgames-claimer
```

更多使用方法见[Docker hub页面](https://hub.docker.com/r/luminoleon/epicgames-claimer)。

### Python

要求Python >= 3.6。

``` bash
git clone -b master https://github.com/luminoleon/epicgames-claimer.git
cd epicgames-claimer
pip3 install -r requirements.txt
python3 main.py
```

如果你不想自动更新脚本，可以用`python3 epicgames_claimer.py`替代`python3 main.py`。

#### Python版本可选参数

| 参数                      | 说明                                 |
| ------------------------- | ----------------------------------- |
| `-h`, `--help`            | 查看帮助信息                         |
| `-n`, `--no-headless`     | 显示浏览器的图形界面                 |
| `-c`, `--chromium-path`   | 指定浏览器可执行文件路径             |
| `-r`, `--run-at`          | 指定每日运行时间（HH:MM，默认09:00） |
| `-o`, `--once`            | 运行一次领取过程后退出               |
| `-na`, `--no-auto-update` | 关闭自动更新                        |

#### 注意事项

在Linux系统中你可能需要安装Chromium依赖以使Chromium正常运行（参考[Chrome headless doesn't launch on UNIX](https://github.com/puppeteer/puppeteer/blob/main/docs/troubleshooting.md#chrome-headless-doesnt-launch-on-unix)）。或者安装其他Chromium内核的浏览器（比如Chrome）并使用`--chromium-path`指定浏览器可执行文件。以下命令或许可以解决一些问题。

##### 安装Chrome

基于Debian的Linux：

``` bash
curl -LO https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install -y ./google-chrome-stable_current_amd64.deb
rm google-chrome-stable_current_amd64.deb
```

基于Redhat的Linux：

``` bash
curl -LO https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm
sudo yum install -y ./google-chrome-stable_current_x86_64.rpm
rm -I google-chrome-stable_current_x86_64.rpm
```

##### 指定使用Chrome浏览器

``` bash
python3 main.py --chromium-path /usr/bin/google-chrome
```

<!--## 进阶用法

你可以将`epicgames_claimer.py`作为模块导入自己的Python脚本中。

### 最简单用法

``` Python
from epicgames_claimer import epicgames_claimer

claimer = epicgames_claimer()
claimer.login(email, password)
claimer.claim()
claimer.close_browser()
```

### 多账号

``` Python
from epicgames_claimer import epicgames_claimer

claimer_1 = epicgames_claimer(data_dir="user_1")
claimer_1.login(email_1, password_1)
claimer_1.claim()
claimer_1.close_browser()

claimer_2 = epicgames_claimer(data_dir="user_2")
claimer_2.login(email_2, password_2)
claimer_2.claim()
claimer_2.close_browser()

...
```-->

## 已知问题

Windows系统中途结束脚本可能导致浏览器进程留在后台。请检查任务管理器并手动结束浏览器进程。
