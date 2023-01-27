from PIL import Image
import os

from utils import tensor_load_rgbimage
from utils import tensor_save_rgbimage
from utils import tensor_save_bgrimage
from utils import preprocess_batch
from net import *


def load_images(content_image_path, style_image_path):
    """
    Function to download and preprocess images to Net

    Args:
            content_image_path (string): path to content photo
            style_image_path (string): path to style photo
    """
    content_image = tensor_load_rgbimage(content_image_path, size=512,
                                         keep_asp=True).unsqueeze(0)
    style_image = tensor_load_rgbimage(
        style_image_path, size=512).unsqueeze(0)
    style_image = preprocess_batch(style_image)

    return content_image, style_image


def load_net():
    """
    Function to startup and load Net
    """
    style_model = Net(ngf=128)
    model_dict = torch.load('21styles.model')
    model_dict_clone = model_dict.copy()
    for key, value in model_dict_clone.items():
        if key.endswith(('running_mean', 'running_var')):
            del model_dict[key]
    style_model.load_state_dict(model_dict, False)
    return style_model


def make_nst(model, content_image, style_image, output_path):
    style_v = Variable(style_image)
    content_image = Variable(preprocess_batch(content_image))
    model.setTarget(style_v)
    output = model(content_image)
    tensor_save_bgrimage(output.data[0], output_path, False)
