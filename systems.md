
# Systems


<a id="orga75af21"></a>

## Raspberry Pi, Arduino, Jetson

We focus on Pi, Jetson

-   **Raspberry Pi 4 Model B**:
    -   Has a quad core ARM processor
    -   4 GB RAM
    -   FFC cables for connecting camera and display
    -   Various other standard peripheral connection ports like USB, mini-HDMI, ethernet
    -   Has built in Wi-Fi

-   **Jetson Nano**:
    -   Has also a quad core AMR processor
    -   2/4 GB RAM
    -   FFC cables for connecting **2 cameras**
    -   Standard HDMI cable for connecting to display
    -   Number of USB and other ports depends on the carrier board

-   **Key points**:
    -   Jetson Runs on a version of ubuntu, while RPi runs on an OS derived from Debian.
    -   **Nano is no longer supported with newer versions of OS from Nvidia**
    -   Jetson contains an integrated GP-GPU with a small number *CUDA cores* which varies according to the variant of Jetson being used
    -   Rest of the interface is pretty much similar


<a id="org20a8940"></a>

## Interfacing with Pi

-   Via Monitor<br/> We won't really do that
-   Headless via SSH
    -   Takes less resources
    -   Useful for production deployment


<a id="org05ca481"></a>

### Generating user/password for initial login

1.  Put empty `ssh` file in `/boot` of SD Card<br/> `touch /mnt/<pi_dir>/boot/ssh`
2.  Create file `/boot/userconf.txt` with `username:encrypted-password`
    -   To generate encrypted password do:
        
        ```bash
        echo '<some_password>' | openssl passwd -6 -stdin
        ```
        
        Paste in `userconf.txt`


<a id="org9aa6313"></a>

### Connecting to RPi via LAN

-   Simplest way to connect is via creating a shared connection on your computer and then directly connecting the LAN cable to the RPi
    -   With that your computer's internet will be shared with the RPi and you can not only login but install/update any packages or change any configurations
    -   The *shared* connection will assign an IP address in the range of `10.42.0.0/24`

-   To find the IP Address of your RPi you'll have to use `arp-scan`
    
    ```bash
    sudo arp-scan 10.42.0.0/24
    ```
    
    There will only be one system with an IP address.<br/> After that you can note down the WiFi MAC and use that to connect later.

-   Update the repos and install some packages which will come in handy later
    
    ```bash
    apt-get install -y python3-{pip,picamera2,ipython,libcamera,flask,opencv,flask}\
            gstreamer1.0-opencv libopencv-dev libraspberrypi0 file i2c-tools ncat git curl
    ```

-   `raspi-config`
    -   Disable serial console and enable `uart`
    -   Enable `SSH`
    -   Enable `I2C,SPI`

-   Automatic wait and connect script:<br/> `ip_addr=10.42.0.184; nc -z -v $ip_addr 22 -w .5 ; until [ $? -eq 0 ] ; do sleep 1s ; nc -z -v $ip_addr 22 -w .5 ; done ; ssh pi@$ip_addr`
    
    ```bash
    ip_addr=10.42.0.184
    nc -z -v $ip_addr 22 -w .5
    until [ $? -eq 0 ]
    do sleep 1s
       nc -z -v $ip_addr 22 -w .5
    done
    ssh pi@$ip_addr
    ```


<a id="org2aba0f0"></a>

### Connecting with SSH keys

```bash
ssh-keygen
ssh-copy-id user@pi_addr
```

-   It is safer but more annoying to have password protected SSH keys.
-   You can also have multiple keys but we won't discuss that here.


<a id="orga2f4acc"></a>

## Configuration options

-   `dtparam=i2c_arm=on`
-   `dtparam=i2c_vc=on`
-   `dtparam=spi=on`
-   `enable_uart=1`
-   `start_x=1`
-   `arm_64bit=1` If using 64-bit OS
-   `dt_overlay`


<a id="org9625d2f"></a>

## Running Headless


<a id="org25cd418"></a>

## GPIO, Serial, UART


<a id="org712d84c"></a>

## Servos and Cameras with Pi

-   [X] Official RPi cameras
-   [X] Arducam alternatives
-   [X] Basics of Servo Motors


<a id="org8753ecd"></a>

## Practical


<a id="org83190f3"></a>

### Taking pictures and videos with libcamera


<a id="orgceda4ad"></a>

### Taking pictures and videos with opencv where supported


<a id="orgd20b78f"></a>

### Some small image transformations with opencv


<a id="org0fc6b56"></a>

### Object tracking of a specific color with opencv