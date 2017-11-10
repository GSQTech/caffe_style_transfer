import numpy as np
from PIL import Image, ImageFilter
import time
import sys, argparse
import caffe
import scipy

def save_image(img, name):
    img = img
    output_img = np.zeros((512,512,3))
    output_img = img.transpose((1,2,0))
    scipy.misc.imsave(name, output_img)


parser = argparse.ArgumentParser(description='Real-time style transfer image generator')
parser.add_argument('input')
parser.add_argument('--gpu', '-g', default=-1, type=int,
                    help='GPU ID (negative value indicates CPU)')
parser.add_argument('--model', '-m', default='model_caffe/morden_art.caffemodel', type=str)
parser.add_argument('--out', '-o', default='out.jpg', type=str)
args = parser.parse_args()



if args.gpu > 0:
    caffe.set_device(args.gpu)
    caffe.set_mode_gpu()
    xp = np
else:
    caffe.set_mode_cpu()
    xp = np


net = caffe.Net('model_caffe/style.prototxt',args.model, caffe.TEST)




width = 224
height = 224


original = Image.open(args.input).convert('RGB')
original = original.resize((512,512), Image.ANTIALIAS)

image = np.asarray(original, dtype=np.float32).transpose(2, 0, 1)
image = image.reshape((1,) + image.shape)
image = xp.asarray(image)


net.blobs['data'].data[...]	= image


start = time.time()
net.forward()
print(time.time() - start, 'sec')

y = net.blobs['output'].data[...]


save_image(y[0], args.out)
