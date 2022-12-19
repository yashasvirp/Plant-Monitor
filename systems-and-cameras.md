
# Systems and Cameras


<a id="orgf129c98"></a>

## Raspberry Pi, Arduino, Jetson

We focus on Raspberry Pi, Jetson

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

**Alternatives**

-   Orange Pi
    -   More powerful hardware than Raspberry Pi
    -   Latest models not easily available in India
    -   Software not as stable as Raspberry Pi or Jetson
    -   See <https://www.tomshardware.com/reviews/orange-pi-4b> for a review
-   Banana Pi
    -   Similar hardware to Pi
    -   Sketchy software support


<a id="org6901a9c"></a>

## Interfacing with the System

-   Via Monitor<br/> We won't really do that
-   Headless via SSH
    -   Takes less resources
    -   Useful for production deployment


<a id="org8bcae5e"></a>

### Generating user/password for initial login (RPI)

1.  Put empty `ssh` file in `/boot` of SD Card<br/> `touch /mnt/<pi_dir>/boot/ssh`
2.  Create file `/boot/userconf.txt` with `username:encrypted-password`
    -   To generate encrypted password do:
        
        ```bash
        echo '<some_password>' | openssl passwd -6 -stdin
        ```
        
        Paste in `userconf.txt`


<a id="org0803938"></a>

### Connecting to via LAN (RPI, Jetson)

-   Simplest way to connect is via creating a shared connection on your computer and then directly connecting the LAN cable to the RPi
    -   With that your computer's internet will be shared with the RPi and you can not only login but install/update any packages or change any configurations
    -   The *shared* connection will assign an IP address in the range of `10.42.0.0/24`

-   To find the IP Address of your system you'll have to use `arp-scan`
    
    ```bash
    sudo arp-scan 10.42.0.0/24
    ```
    
    There will only be one system with an IP address.<br/> After that you can note down the WiFi MAC and use that to connect later.

-   Update the repos and install some packages which will come in handy later
    
    ```bash
    apt-get update
    # python libraries
    apt-get install -y python3-{pip,picamera2,ipython,ipdb,libcamera,flask,opencv,flask,smbus}\
            # useful tools
            file i2c-tools ncat git curl\
            # useful for compiling packages
            libopencv-dev\
            # useful in certain cases
            libraspberrypi0\
            # gstreamer stuff
            gstreamer1.0-opencv gstreamer1.0-plugins-{base,good}\
            # ffmpeg
            python3-prctl libatlas-base-dev ffmpeg libopenjp2-7
    ```

-   Sometimes you might get a certificate not valid error<br/> Do `date` in your computer and then paste in MC with `date -s <date>`

-   `raspi-config` (RPI)
    -   Disable serial console and enable `uart`
    -   Enable `SSH`
    -   Enable `I2C,SPI`

-   Automatic wait and connect script after reboot:<br/> `ip_addr=10.42.0.184; nc -z -v $ip_addr 22 -w .5 ; until [ $? -eq 0 ] ; do sleep 1s ; nc -z -v $ip_addr 22 -w .5 ; done ; ssh pi@$ip_addr`
    
    ```bash
    ip_addr=10.42.0.184
    nc -z -v $ip_addr 22 -w .5
    until [ $? -eq 0 ]
    do sleep 1s
       nc -z -v $ip_addr 22 -w .5
    done
    ssh pi@$ip_addr
    ```


<a id="orgf97faea"></a>

### Connecting with SSH keys (RPI, Jetson)

```bash
ssh-keygen
ssh-copy-id user@pi_addr
```

-   It is safer but more annoying to have password protected SSH keys.
-   You can also have multiple keys but we won't discuss that here.


<a id="org7158afe"></a>

## Configuration options (RPI)

-   `dtparam=i2c_arm=on`
-   `dtparam=i2c_vc=on`
-   `dtparam=spi=on`
-   `enable_uart=1`
-   `start_x=1`
-   `arm_64bit=1` If using 64-bit OS
-   `dt_overlay`


<a id="org7c9edf6"></a>

## Serial Communication (RPI)


<a id="org69be209"></a>

### The Raspberry Pi GPIO

