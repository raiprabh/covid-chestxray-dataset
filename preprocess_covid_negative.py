import numpy as np;
import os;
from skimage import io, color, util, transform, img_as_ubyte;
import pydicom;

source_dir = './dataset/source';
destination_dir = './dataset/destination';

target_height = 256;
target_width = 362;

count = 0;

max_new_width = 0;

for _,_,files in os.walk(source_dir):
	for file in files:
		img_path = os.path.join(source_dir, file);

		image = pydicom.dcmread(img_path).pixel_array;
		image_processed = color.rgb2gray(image);
		height,width = image_processed.shape;


		rescale_factor = target_height / height;
		image_processed = transform.rescale(image_processed, (rescale_factor, rescale_factor));

		#if image_processed.shape[1] > 362:
		#	continue

		im_max = np.max(image_processed);
		im_min = np.min(image_processed);

		if im_max > 1:
			image_processed[image_processed > 1] = 1.0;

		# print('processed max: ', im_max);
		# print('processed min: ', im_min);

		image_processed_path = os.path.join(destination_dir, os.path.splitext(file)[0] + '.png');
		if '._' in image_processed_path:
			split = image_processed_path.split('._');
			image_processed_path = image_processed_path[0] + image_processed_path[1];
		io.imsave(image_processed_path, img_as_ubyte(image_processed));
		print(image_processed_path);

		_,new_width = io.imread(image_processed_path).shape;
		# if new_width > max_new_width:
		# 	max_new_width = new_width

		# count+=1;

		# if count > 10:
		# 	break;

# print(count);

for _,_,files in os.walk(destination_dir):
	for file in files:
		if file.endswith('.png'):
			if '._' in file:
				file = file.split('._')[1];
			new_img_path = os.path.join(destination_dir, file);
			new_image = io.imread(new_img_path);
			new_height,new_width = new_image.shape;

			if new_width < target_width:
				total_pad_width = target_width-new_width;
				pad_left = int(np.ceil(total_pad_width/2));
				pad_right = int(total_pad_width - pad_left);

				new_image_processed = util.pad(new_image, ((0, 0), (pad_left,pad_right)), 'constant', constant_values=(0, 0));
				height, width = new_image_processed.shape
				assert height == target_height
				assert width == target_width
				print(new_image_processed.shape)
				io.imsave(new_img_path, img_as_ubyte(new_image_processed));
			else:
				rescale_factor = target_width / new_width
				image_processed = transform.rescale(new_image, (rescale_factor, rescale_factor));
				processed_height, processed_width = image_processed.shape
				total_pad_height = target_height - processed_height
				pad_top = int(np.ceil(total_pad_height/2));
				pad_bottom = int(total_pad_height - pad_top);
				new_image_processed = util.pad(image_processed, ((pad_top, pad_bottom), (0, 0)), 'constant', constant_values=(0, 0));
				height, width = new_image_processed.shape
				assert height == target_height
				assert width == target_width
				print(new_image_processed.shape)
				io.imsave(new_img_path, img_as_ubyte(new_image_processed));

