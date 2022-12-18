
# Motors and Control

-   Kinds of Motors you'll commonly see
    -   Brushed DC motors
    -   Brushless DC motors
    -   DC Motors with encoders
    -   Stepper motors
    -   Servo motors
    -   Hybrid motors

A useful article giving an overview of various motors <https://www.instructables.com/Complete-Motor-Guide-for-Robotics/>


<a id="org2ddc4fe"></a>

## Servo Motors

-   Kinds of Servos
    -   Digital, Analog
    -   Metal Gear, Plastic Gear
    -   Torque

<https://www.sparkfun.com/servos>


<a id="org2ba7d51"></a>

### What's in a servo motor anyway?

**TODO**


<a id="org325e86c"></a>

## PWM

-   Basics of PWM
    -   Hardware vs Software PWM
-   How a driver interacts with servos


<a id="org501b1f6"></a>

## Powering the Servos

-   Depends on the maximum current draw
-   Small servos can be directly connected to the Raspberry Pi
-   Raspberry pi doesn't have a hardware PWM so the control from Pi and from a hardware driver varies
-   Larger servos need an SMPS
-   Connecting SMPS
-   Voltage converters
-   Using the multimeters


<a id="orgc8d8ced"></a>

## DC Motors

-   **TODO**


<a id="org3c444f1"></a>

## Services and messages

-   [X] Flask as a simple service manager
-   [ ] Passing messages


<a id="orgf476675"></a>

### I2C, UART and SPI

-   <https://www.totalphase.com/blog/2020/12/differences-between-uart-i2c/>
-   <https://www.seeedstudio.com/blog/2019/09/25/uart-vs-i2c-vs-spi-communication-protocols-and-uses/>


<a id="org68b7efa"></a>

## SC08A

-   UART based 8 channel Servo Motor Controller
-   User Manual: <https://robu.in/wp-content/uploads/2016/02/SC08A_Users_Manual.pdf> [/home/joe/projects/tomato<sub>robot</sub>/servo-codes/SC08A<sub>Users</sub><sub>Manual.pdf</sub>](file:///home/joe/projects/tomato_robot/servo-codes/SC08A_Users_Manual.pdf)
-   **Features**
    -   Get/Set position of multiple servos per command
    -   Allows to set speed in a single command


<a id="org2a64689"></a>

## CH342

-   USB/UART based 32 channel Servo Motor Controller
-   Datasheet: [/home/joe/Downloads/CH343DS1.PDF](file:///home/joe/Downloads/CH343DS1.PDF)
-   Manual: [/home/joe/Downloads/42303/Manual.pdf](file:///home/joe/Downloads/42303/Manual.pdf)
-   Driver: [/home/joe/Downloads/CH341SER<sub>LINUX.ZIP</sub>](file:///home/joe/Downloads/CH341SER_LINUX.ZIP)
-   **Features**
    -   **Set position only** of multiple servos per command
    -   Allows to set speed in a single command


<a id="org1177edc"></a>

## Code


<a id="org20c7d6a"></a>

### SC08A

1.  Intializing the controller

2.  Controller properties


<a id="org4800c4f"></a>

### Controlling the servos over the network

-   Fetching things over the network Python `requests` module
    
    ```python
    
    ```
-   Sending things over the network `Flask` package
    
    ```python
    
    ```
-   Combining the two with a client/server mechanism
-   Integrating the servo control