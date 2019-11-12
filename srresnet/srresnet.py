import numpy as np
import time
import os
import cv2
import urllib.request
import sys

from PIL import Image

import ailia

OPT_MODEL=True
if OPT_MODEL:
	model_path = "srresnet.opt.onnx.prototxt"
	weight_path = "srresnet.opt.onnx"
else:
	model_path = "srresnet.onnx.prototxt"
	weight_path = "srresnet.onnx"

print("downloading ...");

if not os.path.exists(model_path):
    urllib.request.urlretrieve("https://storage.googleapis.com/ailia-models/srresnet/"+model_path,model_path)
if not os.path.exists(weight_path):
    urllib.request.urlretrieve("https://storage.googleapis.com/ailia-models/srresnet/"+weight_path,weight_path)

print("loading ...");

env_id=ailia.ENVIRONMENT_AUTO

env_id=ailia.get_gpu_environment_id()
net = ailia.Net(model_path,weight_path,env_id=env_id)

print("inferencing ...");

ailia_input_width = net.get_input_shape()[3]
ailia_input_height = net.get_input_shape()[2]

file_name = './lenna.png'

img = cv2.imread(file_name)

img = cv2.resize(img,(ailia_input_width,ailia_input_height),interpolation=cv2.INTER_AREA)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

img.shape = (1,) + img.shape
img = img.transpose((0, 3, 1, 2))
img = np.array(img)
img = img.astype(np.float32)
img = img / 255.0

output_img = None

cnt = 3
for i in range(cnt):
	start=int(round(time.time() * 1000))
	output_img = net.predict(img)
	end=int(round(time.time() * 1000))
	print("## ailia processing time , "+str(i)+" , "+str(end-start)+" ms")

output_img = output_img.transpose((0,2,3,1))
shape = output_img.shape
output_img = output_img.reshape((shape[1],shape[2],shape[3]))
output_img = output_img*255.
output_img[output_img<0] = 0
output_img[output_img>255.] = 255.            
output_img = output_img.astype(np.int8)
img2 = Image.fromarray(output_img, 'RGB')
img2.save('output.png')