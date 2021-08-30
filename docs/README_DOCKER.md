# EpicGames Claimer

Claim [weekly free games](https://www.epicgames.com/store/free-games) from Epic Games Store.

If you think this project is helpful to you, please star this project.

自动领取Epic游戏商城[每周免费游戏](https://www.epicgames.com/store/free-games)。

如果你觉得本项目对你有帮助，请star本项目。

## English

### Getting Started

``` bash
docker run -it luminoleon/epicgames-claimer
```

After successful login, you can press Ctrl + P + Q to switch to the background.

### Some Examples

* Save account information to local path(Then you don't need to login the next time when you start a new container):

    ```bash
    docker run -it -v ~/epicgames_claimer/User_Data:/User_Data luminoleon/epicgames-claimer
    ```

* Adjust to the time zone of the container:

    ```bash
    docker run -it -e TZ=<YOUR TIME ZONE> luminoleon/epicgames-claimer
    ```

    [Available Time Zones](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones#List)

* No interactive input(Need to disable two-factor authentication(2FA)):

    ```bash
    docker run -d luminoleon/epicgames-claimer -u <YOUR EMAIL> -p <YOUR PASSWORD>
    ```

#### Environment Variables

| Variable | Description                       | Default       | Note        |
| -------- | --------------------------------- | ------------- | ----------- |
| TZ       | the time zone of the container, [Available Time Zones](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones#List)           | Asia/Shanghai |             |
| RUN_AT      | set daily check and claim time | 09:00 | format to HH:MM     |
| ONCE        | claim once then exit           | false | true/false          |
| AUTO_UPDATE | enable auto update             | false | true/false          |
| EMAIL       | set username/email             |       | need to disable 2FA |
| PASSWORD    | set password                   |       | need to disable 2FA |

#### Optional Arguments

Notice: When the corresponding environment variable exists, the value of the argument will be overwritten by the value of the corresponding environment variable.

Usage: `docker run luminoleon/epicgames-claimer [-h] [-r RUN_AT] [-o] [-a] [-u USERNAME] [-p PASSWORD]`

| Arguments               | Description                    | Note                    |
| ----------------------- | ------------------------------ | ----------------------- |
| `-h`, `--help`          | show the help message          |                         |
| `-r`, `--run-at`        | set daily check and claim time | HH:MM, default to 09:00 |
| `-o`, `--once`          | claim once then exit           |                         |
| `-a`, `--auto-update`   | enable auto update             |                         |
| `-u`, `--username`      | set username/email             | need to disable 2FA     |
| `-p`, `--password`      | set password                   | need to disable 2FA     |

## 简体中文

### 开始

``` bash
docker run -it luminoleon/epicgames-claimer
```

登录成功后，可按下Ctrl + P + Q切换至后台运行。

### 一些示例

* 保存账号信息到本地目录(下次创建新的容器时就不需要重新登录了):

    ```bash
    docker run -it -v ~/epicgames_claimer/User_Data:/User_Data luminoleon/epicgames-claimer
    ```

* 修复容器内的时区问题:

    ```bash
    docker run -it -e TZ=<你的时区> luminoleon/epicgames-claimer
    ```

    [可用时区列表](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones#List)

* 无交互式输入(需要关闭双重验证(2FA)):

    ```bash
    docker run -d luminoleon/epicgames-claimer -u <你的邮箱> -p <你的密码>
    ```

#### 环境变量

| 变量        | 说明                  | 默认   | 备注            |
| ----------- | -------------------- | ------ | -------------- |
| TZ          | 容器的时区, [可用时区列表](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones#List)         | Asia/Shanghai | |
| RUN_AT      | 指定每日运行时间      | 09:00 | 格式：HH:MM      |
| ONCE        | 运行一次领取过程后退出 | false | true/false      |
| AUTO_UPDATE | 启用自动更新          | false | true/false      |
| EMAIL       | 设置用户名/邮箱       |       | 需要关闭双重验证 |
| PASSWORD    | 设置密码              |       | 需要关闭双重验证 |

#### 可选参数

注意：对应的环境变量存在时，参数的值为会被对应环境变量的值覆盖。

使用方法: `docker run luminoleon/epicgames-claimer [-h] [-r RUN_AT] [-o] [-a] [-u USERNAME] [-p PASSWORD]`

| 参数                    | 说明                     | 备注            |
| ----------------------- | ----------------------- | --------------- |
| `-h`, `--help`          | 查看帮助信息             |                 |
| `-r`, `--run-at`        | 指定每日运行时间         | HH:MM，默认09:00 |
| `-o`, `--once`          | 运行一次领取过程后退出    |                 |
| `-a`, `--auto-update`   | 启用自动更新             |                 |
| `-u`, `--username`      | 设置用户名/邮箱          | 需要关闭双重验证  |
| `-p`, `--password`      | 设置密码                 | 需要关闭双重验证 |
