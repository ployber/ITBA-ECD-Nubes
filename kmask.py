#!/usr/bin/env python3.8.6
import numpy as np
import collections
import math
import cv2
import argparse
from sklearn.cluster import KMeans
from PIL import Image
from joblib import parallel_backend

def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % (int(rgb[0]), int(rgb[1]), int(rgb[2]))
def format_perc(num, x):
     return str(num*100)[:4 + (x-1)] + '%'
if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Image crop")
	parser.add_argument('-i', '--src_img', help='Source Image', required=True)
	parser.add_argument('-m', '--src_mask', help='Source Mask', required=True)
	parser.add_argument('-v', '--debug', help='print debug msgs', required=False, action='store_true')
	args = parser.parse_args()
	##Open image for processing in RGB colorspace.

	img=cv2.imread(args.src_img)
	msk=cv2.imread(args.src_mask)

	masked = cv2.bitwise_and(img, msk)

	tmp = cv2.cvtColor(masked, cv2.COLOR_BGR2GRAY)
	_,alpha = cv2.threshold(tmp,0,255,cv2.THRESH_BINARY)
	b, g, r = cv2.split(masked)
	rgba = [b,g,r, alpha]
	maskeda = cv2.merge(rgba, 4)

# Cyan
	bg = np.array([255, 255, 0])
	alpha = (maskeda[:, :, 3] / 255).reshape(maskeda.shape[:2] + (1,))
	maskeda_bg_amarillo = ((bg * (1 - alpha)) + (maskeda[:, :, :3] * alpha)).astype(np.uint8)

	maskeda_bg_amarillo=maskeda_bg_amarillo.reshape((maskeda_bg_amarillo.shape[1]*maskeda_bg_amarillo.shape[0],3))
	with parallel_backend('threading', n_jobs=4):
		kmeans=KMeans(n_clusters=7, init="k-means++", n_init=7, verbose=False, algorithm="elkan")
	s=kmeans.fit(maskeda_bg_amarillo)
	nplabels=kmeans.labels_
	items, cuantos = np.unique(nplabels, return_counts=True)
	tlargo=nplabels.size
	percent=[]
	for i in items:
		percent.append(cuantos[i]/tlargo)

	centroid=kmeans.cluster_centers_
