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

#### Optional Arguments

| Arguments               | Descriptions                                                    |
|------------------------ | --------------------------------------------------------------- |
| `-e TZ=<TimeZone>`      | set the time zone of the container(default to Asia/Shanghai, [Available Time Zones](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones#List))                                 |
| `-v <Path>:/User_Data`  | save the user data to the local path(must be full path)         |
| `-e run_at=<Time>`      | set daily check and claim time(HH:MM, default to 09:00)         |
| `-e auto_update=<Bool>` | enable or disable automatic update(true/false, default to true) |

## 简体中文

### 开始

``` bash
docker run -it luminoleon/epicgames-claimer
```

登录成功后，可按下Ctrl + P + Q切换至后台运行。

#### 可选参数

| 参数                    | 说明                                                    |
|------------------------ | ------------------------------------------------------ |
| `-e TZ=<TimeZone>`      | 设定容器的时区信息（默认Asia/Shanghai，[可用时区列表](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones#List)）                                             |
| `-v <Path>:/User_Data`  | 保存用户数据至本机路径（必须是完整路径）                   |
| `-e run_at=<Time>`      | 设定每日运行时间（HH:MM， 默认09:00）                    |
| `-e auto_update=<bool>` | 启用或关闭自动更新(true/false, default: false)          |
