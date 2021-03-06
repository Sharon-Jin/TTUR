#import os
#os.environ['CUDA_VISIBLE_DEVICES'] = "0"
import tensorflow as tf
import numpy as np
import scipy.misc
import fid
import data_container as dc
from glob import glob
import os

#
# Functions taken from: https://github.com/carpedm20/DCGAN-tensorflow/blob/master/utils.py
#
def get_image(image_path, input_height, input_width,
              resize_height=64, resize_width=64,
              is_crop=True, is_grayscale=False):
  image = imread(image_path, is_grayscale)
  return transform(image, input_height, input_width,
                   resize_height, resize_width, is_crop)

def imread(path, is_grayscale = False):
  if (is_grayscale):
    return scipy.misc.imread(path, flatten = True).astype(np.float)
  else:
    return scipy.misc.imread(path).astype(np.float)

def transform(image, input_height, input_width,
              resize_height=64, resize_width=64, is_crop=True):
  if is_crop:
    cropped_image = center_crop(
      image, input_height, input_width,
      resize_height, resize_width)
  else:
    if (input_height != resize_height) or (input_width != resize_width):
      cropped_image = scipy.misc.imresize(image, [resize_height, resize_width])
    else:
      cropped_image = image
  return np.array(cropped_image)
#-------------------------------------------------------------------------------


# set paths
DATA_PATH = # set path to celebA
# download the Inception modelf from http://download.tensorflow.org/models/image/imagenet/inception-2015-12-05.tgz
MODEL_PATH = # set path to inception model
STATS_PATH = # set path to stats



# read N_IMGS data samples and store them in an data container
print("Reading data...", end="", flush=True)
data = glob( os.path.join(DATA_PATH,"*"))
N_IMGS = 5000; N_FEATURES = 64*64*3
X = dc.DataContainer(np.zeros((N_IMGS, N_FEATURES)), epoch_shuffle=True)
for i in range(N_IMGS):
    img = get_image( data[i],
                    input_height=64,
                    input_width=64,
                    resize_height=64,
                    resize_width=64,
                    is_crop=False,
                    is_grayscale=False)
    X._data[i,:] = img.flatten()
print("done")



# load inference model
fid.create_incpetion_graph(MODEL_PATH)

# load precalculated statistics
sigma_trn, mu_trn = fid.load_stats(STATS_PATH)

n_rect = 5
batch_size = 500
alphas = [ 0.75, 0.5, 0.25, 0.0]
init = tf.global_variables_initializer()
sess = tf.Session()
with sess.as_default():
    sess.run(init)
    query_tensor = fid.get_Fid_query_tensor(sess)
    for i,a in enumerate(alphas):
        # disturbe images with implanted black rectangles
        X.apply_mult_rect(n_rect, 64, 64, 3, share=a, val=X._data.min())
        # propagate disturbed images through imagnet
        pred_array = fid.get_predictions( X.get_next_transformed_batch(N_IMGS)[0].reshape(-1,64,64,3),
                                          query_tensor,
                                          sess,
                                          batch_size=batch_size,
                                          verbous=True)
        # calculate FID
        FID, _, _ = fid.FID( pred_array, mu_trn, sigma_trn, sess)
        print("-- alpha: " + str(a) + ", FID: " + str(FID))
