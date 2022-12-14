# 对单个图像可视化
from pytorch_grad_cam import GradCAM, ScoreCAM, GradCAMPlusPlus, AblationCAM, XGradCAM, EigenCAM
from pytorch_grad_cam.utils.image import show_cam_on_image, \
    deprocess_image, \
    preprocess_image
from torchvision.models import resnet50
import cv2
import numpy as np
import os

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# 1.加载模型
model = resnet50(pretrained=True)
# 2.选择目标层
target_layer = [model.layer4[-1]]
# 3. 构建输入图像的Tensor形式
image_path = '../data/images/001.png'
rgb_img = cv2.imread(image_path, 1)[:, :, ::-1]  # 1是读取rgb
rgb_img = np.float32(rgb_img) / 255

# preprocess_image作用：归一化图像，并转成tensor
input_tensor = preprocess_image(rgb_img, mean=[0.485, 0.456, 0.406],
                                std=[0.229, 0.224, 0.225])  # torch.Size([1, 3, 224, 224])
# Create an input tensor image for your model..
# Note: input_tensor can be a batch tensor with several images!

# Construct the CAM object once, and then re-use it on many images:
# 4.初始化GradCAM，包括模型，目标层以及是否使用cuda
cam = GradCAM(model=model, target_layers=target_layer, use_cuda=True)

# If target_category is None, the highest scoring category
# will be used for every image in the batch.
# target_category can also be an integer, or a list of different integers
# for every image in the batch.
# 5.选定目标类别，如果不设置，则默认为分数最高的那一类
target_category = None  # 281

# You can also pass aug_smooth=True and eigen_smooth=True, to apply smoothing.
# 6. 计算cam
grayscale_cam = cam(input_tensor=input_tensor.cuda())  # [batch, 224,224]

# In this example grayscale_cam has only one image in the batch:
# 7.展示热力图并保存, grayscale_cam是一个batch的结果，只能选择一张进行展示
grayscale_cam = grayscale_cam[0]
visualization = show_cam_on_image(rgb_img, grayscale_cam, use_rgb=True)  # (224, 224, 3)
cv2.imwrite(f'cam_dog.jpg', visualization)
