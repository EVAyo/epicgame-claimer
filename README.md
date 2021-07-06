# EpicGames Claimer

[简体中文](README_ZH.md)

Claim [weekly free games](https://www.epicgames.com/store/free-games) from Epic Games Store.

If you think this project is helpful to you, please star this project.

## Start

### Windows

[Download](https://github.com/luminoleon/epicgames-claimer/releases)

Notice: Windows version does not currently support automatic update.

#### Optional Arguments for Windows Version

See [Optional Arguments for Python Version](#optional-arguments-for-python-version).

### Docker

``` bash
docker run -it luminoleon/epicgames-claimer
```

See [Docker hub page](https://hub.docker.com/r/luminoleon/epicgames-claimer) for more informations.

### Python

Require Python >= 3.6.

``` bash
git clone -b master https://github.com/luminoleon/epicgames-claimer.git
cd epicgames-claimer
pip3 install -r requirements.txt
python3 epicgames_claimer_auto_update.py
```

#### Optional Arguments for Python Version

| Arguments                                           | Descriptions                                      |
|---------------------------------------------------- | ------------------------------------------------- |
| `-h`, `--help`                                      | show the help message                             |
| `-hf`, `--headful`                                  | run Chromium in headful mode                      |
| `-c CHROMIUM_PATH`, `--chromium-path CHROMIUM_PATH` | set path to Chromium executable                   |
| `-r RUN_AT`, `--run-at RUN_AT`                      | set daily check and claim time(HH:MM, default: 09:00)                                                                                                    |
| `-o`, `--once`                                      | claim once then exit                              |

#### Notice

In Linux system, you should install Chrome or any other browser that use Chromium kernel, then add `--chromium-path` to set path to the browser executable.

For Debian-based Linux:

``` bash
curl -LO https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install -y ./google-chrome-stable_current_amd64.deb
rm google-chrome-stable_current_amd64.deb
python3 epicgames_claimer_auto_update.py --chromium-path /usr/bin/google-chrome
```

For Redhat-based Linux:

``` bash
curl -LO https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm
sudo yum install -y ./google-chrome-stable_current_x86_64.rpm
rm -I google-chrome-stable_current_x86_64.rpm
python3 epicgames_claimer_auto_update.py --chromium-path /usr/bin/google-chrome
```

## Known Issues

Stop the script midway in Windows system may cause the browser process remain in the background. You should check task manager and kill the browser process manually.
