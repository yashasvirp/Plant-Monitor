
# Motors and Control

-   Kinds of Motors you'll commonly see
    -   Brushed DC motors
    -   Brushless DC motors
    -   DC Motors with encoders
    -   Stepper motors
    -   Servo motors
    -   Hybrid motors

A useful article giving an overview of various motors <https://www.instructables.com/Complete-Motor-Guide-for-Robotics/>


<a id="orgd58bc5e"></a>

## Servo Motors

-   Kinds of Servos
    -   Digital, Analog
    -   Metal Gear, Plastic Gear
    -   Torque

<https://www.sparkfun.com/servos>


<a id="orgd18b846"></a>

### What's in a servo motor anyway?

**TODO**


<a id="orgb6f199a"></a>

## PWM

-   Basics of PWM
    -   Hardware vs Software PWM
-   How a driver interacts with servos


<a id="org8d0229e"></a>

## Powering the Servos

-   Depends on the maximum current draw
-   Small servos can be directly connected to the Raspberry Pi
-   Raspberry pi doesn't have a hardware PWM so the control from Pi and from a hardware driver varies
-   Larger servos need an SMPS
-   Connecting SMPS
-   Voltage converters
-   Using the multimeters


<a id="org651da6e"></a>

### I2C, UART and SPI

-   <https://www.totalphase.com/blog/2020/12/differences-between-uart-i2c/>
-   <https://www.seeedstudio.com/blog/2019/09/25/uart-vs-i2c-vs-spi-communication-protocols-and-uses/>


<a id="org998057a"></a>

## SC08A

-   UART based 8 channel Servo Motor Controller
-   User Manual: <https://robu.in/wp-content/uploads/2016/02/SC08A_Users_Manual.pdf> [/home/joe/projects/tomato<sub>robot</sub>/servo-codes/SC08A<sub>Users</sub><sub>Manual.pdf</sub>](file:///home/joe/projects/tomato_robot/servo-codes/SC08A_Users_Manual.pdf)
-   **Features**
    -   Get/Set position of multiple servos per command
    -   Allows to set speed in a single command
-   See <https://github.com/uoh-robotics/workshop-2022/tree/main/code/sc08a>


<a id="orgdacfd22"></a>

## CH342

-   USB/UART based 32 channel Servo Motor Controller
-   Datasheet: [/home/joe/Downloads/CH343DS1.PDF](file:///home/joe/Downloads/CH343DS1.PDF)
-   Manual: [/home/joe/Downloads/42303/Manual.pdf](file:///home/joe/Downloads/42303/Manual.pdf)
-   Driver: [/home/joe/Downloads/CH341SER<sub>LINUX.ZIP</sub>](file:///home/joe/Downloads/CH341SER_LINUX.ZIP)
-   **Features**
    -   **Set position only** of multiple servos per command
    -   Allows to set speed in a single command


<a id="org1537673"></a>

## Code


<a id="orgda042b2"></a>

### SC08A

1.  Intializing the controller

    -   Initialize the port
        
        ```python
        import serial
        
        # sudo chmod 777 /dev/ttyUSB0
        portname = "/dev/ttyUSB0" # substitute port for the name
        baudrate = 9600
        # Initialize serial port
        port = serial.Serial(portname, baudrate, timeout=0.1, write_timeout=0.1)
        ```
        
        In Raspberry Pi, if not using CP2102, port will be `/dev/ttyS0`
    
    -   Turn motors on/off
        
        ```python
        channels = 1
        first_byte = 0b11000000 | channels
        # turn motors in channels on
        port.write(bytes([first_byte, 1])) # 0 for off, 1 for on
        ```

2.  Controller properties

    -   Read motor position
        
        ```python
        channel = 1 # substitute with channel number
        port.write(bytes([0b10100000 | channel]))
        high, low = port.read(2)
        print(int(bin(0b10000000 | high)[3:] + bin(0b1000000 | low)[3:], 2))
        ```


<a id="orga0e2d96"></a>

### Controlling the servos over the network

**Following Covered in addendem to previous topic**

-   Fetching things over the network
-   Sending things over the network `Flask` package
-   Combining the two with a client/server mechanism