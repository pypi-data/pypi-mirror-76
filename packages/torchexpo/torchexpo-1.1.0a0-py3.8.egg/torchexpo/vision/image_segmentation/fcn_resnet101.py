import abc
import torch
import torch.nn as nn
import torchvision
from torchexpo.modules import ImageSegmentationModule


def fcn_resnet101():
    """FCN-ResNet101 Model"""
    model = FCNResNet101()
    obj = ImageSegmentationModule(model, "FCN-ResNet101")
    return obj

class FCNResNet101(nn.Module):
    """TorchExpo FCN-ResNet101 Scriptable Module"""
    def __init__(self):
        super(FCNResNet101, self).__init__()
        self.fcn = torchvision.models.segmentation.fcn_resnet101(pretrained=True)

    @abc.abstractmethod
    def forward(self, tensor):
        """Model Forward"""
        output = self.fcn(tensor)['out']
        return output[0]