![img](https://www.raspberrypi.com/documentation/computers/images/GPIO-Pinout-Diagram-2.png) `Source: https://www.raspberrypi.com/documentation/computers/images/GPIO-Pinout-Diagram-2.png` and <https://www.raspberrypi.com/documentation/computers/raspberry-pi.html>

See <https://www.raspberrypi.com/documentation/computers/raspberry-pi.html> for detailed documentation on hardware

In case of boot failures you can use the serial console to debug: See:<br/>

-   <https://raspberrypi.stackexchange.com/a/106921>
-   <https://www.jeffgeerling.com/blog/2021/attaching-raspberry-pis-serial-console-uart-debugging>
-   Also <https://www.raspberrypi.com/documentation/computers/raspberry-pi.html#boot-diagnostics-on-the-raspberry-pi-4>

But we'll disable the serial console and enable UART See <https://www.raspberrypi.com/documentation/computers/configuration.html#disabling-the-linux-serial-console>

For details on Raspberry Pi UART device tree, see:<br/> <https://www.raspberrypi.com/documentation/computers/configuration.html#uarts-and-device-tree>


<a id="orgd413bb5"></a>

### Jetson GPIO

We had a lot of trouble communicating with the Jetson GPIO that we had, so we decided to skip that entirely and use a USB to Serial module.


<a id="orge752265"></a>

### USB to Serial (RPI, Jetson)

The module that we found useful is a CP2102 USB to Serial converter. See <https://www.silabs.com/documents/public/data-sheets/CP2102-9.pdf> for the datasheet.

Essentially you can attach it to a free USB port and communicate via UART with the required sensor/driver/expansion board.


<a id="org06e380a"></a>

### I2C Communication

We don't have any modules with I2C so we won't discuss it.


<a id="org84ab84a"></a>

## Cameras with RPi (RPI)

-   Official RPi camera
    -   The current camera is V2 based on IMX-219 sensor
    -   Earlier one was phased out in 2016 and the "official" V1 cameras available in the market (based on OV5647 sensor) probably can't be relied upon
    -   Official cameras also includes an interchangeable lens camera for flexibility <https://www.raspberrypi.com/products/raspberry-pi-high-quality-camera/>
    -   Some other sensors like IMX-519 (available from arducam e.g.) are also supported natively with the current version of the OS
-   Arducam alternatives
    -   A crowdfunded startup which makes customized cameras for various applications
    -   Has various sensors with additional features like motorized focus
-   Other alternatives
    -   There are several other camera manufacturer alternatives for both RPI and Jetson


<a id="orgc131505"></a>

## Cameras with Jetson (Jetson)

RPi cameras will also work with Jetson in most cases

We could not get autofocus/motorized focus cameras to work with RPis but they work with Jetson. This is probably because of some differences from RPi 3 -> 4 device changes


<a id="org0146ffc"></a>

## Code


<a id="org3e39893"></a>

### Basic Image Processing with opencv (RPi, Jetson)

1.  Basic Numpy

    -   Numpy arrays are multidimensional C arrays with python wrappers that link with fast linear algebra backends
    -   Some operations are also parallelized

2.  Image Reading/Writing

    ```python
    import cv2 as cv
    
    img = cv.imread(img_file)
    cv.imshow("window name", img) # Exits immediately
    
    # wait 1000ms, if key not pressed move forward
    cv.imshow("window name", img)
    cv.waitKey(1000)
    cv.destroyWindow("window name")
    
    # wait indefinitely for key
    cv.imshow("window name", img)
    cv.waitKey(0)
    cv.destroyWindow("window name")
    
    # If destroyWindow not called, the window is left hanging there
    cv.imshow("window name", img)
    retval = cv.waitKey(0) # retval contains the unicode value of key pressed
    
    # Use this to exit all windows
    cv.destroyAllWindows()
    ```

3.  Basic Image Processing

    -   Let's write a simple show image function which also scales the image as required
        
        ```python
        import cv2 as cv
        
        def show_image(img, win_name="img", img_scale=1):
            display_img = cv.resize(img, (int(img.shape[1] * img_scale),
                                          int(img.shape[0] * img_scale)))
            cv.imshow(win_name, display_img)
            cv.waitKey(0)
            cv.destroyWindow(win_name)
        ```
    
    -   Show image and it's grayscale version side by side
        
        ```python
        import cv2 as cv
        
        def show_images(imgs, win_name="img", size=None):
            """:code:`imgs` can be alist of different kinds of imgs
        
            Args:
                imgs: List of images
                win_name: Display name of window
                size: display size of the window
        
            """
            display_imgs = []
            if size is None:
                height, width = np.array([[*x.shape[:2]] for x in imgs]).mean(0)
            else:
                width, height = size
            for img in imgs:
                if len(img.shape) == 2:
                    tmp = cv.cvtColor(img, cv.COLOR_GRAY2BGR)
                else:
                    tmp = img
                display_imgs.append(cv.resize(tmp, (int(width), int(height))))
            cv.imshow(win_name, np.hstack(display_imgs))
            cv.waitKey(0)
            cv.destroyWindow(win_name)
        ```
    
    -   Convert to HSV, threshold by intensity and show side by side
        
        ```python
        hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
        gray = hsv[:, : , -1]
        below_100 = (gray > 100) # is np.bool
        threshold = np.uint8(threshold) * 255
        show_images(img, threshold)
        ```


<a id="orgbeac41a"></a>

### Taking pictures and videos with libcamera (RPi)

-   Standard utilities for capture used to be `raspi*`
-   Now it's moved to libcamera
    
    ```bash
    libcamera-hello
    ```
    
    ```bash
    libcamera-jpeg -o test.jpg
    ```

-   Clone the repo to see the python interface
    
    ```bash
    git clone https://github.com/raspberrypi/picamera2
    cd picamera2/examples
    ```

-   First, `opencv` <br/> Useful functions:

-   Capture headless: `picamera2/examples/capture_headless.py`
    
    ```python
    from picamera2 import Picamera2
    
    picam2 = Picamera2()
    config = picam2.create_still_configuration()
    picam2.configure(config)
    
    picam2.start()
    
    np_array = picam2.capture_array()
    print(np_array)
    picam2.capture_file("demo.jpg")
    picam2.stop()
    ```

-   To see all functionality available use ipython
    
    ```python
    from picamera2 import Picamera2
    
    cam = Picamera2()
    print(cam.__dict__.keys())
    # OR
    dir(cam)
    
    # Then you can do e.g.
    cam.global_camera_info() # prints info of all attached cameras
    ```

-   Capturing video: `picamera2/examples/audio_video_capture.py`
    
    ```python
    import time
    
    from picamera2 import Picamera2
    from picamera2.encoders import H264Encoder
    from picamera2.outputs import FfmpegOutput
    
    picam2 = Picamera2()
    video_config = picam2.create_video_configuration()
    picam2.configure(video_config)
    
    encoder = H264Encoder(10000000)
    output = FfmpegOutput('test.mp4', audio=True)
    
    picam2.start_recording(encoder, output)
    time.sleep(10)
    picam2.stop_recording()
    ```


<a id="org8ae0f5c"></a>

### Taking pictures and videos with opencv (RPi, Jetson)

Opencv capture can be used with python and various backends.

-   This works in any laptop
    
    ```python
    import cv2 as cv
    
    cap = cv.VideoCapture("test.mp4")
    i = 0
    while cap.isOpened():
        status, frame = cap.read()
        if not status:
            break
        cv.imshow("frame", frame)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
        i += 1 # track frame count
    cv.destroyAllWindows()
    print(f"{i} frames read")
    cap.release()
    ```

-   We can make a small function of this
    
    ```python
    import cv2 as cv
    
    cap = cv.VideoCapture("test.mp4")
    
    def show_capture(cap, win_name="video"):
        i = 0
        try:
            while cap.isOpened():
                status, frame = cap.read()
                if not status:
                    break
                cv.imshow(win_name, frame)
                if cv.waitKey(1) & 0xFF == ord('q'):
                    break
                i += 1 # track frame count
        except Exception:
            cv.destroyAllWindows()
            print(f"{i} frames read")
            cap.release()
        cv.destroyAllWindows()
        print(f"{i} frames read")
        cap.release()
    
    show_capture(cap)
    ```

-   To capture default camera of laptop
    
    ```python
    import cv2 as cv
    
    cap = cv.VideoCapture(0)
    show_capture(cap)
    ```

-   For Opencv capture in RPi and Jetson capture with `gstreamer` it's a bit more complicated.<br/> We'll have to define a `gstreamer` pipeline and use that to capture the frames.<br/> There are separate arguments for `gstreamer` in RPi, Jetson and laptop
    
    ```python
    def jetson_pipeline(sensor_id=0, capture_width=1280, capture_height=720,
                        display_width=1280, display_height=720, flip_method=0):
        args = [f"nvarguscamerasrc sensor-id={sensor_id}",
                f"video/x-raw(memory:NVMM), width={int(capture_width)}, height={int(capture_height)},"
                " format=NV12",
                f"nvvidconv flip-method={int(flip_method)}",
                f"video/x-raw, width={int(display_width)}, height={int(display_height)}, format=BGRx",
                "videoconvert",
                "video/x-raw, format=BGR",
                "appsink"]
        return " ! ".join(args)
    
    
    def pi_pipeline(capture_width=1280, capture_height=720,
                    display_width=1280, display_height=720, flip_180=False):
        args = ["libcamerasrc",
                f"video/x-raw, width={int(capture_width)}, height={int(capture_height)}"]
        if flip_180:
            args.append("videoflip method=rotate-180")
        if capture_width != display_width or capture_height != display_height:
            args.append("videoscale")
            args.append(f"video/x-raw, width={int(display_width)}, height={int(display_height)}")
        args.append("appsink")
        return (" ! ".join(args))
    
    
    def laptop_pipeline(capture_width=1280, capture_height=720,
                    display_width=1280, display_height=720, flip_180=False):
        # leave params as default
        args = ["v4l2src device=/dev/video0", f"video/x-raw"]
        if flip_180:
            args.append("videoflip method=rotate-180")
        if capture_width != display_width or capture_height != display_height:
            args.append("videoscale")
            args.append(f"video/x-raw, width={int(display_width)}, height={int(display_height)}")
        args.append("appsink")
        return (" ! ".join(args))
    ```


<a id="org05fa660"></a>

### Basic Flask Service

```python
from flask import Flask
from werkzeug import serving

app = Flask()

@app.route("/ping")
def ping():
    return "pong"


# Binds on ALL IP addresses
# Accessible from networks, if no firewall is up
serving.run_simple("0.0.0.0", 8282, app)

# Runs on localhost only
# Not accessible outside the current system
serving.run_simple("127.0.0.1", 8282, app)
```


<a id="org97fda26"></a>

### Flask Service for Capturing and sending an image

-   Server
    
    ```python
    import sys
    import base64
    
    
    from flask import Flask
    from werkzeug import serving
    
    import cv2 as cv
    
    app = Flask()
    
    def capture_system():
        if cap.isOpened():
            return cv.VideoCapture(0) # for laptop
    
    def pi_capture(width, height):
        gp = "libcamerasrc ! video/x-raw, width=1280, height=720 ! appsink"
        cap = cv.videocapture(gp, cv.CAP_GSTREAMER)
        if cap.isOpened():
            return cap
    
    
    cap = capture_system()
    if not cap:
        sys.exit(1)
    
    
    @app.route("/ping")
    def ping():
        return "pong"
    
    
    @app.route("/capture")
    def capture():
        status, frame = cap.read()
        if status:
            return base64.b64encode(frame)
        else:
            return "Error"
    
    
    # Binds on ALL IP addresses
    # Accessible from networks, if no firewall is up
    serving.run_simple("0.0.0.0", 8282, app)
    ```

-   Simple Client
    
    ```python
    import base64
    
    import requests
    import numpy as np
    import cv2 as cv
    
    
    host = "localhost"
    port = 8282
    server = f"http://{host}:{port}"
    
    
    def get_capture():
        resp = requests.get(f"{server}/capture")
        content = resp.content
        if content.decode() != "Error":
            buf = np.frombuffer(base64.b64decode(resp.content), dtype=np.uint8)
            # Need to know the buffer shape
            buf = np.reshape(1080, 1920, 3)
            show_image(buf)
        else:
            print("Error")
    ```

-   Slightly more sophisticated client/server<br/> Only the client/server functions shown here
    
    ```python
    # Server function
    # Need json to serialize dictionary
    import json
    @app.route("/capture")
    def capture():
        status, frame = cap.read()
        if status:
            return json.dumps({"frame": base64.b64encode(frame).decode("utf8"),
                               "size": [*frame.shape]})
        else:
            return json.dumps({"frame": None, "size": None})
    
    
    # Client function
    def get_capture():
        resp = requests.get(f"{server}/capture")
        content = resp.json()
        if content["frame"] is not None:
            buf = np.frombuffer(base64.b64decode(content["frame"]), dtype=np.uint8)
            buf = buf.reshape(content["size"])
            show_image(buf)
        else:
            print("Error")
    ```