from typing import List, Optional
import sys
import time
import argparse

from flask import Flask, request
from werkzeug import serving

from sc08a import SC08A
import serial

class Service:
    """Flask service for SCO8A Servo Controller

    Args:
        pins: List of pins to run on the service
        port: The port for the servo controller
        baudrate: Baudrate for the port


    TODO:
        1. Motor status, is it on or off?
        2. Motor running status, is the motor running?
           While running we should not issue new commands to a motor and
           status should be stored internally

    """
    def __init__(self, port: str, baudrate: Optional[int] = None):
        #self.pins = pins
        self.port = port
        self.baudrate = baudrate or 9600
        self.app = Flask("Servo")
        self.init_routes()

    def init_controller(self):
        self.controller = SC08A(self.port, self.baudrate)
        self.controller.init_all_motors()
        for i in range(1,9):
            self.controller.set_pos_speed(i, 4000, 50)

    def init_routes(self):
        @self.app.route("/update_pos", methods=["GET"])  
        def _update_pos():
            if "dir" not in request.args:
                return "no direction given"           
            if "delta" not in request.args:
                return "delta not given"
            if "speed" not in request.args:
                return "speed not given"
           
            delta = int(request.args.get("delta"))
            speed = int(request.args.get("speed"))
            pin = int(request.args.get("pin"))
            dir = request.args.get("dir")
        
            curr_pos = self.controller.get_pos(pin)
            if(dir == "left"):
                curr_pos-=delta
            elif(dir=="right"):
                curr_pos+=delta

            if(curr_pos == 300 or curr_pos == 8000):
                pass
            elif(curr_pos>300 or curr_pos<8000):                      
                self.controller.set_pos_speed(pin, curr_pos,speed )
            if(curr_pos<300):
                curr_pos = 300
            if(curr_pos>8000):
                curr_pos = 8000 
            print("Setting position for motor: {pin} at: {curr_pos} and speed: {speed}")           
            return f"Setting position for motor: {pin} at: {curr_pos} and speed: {speed}"
       
        @self.app.route("/set_pos", methods=["GET"])
        def _set_pos():
            if "pin" not in request.args:
                return "Pin not given"
            if "pos" not in request.args:
                return "pos (position) not given"
            if "speed" not in request.args:
                print("speed not given. Will use 50")
                speed = 50
            else:
                speed = int(request.args.get("speed"))
            pin = int(request.args.get("pin"))
            pos = int(request.args.get("pos"))
            self.controller.set_pos_speed(pin, pos, speed)
            return f"Setting position for motor: {pin} at: {pos} and speed: {speed}"

        @self.app.route("/get_pos", methods=["GET"])
        def _get_pos():
            print(request.args.get("pin"))
            if "pin" not in request.args:
                return "Pin not given"
            pin = int(request.args.get("pin"))
            return str(self.controller.get_pos(pin))

        @self.app.route("/reset", methods=["GET"])
        def _reset():
            if "pin" not in request.args:
                return "Pin not given"
            pin = int(request.args.get("pin"))
            self.controller.off_motor(pin)
            return f"Turning motor {pin} OFF"

        @self.app.route("/reset_all", methods=["GET"])
        def _reset_all():
            for pin in self.pins:
                self.controller.off_motor(pin)
            return "Issued OFF command for all motors"

        @self.app.route("/close", methods=["GET"])
        def _close():
            _reset_all()
            self.controller.shutdown()
            return "Stopped all motors and turned off the controller"

        @self.app.route("/start", methods=["GET"])
        def _start():
            self.init_controller()
            return "Initialized the controller"

    def start(self):
        serving.run_simple("0.0.0.0", 8080, self.app, threaded=True)
        self.init_controller()

# if __name__ == '__main__':
#     parser = argparse.ArgumentParser()
#     parser.add_argument("--pins", required=True, help="List of comma separated pins")
#     parser.add_argument("--port", required=True, help="The serial port")
#     parser.add_argument("--baudrate", help="Baudrate for the serial port")
#     args = parser.parse_args()
#     pins = args.pins.split(",")
#     service = Service([*map(int, pins)], args.port, args.baudrate)
#     service.start()
#myServo = SC08A("/dev/ttyUSB0", 9600)
#myServo.init_all_motors()
#test_servo(myServo, 4)
myService = Service("/dev/ttyUSB0", 9600)
myService.start()
