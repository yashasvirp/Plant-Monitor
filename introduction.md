
# Introduction


<a id="org3948d8a"></a>

## IoE Workshop on Practical Robotics

Funding under IoE grant `UoH-IoE-RC3-21-050`

The aim is to get people started on building small practical robots with DIY parts available off the shelf.

We'll focus on Computing Systems, DC/Servo Motors and Cameras for building such robots.

At the end of the workshop the users should feel confident in conducint such experiments themselves.


<a id="orgd834050"></a>

## What is Robotics

-   What is a robot?
    -   It must have a mechanical component, in that it must be able to move and/or effect external physical phenomenon.
-   Robots have been around for a while especially in industrial automation.
-   Industrial robots are historically not autonomous and move in pre-determined and efficient manner.
-   **Autonomous Robots** on the other hand can move/effect in stochastic manner based on stimulus
-   In that sense, stimulus is crucial to Autonomous Robots as their decisions are based on how they sense their environment


<a id="org0e07dd0"></a>

## Practical Robotics

-   In this workshop we're going to consider only two modalities of stimulus:
    1.  Position
    2.  Vision
-   Position would be the position of the robot's components
-   Vision could be surrounding environment captured by one or more cameras
-   We'll only deal with a single camera but in practice multiple cameras or sensors can be used.
-   Some common sensors for modeling the environment are:
    -   IR and LiDAR sensors for disance
    -   IR sensors for night vision
    -   Binocular cameras for 3D reconstruction of environment
    -   Accelerometer for sensing movement
    -   Pressure sensors for sensing touch
    -   Piezoelectric sensors for vibration