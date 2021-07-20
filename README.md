# EpicGames Claimer

<!-- [START badges] -->

![](https://img.shields.io/badge/language-python-3572A5.svg) ![](https://img.shields.io/github/license/luminoleon/epicgames-claimer.svg) ![](https://img.shields.io/github/last-commit/luminoleon/epicgames-claimer.svg)

<!-- [END badges] -->

###### Other language: [简体中文](docs/README_ZH.md)

> Claim [weekly free games](https://www.epicgames.com/store/free-games) from Epic Games Store.

Very simple and easy to use. You almost don't need to input or modify any arguments, and it can automatically synchronize with the latest GitHub version.

If you think this project is helpful to you, please star this project.

## Getting Started

### Windows

[Download](https://github.com/luminoleon/epicgames-claimer/releases)

Notice: Windows version does not currently support automatic update.

#### Optional Arguments for Windows Version

| Arguments                 | Descriptions                                            |
| ------------------------- | ------------------------------------------------------- |
| `-h`, `--help`            | show the help message                                   |
| `-n`, `--no-headless`     | run the browser with GUI                                |
| `-c`, `--chromium-path`   | set path to browser executable                          |
| `-r`, `--run-at`          | set daily check and claim time(HH:MM, default to 09:00) |
| `-o`, `--once`            | claim once then exit                                    |

### Docker

``` bash
docker run -it luminoleon/epicgames-claimer
```

See [Docker hub page](https://hub.docker.com/r/luminoleon/epicgames-claimer) for more informations.

### Python

Require Python >= 3.6.

#### How to Install

1. Download

``` bash
git clone -b master https://github.com/luminoleon/epicgames-claimer.git
cd epicgames-claimer
```

2. Install Python Modules

``` bash
pip3 install -r requirements.txt
```

3. Install Dependencies(Linux Only)

``` bash
sudo sh install_dependencies.sh
```

4. Run

``` bash
python3 main.py
```

#### Optional Arguments for Python Version

| Arguments                 | Descriptions                                            |
| ------------------------- | ------------------------------------------------------- |
| `-h`, `--help`            | show the help message                                   |
| `-n`, `--no-headless`     | run the browser with GUI                                |
| `-c`, `--chromium-path`   | set path to browser executable                          |
| `-r`, `--run-at`          | set daily check and claim time(HH:MM, default to 09:00) |
| `-o`, `--once`            | claim once then exit                                    |
| `-na`, `--no-auto-update` | disable auto update                                     |

#### Notice

If the script runs incorrectly in Linux system, you can try to use Chrome instead of default Chromium(Refer to [Chrome headless doesn't launch on UNIX](https://github.com/puppeteer/puppeteer/blob/main/docs/troubleshooting.md#chrome-headless-doesnt-launch-on-unix)). The following commands may fix some problems.

##### Install Chrome

For Debian-based Linux:

``` bash
curl -LO https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install -y ./google-chrome-stable_current_amd64.deb
rm google-chrome-stable_current_amd64.deb
```

For Redhat-based Linux:

``` bash
curl -LO https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm
sudo yum install -y ./google-chrome-stable_current_x86_64.rpm
rm -I google-chrome-stable_current_x86_64.rpm
```

##### Set the path to Chrome

``` bash
python3 main.py --chromium-path /usr/bin/google-chrome
```

## Known Issues

Stop the script midway in Windows system may cause the browser process remain in the background. You should check task manager and kill the browser process manually.
