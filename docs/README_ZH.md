# EpicGames Claimer

<!-- [START badges] -->

![](https://img.shields.io/badge/language-python-3572A5.svg) ![](https://img.shields.io/github/license/luminoleon/epicgames-claimer.svg) ![](https://img.shields.io/github/last-commit/luminoleon/epicgames-claimer.svg)

<!-- [END badges] -->

###### 其他语言：[English](../README.md)

> 自动领取Epic游戏商城[每周免费游戏](https://www.epicgames.com/store/free-games)。

十分简单易用，使用过程中几乎不需要输入或修改任何参数，并且可以自动与GitHub最新版本保持同步。

如果你觉得本项目对你有帮助，请star本项目。

## 开始

### Windows

[下载](https://github.com/luminoleon/epicgames-claimer/releases)

注意：Windows版本目前不支持自动更新。

#### Windows版本可选参数

| 参数                      | 说明                    | 备注            |
| ------------------------- | -----------------------| --------------- |
| `-h`, `--help`            | 查看帮助信息            |                 |
| `-n`, `--no-headless`     | 显示浏览器的图形界面     |                 |
| `-c`, `--chromium-path`   | 指定浏览器可执行文件路径 |                 |
| `-r`, `--run-at`          | 指定每日运行时间        | HH:MM，默认09:00 |
| `-o`, `--once`            | 运行一次领取过程后退出   |                 |
| `-u`, `--username`        | 设置用户名/邮箱         | 需要关闭双重验证  |
| `-p`, `--password`        | 设置密码                | 需要关闭双重验证 |

### Docker

``` bash
docker run -it luminoleon/epicgames-claimer
```

更多使用方法见[Docker hub页面](https://hub.docker.com/r/luminoleon/epicgames-claimer)。

### Python

要求Python >= 3.6。

#### 如何使用

1. 克隆/[下载](https://github.com/luminoleon/epicgames-claimer/releases)

    ``` bash
    git clone -b master https://github.com/luminoleon/epicgames-claimer.git
    cd epicgames-claimer
    ```

2. 安装Python模块

    ``` bash
    pip3 install -r requirements.txt
    ```

3. 安装依赖（仅Linux）

    ``` bash
    sudo sh install_dependencies.sh
    ```

4. 运行

    ``` bash
    python3 main.py
    ```

    <details>
    <summary>启用自动更新</summary>

    ```bash
    python3 main.py --auto-update
    ```

    </details>

    <details>
    <summary>无交互输入（需要关闭双重验证（2FA））</summary>

    ```bash
    python3 main.py -u <你的邮箱> -p <你的密码>
    ```

    </details>

#### Python版本可选参数

| 参数                    | 说明                     | 备注            |
| ----------------------- | ----------------------- | --------------- |
| `-h`, `--help`          | 查看帮助信息             |                 |
| `-n`, `--no-headless`   | 显示浏览器的图形界面      |                 |
| `-c`, `--chromium-path` | 指定浏览器可执行文件路径  |                 |
| `-r`, `--run-at`        | 指定每日运行时间         | HH:MM，默认09:00 |
| `-o`, `--once`          | 运行一次领取过程后退出    |                 |
| `-a`, `--auto-update`   | 启用自动更新             |                 |
| `-u`, `--username`      | 设置用户名/邮箱          | 需要关闭双重验证  |
| `-p`, `--password`      | 设置密码                 | 需要关闭双重验证 |

#### 注意事项

在Linux系统中，如果脚本不能正确运行，你可以尝试安装Chrome替代默认的Chromium（参考[Chrome headless doesn't launch on UNIX](https://github.com/puppeteer/puppeteer/blob/main/docs/troubleshooting.md#chrome-headless-doesnt-launch-on-unix)）。以下命令或许可以解决一些问题。

##### 安装Chrome

<details>
<summary>Debian（e.g. Ubuntu）</summary>

``` bash
curl -LO https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install -y ./google-chrome-stable_current_amd64.deb
rm google-chrome-stable_current_amd64.deb
```

</details>

<details>
<summary>CentOS</summary>

``` bash
curl -LO https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm
sudo yum install -y ./google-chrome-stable_current_x86_64.rpm
rm -I google-chrome-stable_current_x86_64.rpm
```

</details>

##### 使用Chrome替代默认浏览器

``` bash
python3 main.py --chromium-path google-chrome
```

## 已知问题

Windows系统中途结束脚本可能导致浏览器进程留在后台。请检查任务管理器并手动结束浏览器进程。