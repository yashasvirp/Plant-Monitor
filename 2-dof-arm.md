
# 2 DOF arm


<a id="orge1c2bc7"></a>

## Building a 2DOF robot arm with camera

-   By now we have constructed a 2DOF robotic arm
-   The next task would be to track a red ball manually
-   After that program the arm to track it based on distance from the red ball


<a id="orgec5fd6b"></a>

## Tracking a red object manually

We have the following components:

-   [X] Streaming service and client
-   [X] Keyboard driven control of arm

We need the following to complete the task:

-   Bufferless video capture
    
    ```python
    # Bufferless VideoCapture
    # Adapted from https://stackoverflow.com/a/54577746/16723964
    class VideoCapture:
        def __init__(self, pipeline, cap_type):
            self._cap = cv.VideoCapture(pipeline, cap_type)
            self.q = Queue()
            self._reader_thread = Thread(target=self._reader)
            self._reader_thread.start()
            self._should_read = Event()
            self._should_read.set()
    
        # read frames as soon as they are available, keeping only most recent one
        def _reader(self):
            while self._should_read.is_set():
                ret, frame = self._cap.read()
                if not ret:
                    break
                if not self.q.empty():
                    try:
                        self.q.get_nowait() # discard previous (unprocessed) frame
                    except Queue.Empty:
                        pass
                self.q.put(frame)
    
        def stop(self):
            self._should_read.clear()
            self._reader_thread.join()
            self._cap.release()
    
        def isOpened(self):
            return self._should_read.is_set()
    
        def release(self):
            self.stop()
    
        def read(self):
            if self._should_read.is_set():
                return True, self.q.get()
            else:
                return False, None
    ```
-   Faster image transfer with jpeg encoding
    
    ```python
    def get_frame():
        status, img = cap.read()
        status, buf = cv.imencode(".jpg", img)
        data = base64.b64encode(buf)
        return data
    ```
-   Segmentation and contouring<br/> Segment the image and find contours of red object
    
    ```python
    def get_contours_and_mask_hsv(img, low_val=[163, 74, 30],
                                  high_val=[179, 255, 255]):
        hsv_img = cv.cvtColor(img, cv.COLOR_BGR2HSV)
        mask = cv.inRange(hsv_img, low_val, high_val)
        mask = cv.erode(mask, np.ones((5, 5), dtype='uint8'), iterations=1)
        contours, _ = cv.findContours(mask, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
        return contours, mask
    ```
    
    Draw the bounding rectangle for the contours
    
    ```python
    def draw_bounding_rect_for_contour(contour, img):
        (x, y, w, h) = cv.boundingRect(contour)
        # Getting Position of rectangle & line colour & thickness
        cv.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    ```
-   Find the center of the object
    
    ```python
    def get_midpoints(contour):
        (x, y, w, h) = cv.boundingRect(contour)
        # Checking horizontal center of red object & save to variable
        x_mid = int((x + x + w) / 2)
        # Checking Vertical center of red object & save to variable
        y_mid = int((y + y + h) / 2)
        return x_mid, y_mid
    ```
-   [ ] Object tracking


<a id="org8044c78"></a>

### Object detection of a specific color with opencv (RPi, Jetson)

-   Capture image from camera
-   Convert to HSV
-   Detect in image
-   Draw bounding box around it


<a id="orgcc68423"></a>

### Streaming Video/image streams over the network

-   Approach 1<br/> Use `TCP` with `picamera2`
-   Approach 2<br/> Use `HTTP` streaming with `ffmpeg`
-   Approach 3<br/> Use `HTTP` service with frames on demand with `gstreamer+OpenCV` capture
-   Approach 3.1<br/> Use `HTTP` service with frames on demand with a separate thread for bufferless capture with `gstreamer+OpenCV`