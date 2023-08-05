import torch
from torchvision import transforms

from pytorch.segmentation.data_loader.segmentation_dataset import SegmentationDataset
from pytorch.segmentation.data_loader.transform import Rescale, ToTensor
from pytorch.segmentation.trainer import Trainer
from pytorch.segmentation.predict import *
from pytorch.segmentation.models import all_models
from pytorch.util.logger import Logger

# train_images = r'D:/datasets/cityspaces_full/images/train'
# test_images = r'D:/datasets/cityspaces_full/images/test'
# train_labled = r'D:/datasets/cityspaces_full/labeled/train'
# test_labeled = r'D:/datasets/cityspaces_full/labeled/test'

train_images = r'test/dataset/cityspaces/images/train'
test_images = r'test/dataset/cityspaces/images/test'
train_labled = r'test/dataset/cityspaces/labeled/train'
test_labeled = r'test/dataset/cityspaces/labeled/test'

if __name__ == '__main__':
    model_name = "fcn16_resnet18"
    device = 'cuda'
    batch_size = 8
    n_classes = 34
    input_axis_minimum_size = 80
    fixed_feature = False
    pretrained = False
    num_epochs = 1
    check_point_stride = 1

    logger = Logger(model_name=model_name, data_name='example')

    # Loader
    compose = transforms.Compose([
        Rescale(input_axis_minimum_size),
        ToTensor()
         ])

    train_datasets = SegmentationDataset(train_images, train_labled, n_classes, compose)
    train_loader = torch.utils.data.DataLoader(train_datasets, batch_size=batch_size, shuffle=True, drop_last=True)

    #test_datasets = SegmentationDataset(test_images, test_labeled, n_classes, compose)
    #test_loader = torch.utils.data.DataLoader(test_datasets, batch_size=batch_size, shuffle=True, drop_last=True)
    test_loader = None

    # Model
    model = all_models.model_from_name[model_name](n_classes, batch_size,
                                                   pretrained=pretrained,
                                                   fixed_feature=fixed_feature)
    #Optimizers

    if pretrained and fixed_feature: #fine tunning
        params_to_update = model.parameters()
        print("Params to learn:")
        params_to_update = []
        for name, param in model.named_parameters():
            if param.requires_grad == True:
                params_to_update.append(param)
                print("\t", name)
        optimizer = torch.optim.Adadelta(params_to_update)
    else:
        optimizer = torch.optim.Adadelta(model.parameters())

    #logger.load_model(model, 'epoch_280')
    model.to(device)
    #Train
    scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=10, gamma=0.1)
    trainer = Trainer(model, optimizer, logger, num_epochs,
                      train_loader, test_loader,
                      #epoch=281,
                      check_point_epoch_stride=check_point_stride)
    trainer.train()

    # Get result
    predict(model, r'C:\Dropbox\Dropbox\python\pytorch\docs\exam_result\input3.png',
              r'C:\Dropbox\Dropbox\python\pytorch\docs\exam_result\output3.png')
    # predict(model, r'C:\Dropbox\Dropbox\python\pytorch\docs\exam_result\input4.png',
    #         r'C:\Dropbox\Dropbox\python\pytorch\docs\exam_result\output4.png')
    # predict(model, r'C:\Dropbox\Dropbox\python\pytorch\docs\exam_result\input3.png',
    #         r'C:\Dropbox\Dropbox\python\pytorch\docs\exam_result\output3.png')
    #
    # convert_seg_gray_to_color(r'C:\Dropbox\Dropbox\python\pytorch\docs\exam_result\ground_truth3.png', n_classes,
    #                           output_path='C:\Dropbox\Dropbox\python\pytorch\docs\exam_result\c_ground_truth3.png')
    # convert_seg_gray_to_color(r'C:\Dropbox\Dropbox\python\pytorch\docs\exam_result\ground_truth4.png', n_classes,
    #                           output_path='C:\Dropbox\Dropbox\python\pytorch\docs\exam_result\c_ground_truth4.png')
    # convert_seg_gray_to_color(r'C:\Dropbox\Dropbox\python\pytorch\docs\exam_result\ground_truth5.png', n_classes,
    #                           output_path='C:\Dropbox\Dropbox\python\pytorch\docs\exam_result\c_ground_truth5.png')




