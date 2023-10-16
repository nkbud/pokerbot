import argparse
import subprocess
import time

import numpy as np
import pyautogui
import cv2 as cv

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('--ahk_cmd', type=str, default="C:/Program Files/AutoHotkey/AutoHotkey.exe")
	parser.add_argument('--ahk_exe', type=str, default="PokerStars.exe")
	parser.add_argument('--ahk_class', type=str, default="GLFW30")
	args = parser.parse_args()

	cmd = subprocess.list2cmdline([
		"powershell",
		"Start-Process",
		"-FilePath",
		"\"" + args.ahk_cmd + "\"",
		"-ArgumentList",
		",".join([
			"window.ahk",
			"\"" + args.ahk_exe + "\"",
			"\"" + args.ahk_class + "\""
		])])
	completed = subprocess.run(cmd)

	if completed.returncode == 0:
		time.sleep(1)
		with open("./window.props", "r") as f:
			xywh = f.readline()
		with open("./window.props", "w") as f:
			f.writelines([
				"ahk_cmd=" + args.ahk_cmd + "\n",
				"ahk_exe=" + args.ahk_exe + "\n",
				"ahk_class=" + args.ahk_class + "\n",
				"xywh=" + xywh
			])

	x,y,w,h = xywh.split(",")[0:4]
	rgb = np.array(pyautogui.screenshot(region=(x,y,w,h)))
	bgr = cv.cvtColor(rgb, cv.COLOR_RGB2BGR)
	cv.imwrite("window.png", bgr)
