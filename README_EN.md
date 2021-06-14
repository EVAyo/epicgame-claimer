# Epic Games Claimer

Claim [weekly free games](https://www.epicgames.com/store/free-games) from Epic Games Store.

## Start

### Windows

[Download](https://github.com/luminoleon/epicgames-claimer/releases)

#### Optional Arguments of Windows Version

See [Optional Arguments of Python Version](#Optional-Arguments-of-Python-Version).

### Docker

``` bash
docker run -it luminoleon/epicgames-claimer
```

After successful login, you can press Ctrl + P + Q to switch to the background.

#### Optional Arguments of Docker Version

| Arguments              | Descriptions                                      |
|----------------------- | ------------------------------------------------- |
| `-e TZ=<TimeZone>`     | set the time zone of the container(Default: Asia/Shanghai, [Available Time Zones](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones#List))         |
| `-v <Path>:/User_Data` | save the user data to the local path              |
| `-e run_at=<Time>`     | set daily check and claim time(HH:MM, e.g. 08:30) |

### Python

Require Python >= 3.6.

``` bash
git clone https://github.com/luminoleon/epicgames-claimer.git
cd epicgames-claimer
pip3 install -r requirements.txt
python3 epicgames_claimer.py
```

#### Optional Arguments of Python Version

| Arguments                                           | Descriptions                                      |
|---------------------------------------------------- | ------------------------------------------------- |
| `-h`, `--help`                                      | show the help message                             |
| `-hf`, `--headful`                                  | run Chromium in headful mode                      |
| `-c CHROMIUM_PATH`, `--chromium-path CHROMIUM_PATH` | set Chromium executable path                      |
| `-r RUN_AT`, `--run-at RUN_AT`                      | set daily check and claim time(HH:MM, e.g. 08:30) |
| `-o`, `--once`                                      | claim once then exit                              |

#### Notice

You should install the dependencies of Chromium in Linux.

For Ubuntu:

``` bash
sudo apt install gconf-service libasound2 libatk1.0-0 libatk-bridge2.0-0 libc6 libcairo2 libcups2 libdbus-1-3 libexpat1 libfontconfig1 libgcc1 libgconf-2-4 libgdk-pixbuf2.0-0 libglib2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libpangocairo-1.0-0 libstdc++6 libx11-6 libx11-xcb1 libxcb1 libxcomposite1 libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 libxss1 libxtst6 ca-certificates fonts-liberation libappindicator1 libnss3 lsb-release xdg-utils wget
```

Or you can install any browser that uses Chromium kernel.

``` bash
curl -LO https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install -y google-chrome-stable_current_amd64.deb
rm google-chrome-stable_current_amd64.deb
python3 epicgames_claimer.py --chromium-path /usr/bin/google-chrome
```
