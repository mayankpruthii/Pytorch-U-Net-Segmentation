from torch.utils.data import Dataset
import glob
import torch
import numpy as np
import json
import sys
from PIL import Image
from utils.one_hot_encoder import HotEncoder
from skimage import io
import skimage


class ImageList():
    """Give the Image and Annotations direcectory and train_percentage
        it generates a list of image paths which are passed to the
        Image loaders"""

    def __init__(self, Images, Annotations,
                 train_percentage, extension):
        self.extension = "/*" + extension
        self.Image = glob.glob(Images + self.extension)
        self.Annotations = glob.glob(Annotations + self.extension)
        self.train_percentage = train_percentage
        train_len = int(train_percentage * len(Images))
        self.train_set = {"Images": self.Image[:train_len],
                          "Annotations": self.Annotations[:train_len]}
        self.test_set = {"Images": self.Image[train_len:],
                         "Annotations": self.Annotations[train_len:]}


class ImageLoader(Dataset):
    """Takes a data dict generated from the ImageList class.
        Make object pass the training/test dataset and loop through it"""

    def __init__(self, data, encoder_obj, extension="jpeg", transform=None):
        self.extension = extension.lower()
        self.transform = transform
        self.images = data["Images"]
        self.target_images = data["Annotations"]
        self.encoder= encoder_obj
        self.colors= self.encoder_obj.color


    def __len__(self):
        return len(self.images)

    def __getitem__(self, index):
        if self.extension == "png":
            image = io.imread(self.images[index])[:3]
            label = io.imread(self.target_images)[:3]
        if self.extension == "tif":
            image = Image.open(self.images[index])
            label = Image.open(self.target_images[index])
        label = self.encoder.hotEncode(self.encoder.PerPixelClassMatrix(label))
        if self.transform:
            image = self.transform(image)
            label = self.transform(label)
        return {"Image": image, "Label": label}
