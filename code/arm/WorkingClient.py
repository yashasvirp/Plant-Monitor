import cv2 as cv
import requests
import numpy as np

#servo constants
serverIP = "localhost"
serverPort = "8080"
serverURL = f"http://{serverIP}:{serverPort}"

#servo constants

LR_delta = 100
LR_speed = 100

def makeRequest(endpoint):
	res = requests.get(f"{serverURL}/" + endpoint)
	return res.text

print("Server start status: ", makeRequest("start"))
pin = 1
while True:
	cv.imshow("dummy image", np.zeros([8,8,3], dtype=np.uint8))
	key = cv.waitKey(0)


	print("Pin is {}".format(pin))


	if key == 81:
		print(makeRequest(f"update_pos?delta={LR_delta}&speed={LR_speed}&dir=left&pin={pin}"))
		print("Pin 1 servo: " + makeRequest(f"get_pos?pin=1"))
		print("Pin 2 servo: " + makeRequest(f"get_pos?pin=2"))
		print("Pin 3 servo: " + makeRequest(f"get_pos?pin=3"))
		print("Pin 4 servo: " + makeRequest(f"get_pos?pin=4"))
	elif key == 83:
		print(makeRequest(f"update_pos?delta={LR_delta}&speed={LR_speed}&dir=right&pin={pin}"))
		print("Pin 1 servo: " + makeRequest(f"get_pos?pin=1"))
		print("Pin 2 servo: " + makeRequest(f"get_pos?pin=2"))
		print("Pin 3 servo: " + makeRequest(f"get_pos?pin=3"))
		print("Pin 4 servo: " + makeRequest(f"get_pos?pin=4"))
	elif key ==  ord("s"):
		k = cv.waitKey(0)
		if k in [ord("1"), ord("2"), ord("3"), ord("4"), ord("5"), ord("6"), ord("7"), ord("8")]:
			pin = k - ord("0")

	if key == ord("q"):
		#print(makeRequest(f"update_pos?delta={LR_delta}&speed={128}&dir=left&pin={4}"))
		break
	print(key)
cv.destroyAllWindows()
