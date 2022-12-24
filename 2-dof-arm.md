
# 2 DOF arm


<a id="orgbaee1ee"></a>

## Building a 2DOF robot arm with camera

-   By now we have constructed a 2DOF robotic arm
-   The next task would be to track a red ball manually
-   After that program the arm to track it based on distance from the red ball


<a id="org19b2033"></a>

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
            self._should_read = Event()
            self._should_read.set()
            self._reader_thread = Thread(target=self._reader)
            self._reader_thread.start()
    
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
-   Local red object detect and view
    
    ```python
    import argparse
    
    import numpy as np
    import cv2 as cv
    
    
    def gstreamer_pipeline(width=512, height=512, flip_180=False):
        args = ["libcamerasrc", f"video/x-raw, width={width}, height={height}"]
        if flip_180:
            args.append("videoflip method=rotate-180")
        args.append("appsink")
        return (" ! ".join(args))
    
    
    def calc_pos(x_pos, y_pos, x_mid, y_mid, x_center, y_center, x_band, y_band):
        if x_mid < x_center - x_band:
            x_pos -= 1
        elif x_mid > x_center + x_band:
            x_pos += 1
    
        if y_mid < y_center - y_band:
            y_pos -= 1
        elif y_mid > y_center + y_band:
            y_pos += 1
    
        if x_pos >= 180:
            x_pos = 180
        elif x_pos <= 0:
            x_pos = 0
        else:
            x_pos = x_pos
        if y_pos >= 180:
            y_pos = 180
        elif y_pos <= 0:
            y_pos = 0
        else:
            y_pos = y_pos
        return x_pos, y_pos
    
    
    def draw_bounding_rect_for_contour(contour, img):
        (x, y, w, h) = cv.boundingRect(contour)
        # Getting Position of rectangle & line colour & thickness
        cv.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
    
    def get_midpoints(contour):
        (x, y, w, h) = cv.boundingRect(contour)
        # Checking horizontal center of red object & save to variable
        x_mid = int((x + x + w) / 2)
        # Checking Vertical center of red object & save to variable
        y_mid = int((y + y + h) / 2)
        return x_mid, y_mid
    
    
    def show_image(img, name=None, img_scale=1):
        display_img = cv.resize(img, (img.shape[1] // img_scale,
                                      img.shape[0] // img_scale))
        if not name:
            name = "img"
        cv.imshow(name, display_img)
        cv.waitKey(0)
        cv.destroyWindow(name)
    
    
    def get_contours_and_mask_hsv(img, low_val=[163, 74, 30],
                                  high_val=[179, 255, 255]):
        hsv_img = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    
        # low_red = np.array([163, 74, 30])
        # high_red = np.array([179, 255, 255])
    
        mask = cv.inRange(hsv_img, low_val, high_val)
        mask = cv.erode(mask, np.ones((5, 5), dtype='uint8'), iterations=1)
        # red = cv.bitwise_and(frame, frame, mask=red_mask)
    
        contours, _ = cv.findContours(mask, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
        return contours, mask
    
    
    def get_contours_and_mask_bgr(img, low_val, high_val):
        mask = cv.inRange(img, low_val, high_val)
        contours, _ = cv.findContours(mask, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
        return contours, mask
    
    
    def main(width, height, low_val, high_val):
        # _gst_pipeline = gstreamer_pipeline(width, height, flip_180=True)
        # cap = cv.VideoCapture(_gst_pipeline, cv.CAP_GSTREAMER)
    
        # NOTE: Capture directly from laptop camera
        cap = cv.VideoCapture(0)
    
        status, frame = cap.read()
        rows, cols, ch = frame.shape
        x_mid = int(cols / 2)
        y_mid = int(rows / 2)
    
        x_center = int(cols / 2)
        y_center = int(rows / 2)
    
        x_pos = 90
        y_pos = 90
    
        x_band = 50
        y_band = 50
    
        while status:
            frame = cv.flip(frame, 1)
            # contours, mask = get_contours_and_mask_bgr(frame, low_val, high_val)
            contours, mask = get_contours_and_mask_hsv(frame, low_val, high_val)
    
            if not len(contours):
                print("No contour found")
                status, frame = cap.read()
                continue
            areas = [cv.contourArea(x) for x in contours]
            sorted_inds = np.argsort(areas)
            max_area_contour = contours[sorted_inds[-1]]
            # img = frame.copy()
    
            draw_bounding_rect_for_contour(max_area_contour, frame)
    
            x_mid, y_mid = get_midpoints(max_area_contour)
    
            # Draw horizontal centre line of red object
            cv.line(frame, (x_mid, 0), (x_mid, height), (0, 255, 0), 2)
            # Draw Vertical centre line of red object
            cv.line(frame, (0, y_mid), (width, y_mid), (0, 255, 0), 2)
            img = np.hstack([frame, np.repeat(mask, 3).reshape(*mask.shape, 3)])
            cv.imshow("IN Frame", img)
    
            x_pos, y_pos = calc_pos(x_pos, y_pos, x_mid, y_mid,
                                    x_center, y_center, x_band, y_band)
            print(f"X, Y: ({x_pos}, {y_pos})")
    
            key = cv.waitKey(1)
            if key == ord('q'):
                break
            status, frame = cap.read()
    
    
        cv.destroyAllWindows()
        cap.release()
    
    
    if __name__ == '__main__':
        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument("-h", "--height", type=int, default=320)
        parser.add_argument("-w", "--width", type=int, default=480)
        parser.add_argument("-lv", "--low-val")
        parser.add_argument("-hv", "--high-val")
        args = parser.parse_args()
        low_val = np.array([*map(int, args.low_val.split(","))])
        high_val = np.array([*map(int, args.high_val.split(","))])
        main(args.width, args.height, low_val, high_val)
    # Example file calling
    # python red_detect.py -w 800 -h 600 -lv 163,74,30 -hv 179,255,255
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