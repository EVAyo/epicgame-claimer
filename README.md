# EpicGames Claimer

<!-- [START badges] -->

![](https://img.shields.io/badge/language-python-3572A5.svg) ![](https://img.shields.io/github/license/luminoleon/epicgames-claimer.svg) ![](https://img.shields.io/github/last-commit/luminoleon/epicgames-claimer.svg)

<!-- [END badges] -->

###### Other language: [简体中文](docs/README_ZH.md)

> Claim [weekly free games](https://www.epicgames.com/store/free-games) from Epic Games Store.

It's very simple and easy to use. In most cases, you don't need to input or modify any arguments, and it automatically synchronizes with the latest GitHub version.

If you think this project is helpful to you, please star this project.

## Getting Started

### Windows

[Download](https://github.com/luminoleon/epicgames-claimer/releases)

Notice: Windows version does not currently support automatic update.

#### Optional Arguments for Windows Version

| Arguments                 | Descriptions                   | Note                    |
| ------------------------- | -------------------------------|------------------------ |
| `-h`, `--help`            | show the help message          |                         |
| `-n`, `--no-headless`     | run the browser with GUI       |                         |
| `-c`, `--chromium-path`   | set path to browser executable |                         |
| `-r`, `--run-at`          | set daily check and claim time | HH:MM, default to 09:00 |
| `-o`, `--once`            | claim once then exit           |                         |
| `-u`, `--username`        | set username/email             | need to disable 2FA     |
| `-p`, `--password`        | set password                   | need to disable 2FA     |

### Docker

``` bash
docker run -it luminoleon/epicgames-claimer
```

See [Docker hub page](https://hub.docker.com/r/luminoleon/epicgames-claimer) for more informations.

### Python

Require Python >= 3.6.

#### How to Use

1. Clone/[Download](https://github.com/luminoleon/epicgames-claimer/releases)

    ``` bash
    git clone -b master https://github.com/luminoleon/epicgames-claimer.git
    cd epicgames-claimer
    ```

2. Install Python modules

    ``` bash
    pip3 install -r requirements.txt
    ```

3. Install dependencies(Linux only)

    ``` bash
    sudo sh install_dependencies.sh
    ```

4. Run

    ``` bash
    python3 main.py
    ```

    <details>
    <summary>Enable auto update</summary>

    ```bash
    python3 main.py --auto-update
    ```

    </details>

    <details>
    <summary>No interactive input(Need to disable two-factor authentication(2FA))</summary>

    ```bash
    python3 main.py -u <YOUR EMAIL> -p <YOUR PASSWORD>
    ```

    </details>

#### Optional Arguments for Python Version

| Arguments               | Descriptions                   | Note                    |
| ----------------------- | ------------------------------ | ----------------------- |
| `-h`, `--help`          | show the help message          |                         |
| `-n`, `--no-headless`   | run the browser with GUI       |                         |
| `-c`, `--chromium-path` | set path to browser executable |                         |
| `-r`, `--run-at`        | set daily check and claim time | HH:MM, default to 09:00 |
| `-o`, `--once`          | claim once then exit           |                         |
| `-a`, `--auto-update`   | enable auto update             |                         |
| `-u`, `--username`      | set username/email             | need to disable 2FA     |
| `-p`, `--password`      | set password                   | need to disable 2FA     |

#### Notice

If the script runs incorrectly in Linux, you can try to use Chrome instead of default Chromium(Refer to [Chrome headless doesn't launch on UNIX](https://github.com/puppeteer/puppeteer/blob/main/docs/troubleshooting.md#chrome-headless-doesnt-launch-on-unix)). The following commands may fix some problems.

##### Install Chrome(AMD64)

<details>
<summary>Debian (e.g. Ubuntu)</summary>

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

##### Use Chrome instead of default browser

``` bash
python3 main.py --chromium-path /usr/bin/google-chrome
```

## Known Issues

Stopping the script midway in Windows may cause the browser process remain in the background. You should check task manager and kill the browser process manually.
