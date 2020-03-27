import math
import geopy
from geopy.distance import VincentyDistance
import cv2
import numpy as np
import time

def mouse_crop(event, x, y, flags, param):
	# grab references to the global variables
	global x_start, y_start, x_end, y_end, cropping
	if event == cv2.EVENT_LBUTTONDOWN:
		x_start, y_start, x_end, y_end = x, y, x, y
		cropping = True

	elif event == cv2.EVENT_MOUSEMOVE:
		if cropping == True:
			x_end, y_end = x, y

	elif event == cv2.EVENT_LBUTTONUP:
		x_end, y_end = x, y
		cropping = False
		return (int((x_start+x_end)/2),int((y_start+y_end)/2))

def call (latc, longc, auvh, bearingr, px, py, height = 1080, width = 1920, hfov = 88.35605961287, vfov = 56.88585724872): #88.35605961287 56.88585724872 or #63.10276 41.9357
	global u1, u2
	heightr = 2*auvh*math.tan(vfov/2)
	widthr = 2*auvh*math.tan(hfov/2)
	x1 = int (height/2)
	y1 = int (width/2)
	dpph = heightr/height
	dppv = widthr/width
	origin = geopy.Point(latc, longc)
	if px>= (width/2):
		bearingo = 90 + (180*math.atan((py-y1)/(px-x1)))/math.pi
	else:
		bearingo = 270 + (180*math.atan((py-y1)/(px-x1)))/math.pi
	bearing = bearingr + bearingo
	if bearing > 360:
		bearing = bearing - 360
	actdist = (math.pow(((py-y1)*(py-y1)*dppv*dppv + (px-x1)*(px-x1)*dpph*dpph),0.5))
	destination = VincentyDistance(kilometers=(actdist/1000)).destination(origin, bearing)
	t = (destination.latitude, destination.longitude)
	return t

cropping = False
x_start, y_start, x_end, y_end, u1, u2 = 0, 0, 0, 0, 0.0, 0.0
lon,lat,alt,bear=0.0,0.0,0.0,0.0
f=1
ln=-1
ii=open('gps_log.txt')
il=ii.read()
list1=il.split()
ww=int(len(list1)/6)
a=cv2.VideoCapture('b.avi')
while True:
	time.sleep(0.05)
	_,img=a.read()
	cv2.imshow('b',img)
	dimensions = img.shape
	k=cv2.waitKey(1)
	if k & 0xFF == ord('p'):
		u=str(f)
		xb=img.copy()
		cv2.imshow(u,xb)
		oriImage = xb.copy()
		cv2.namedWindow(u)
		cv2.setMouseCallback(u, mouse_crop)
		while True:
			i = xb.copy()
			if not cropping:
				cv2.imshow(u, xb)
			k = cv2.waitKey(0)
			if k & 0xFF == ord('x'):
				break
		lon,lat,alt,bear=float(list1[(ln*6)+2]),float(list1[(ln*6)+3]),((-1)*float(list1[(ln*6)+4])-195.04),float(list1[(ln*6)+5])
		px = int((x_start+x_end)/2)
		py = int((y_start+y_end)/2)
		xx = call(lat, lon, alt, bear, px, py, dimensions[0], dimensions[1])
		print ("Latitude: ", xx[0], "Longitude: ", xx[1])
		f=f+1
	if k==27:
		break
	ln=ln+1