# bg 0.5500303571533832
	covertura_pos = -1
	str_bgr_hex0 = rgb_to_hex(centroid[0])
	str_bgr_hex1 = rgb_to_hex(centroid[1])
	str_bgr_hex2 = rgb_to_hex(centroid[2])
	str_bgr_hex3 = rgb_to_hex(centroid[3])
	str_bgr_hex4 = rgb_to_hex(centroid[4])
	str_bgr_hex5 = rgb_to_hex(centroid[5])
	str_bgr_hex6 = rgb_to_hex(centroid[6])
	if args.debug:
		print("str_bgr_hex0", str_bgr_hex0)
		print("str_bgr_hex1", str_bgr_hex1)
		print("str_bgr_hex2", str_bgr_hex2)
		print("str_bgr_hex3", str_bgr_hex3)
		print("str_bgr_hex4", str_bgr_hex4)
		print("str_bgr_hex5", str_bgr_hex5)
		print("str_bgr_hex6", str_bgr_hex6)
	if (str_bgr_hex0 == "#4ee329" or str_bgr_hex0 == "#4ee429" or str_bgr_hex0 == "#4fe32a" or str_bgr_hex0 == "#4fe42a" or str_bgr_hex0 == "#4ee42a" or str_bgr_hex0 == "#4ee32a" or str_bgr_hex0 == "#4de329"):
		covertura_pos = 0
	if (str_bgr_hex1 == "#4ee329" or str_bgr_hex1 == "#4ee429" or str_bgr_hex1 == "#4fe32a" or str_bgr_hex1 == "#4fe42a" or str_bgr_hex1 == "#4ee42a" or str_bgr_hex1 == "#4ee32a" or str_bgr_hex1 == "#4de329"):
		covertura_pos = 1
	if (str_bgr_hex2 == "#4ee329" or str_bgr_hex2 == "#4ee429" or str_bgr_hex2 == "#4fe32a" or str_bgr_hex2 == "#4fe42a" or str_bgr_hex2 == "#4ee42a" or str_bgr_hex2 == "#4ee32a" or str_bgr_hex2 == "#4de329"):
		covertura_pos = 2
	if (str_bgr_hex3 == "#4ee329" or str_bgr_hex3 == "#4ee429" or str_bgr_hex3 == "#4fe32a" or str_bgr_hex3 == "#4fe42a" or str_bgr_hex3 == "#4ee42a" or str_bgr_hex3 == "#4ee32a" or str_bgr_hex3 == "#4de329"):
		covertura_pos = 3
	if (str_bgr_hex4 == "#4ee329" or str_bgr_hex4 == "#4ee429" or str_bgr_hex4 == "#4fe32a" or str_bgr_hex4 == "#4fe42a" or str_bgr_hex4 == "#4ee42a" or str_bgr_hex4 == "#4ee32a" or str_bgr_hex4 == "#4de329"):
		covertura_pos = 4
	if (str_bgr_hex5 == "#4ee329" or str_bgr_hex5 == "#4ee429" or str_bgr_hex5 == "#4fe32a" or str_bgr_hex5 == "#4fe42a" or str_bgr_hex5 == "#4ee42a" or str_bgr_hex5 == "#4ee32a" or str_bgr_hex5 == "#4de329"):
		covertura_pos = 5
	if (str_bgr_hex6 == "#4ee329" or str_bgr_hex6 == "#4ee429" or str_bgr_hex6 == "#4fe32a" or str_bgr_hex6 == "#4fe42a" or str_bgr_hex6 == "#4ee42a" or str_bgr_hex6 == "#4ee32a" or str_bgr_hex6 == "#4de329"):
		covertura_pos = 6

	covertura = 1
	if percent[0] > 0.55:
		bg_pos = 0
		ptot = percent[1] + percent[2] + percent[3] + percent[4] + percent[5] + percent[6]
		covertura = percent[covertura_pos]/ptot
	if percent[1] > 0.55:
		bg_pos = 1
		ptot = percent[0] + percent[2] + percent[3] + percent[4] + percent[5] + percent[6]
		covertura = percent[covertura_pos]/ptot
	if percent[2] > 0.55:
		bg_pos = 2
		ptot = percent[0] + percent[1] + percent[3] + percent[4] + percent[5] + percent[6]
		covertura = percent[covertura_pos]/ptot
	if percent[3] > 0.55:
		bg_pos = 3
		ptot = percent[0] + percent[1] + percent[2] + percent[4] + percent[5] + percent[6]
		covertura = percent[covertura_pos]/ptot
	if percent[4] > 0.55:
		bg_pos = 4
		ptot = percent[0] + percent[1] + percent[2] + percent[3] + percent[5] + percent[6]
		covertura = percent[covertura_pos]/ptot
	if percent[5] > 0.55:
		bg_pos = 5
		ptot = percent[0] + percent[1] + percent[2] + percent[3] + percent[4] + percent[6]
		covertura = percent[covertura_pos]/ptot
	if percent[6] > 0.55:
		bg_pos = 6
		ptot = percent[0] + percent[1] + percent[2] + percent[3] + percent[4] + percent[5]
		covertura = percent[covertura_pos]/ptot

	if args.debug:
		print("%0", percent[0])
		print("%1", percent[1])
		print("%2", percent[2])
		print("%3", percent[3])
		print("%4", percent[4])
		print("%5", percent[5])
		print("%6", percent[6])
		print("cov ix", covertura_pos)
		print("bg ix", bg_pos)
		print("total", ptot)
	if covertura_pos > -1:
		print(args.src_img, ", ", format_perc(covertura, 2))
	else:
		print(args.src_img, ", ERROR pos covertura")

