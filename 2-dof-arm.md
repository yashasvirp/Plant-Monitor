
# 2 DOF arm


<a id="orgcf7ff86"></a>

## Building a 2DOF robot arm with camera

-   By now we have constructed a 2DOF robotic arm
-   The next task would be to track a red ball manually
-   After that program the arm to track it based on distance from the red ball


<a id="org2ebe9b0"></a>

## Tracking a red object manually

We have the following components:

-   [X] Streaming service and client
-   [X] Keyboard driven control of arm

We need the following to complete the task:

-   [ ] Segmentation and contouring
-   [ ] Find the center of the object
-   [ ] Drawing the object
-   [ ] Object tracking


<a id="orgd28b66f"></a>

### Object detection of a specific color with opencv (RPi, Jetson)

-   Capture image from camera
-   Convert to HSV
-   Detect in image
-   Draw bounding box around it


<a id="org663fc45"></a>

### Streaming Video/image streams over the network

-   Approach 1<br/> Use `TCP` with `picamera2`
-   Approach 2<br/> Use `HTTP` streaming with `ffmpeg`
-   Approach 3<br/> Use `HTTP` service with frames on demand with `gstreamer+OpenCV` capture
-   Approach 3.1<br/> Use `HTTP` service with frames on demand with a separate thread for bufferless capture with `gstreamer+OpenCV`