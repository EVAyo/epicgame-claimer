# EpicGames Claimer

[简体中文](README_ZH.md)

Claim [weekly free games](https://www.epicgames.com/store/free-games) from Epic Games Store.

If you think this project is helpful to you, please star this project.

## Start

### Windows

[Download](https://github.com/luminoleon/epicgames-claimer/releases)

#### Optional Arguments for Windows Version

See [Optional Arguments for Python Version](#optional-arguments-for-python-version).

### Docker

``` bash
docker run -it luminoleon/epicgames-claimer
```

After successful login, you can press Ctrl + P + Q to switch to the background.

#### Optional Arguments for Docker Version

| Arguments              | Descriptions                                                      |
|----------------------- | ----------------------------------------------------------------- |
| `-e TZ=<TimeZone>`     | set the time zone of the container(default: Asia/Shanghai, [Available Time Zones](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones#List))                         |
| `-v <Path>:/User_Data` | save the user data to the local path                              |
| `-e run_at=<Time>`     | set daily check and claim time(HH:MM, default: 09:00) |

### Python

Require Python >= 3.6.

``` bash
git clone -b master https://github.com/luminoleon/epicgames-claimer.git
cd epicgames-claimer
pip3 install -r requirements.txt
python3 epicgames_claimer.py
```

#### Optional Arguments for Python Version

| Arguments                                           | Descriptions                                      |
|---------------------------------------------------- | ------------------------------------------------- |
| `-h`, `--help`                                      | show the help message                             |
| `-hf`, `--headful`                                  | run Chromium in headful mode                      |
| `-c CHROMIUM_PATH`, `--chromium-path CHROMIUM_PATH` | set path to Chromium executable                   |
| `-r RUN_AT`, `--run-at RUN_AT`                      | set daily check and claim time(HH:MM, default: 08:30)                                                                                                    |
| `-o`, `--once`                                      | claim once then exit                              |

#### Notice

In Linux system, you should install Chrome or any other browser that use Chromium kernel, then add `--chromium-path` to set path to the browser executable.

For Debian-based Linux：

``` bash
curl -LO https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install -y ./google-chrome-stable_current_amd64.deb
rm google-chrome-stable_current_amd64.deb
python3 epicgames_claimer.py --chromium-path /usr/bin/google-chrome
```

For Redhat-based Linux：

``` bash
curl -LO https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm
sudo yum install -y ./google-chrome-stable_current_x86_64.rpm
rm -I google-chrome-stable_current_x86_64.rpm
python3 epicgames_claimer.py --chromium-path /usr/bin/google-chrome
```

## Known Issues

Stop the script midway in Windows system may cause the browser process remain in the background. You should check task manager and kill the browser process manually.
