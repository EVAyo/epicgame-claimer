# Troubleshooting

* [Browser closed unexpectedly](#browser-closed-unexpectedly)
* [Running on small memory or ARM devices](#running-on-small-memory-or-arm-devices)

## Browser closed unexpectedly

You can try to use Google Chrome instead of default Chromium. This may solve some problems (Refer to [Chrome headless doesn't launch on UNIX](https://github.com/puppeteer/puppeteer/blob/main/docs/troubleshooting.md#chrome-headless-doesnt-launch-on-unix)).

1. Installing Google Chrome (AMD64)

    * Debian (e.g. Ubuntu)

        ``` bash
        curl -LO https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
        sudo apt install -y ./google-chrome-stable_current_amd64.deb
        rm google-chrome-stable_current_amd64.deb
        ```

    * CentOS

        ``` bash
        curl -LO https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm
        sudo yum install -y ./google-chrome-stable_current_x86_64.rpm
        rm -I google-chrome-stable_current_x86_64.rpm
        ```

2. Setting browser executable

    ``` bash
    python3 main.py --chromium-path /usr/bin/google-chrome
    ```

## Running on small memory or ARM devices

1. Installing Chromium

    * Debian (e.g. Ubuntu)

        ``` bash
        sudo apt install chromium-browser
        ```

    * CentOS

        ``` bash
        sudo yum install -y epel-release
        sudo yum install -y chromium
        ```

2. Setting browser executable

    ``` bash
    python3 main.py --chromium-path chromium-browser
    ```
