# -*- coding: utf-8 -*-
"""TSU_AllNetworks_4_spaghetti

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1kKCU9pAsVRqNR-lX1p45Z7BLTxp76CMq

# TSU all networks 4
Testing the algorithms with the spaghetti dataset (since white and red are used for lighting)
"""

"""## functions"""

# Commented out IPython magic to ensure Python compatibility.
# WandB – Install the W&B library
# %pip install wandb -q

import shutil
import os
import random
import pandas as pd
import torch
import torchvision
import torchvision.transforms as transforms
import matplotlib.image as img
from torch.utils.data.dataset import Dataset
from tqdm.notebook import tqdm
#from __future__ import print_function
#from __future__ import division
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, models, transforms
import matplotlib.pyplot as plt
import time
import copy
import numpy as np

import logging
logging.propagate = False 
logging.getLogger().setLevel(logging.ERROR)
import torch.nn.functional as F
#from __future__ import print_function
import argparse
import random # to set the python random seed
import numpy as np
# WandB – Import the wandb library
import wandb
import sys
print("PyTorch Version: ",torch.__version__)
print("Torchvision Version: ",torchvision.__version__)

# change this path on other computers
#default_path = "/content/drive/MyDrive/Colab Notebooks/ToolWearInspection/TestCameraSetup/"
default_path = "/Users/larsdepauw/Documents/Lars.nosync/Documents/School/1Ma ing/Masterproef/TWI/code/Vision/wandb/TSU_AllNetworks_4_spaghetti/TestCameraSetup/"

torch_path = os.path.join(default_path, "torch/")
data_path = os.path.join(default_path, "data/spaghetti_dataset/")
sorted_path = os.path.join(default_path, "data/spaghetti_dataset_sorted/")
labels_path = os.path.join(default_path, "data/labels5.csv")
models_path = os.path.join(sorted_path, "models/")

#unsorted_path = os.path.join(data_path, 'data_unsorted/')
train_perc = 70
valid_perc = 20
test_perc = 10

max_val = 230
min_val = 130

# all possible options for images
batches = [1,2,3,4,5,11,12,13,14,15,16,17,18,19]  # photographed batches
plates = [1,2,3,4,5,6,7,8,9,10] # plates per batch
colors = ["white", "red"]
bullets = ["nb", "b"]



def iets():
  print("iets")

def get_folder(filename, labels):
    val = float(labels.loc[labels['imgname'] == filename]["value"])
    if (val > max_val):
      return "bad/"+filename
    if (val <= max_val and val >= min_val):
      return "medium/"+filename
    if val < min_val:
      return "good/"+filename

def get_foldername(bnr, pnr):
  bn = '{:03d}'.format(int(bnr))
  pn = '{:03d}'.format(int(pnr))
  return 'batch_' + bn + '_plate_' + pn + '/'

# changed to suit the purpose of spaghetti dataset where only white and red where used with a range of leds turned on for both led strip
def get_imname(bnr, pnr, bullet, color="white"):
  bnr = '{:03d}'.format(int(bnr))
  pnr = '{:03d}'.format(int(pnr))
  startled = '{:03d}'.format(6)
  stopled = '{:03d}'.format(11)
  
  if bullet == 0:
    bulletstr = 'nb'
  else:
    bulletstr = 'b'

  path = 'b_'+bnr+'_p_'+pnr
  path += '_l_'+startled+'-'+stopled
  path += '_'+color+'_'+bullet
  path += '.png'
  return path

def get_class(bnr, pnr, bullet, labels):
  row = labels[(labels['bn'] == bnr) & (labels['pn'] == pnr) & (labels['bullet'] == bullet)]
  val = float(row.get("value"))
  #print(str(val))
  if (val > max_val):
    return "bad"
  if (val <= max_val and val >= min_val):
    return "medium"
  if val < min_val:
    return "good"

def sort_data2(labels):
    
    #sorted_path = os.path.join(data_path, "../birthday_dataset_sorted/")
    sort_dirs = ["train", "test", "valid"]
    classes = ["good", "bad", "medium"]
    for color in colors:
      for dir in sort_dirs:
        for c in classes:
          # create dir to save files
          create_path = os.path.join(sorted_path, color+"/"+dir+"/"+c+"/")
          if not os.path.exists(create_path):
            os.makedirs(create_path)
            #print("created: "+create_path)
    
    nb_plates = {"train": 0, "test":0, "valid":0}

    # take temporary variables
    temp_batches = batches
    temp_plates = plates
    temp_leds = leds
    temp_colors = colors
    temp_bullets = bullets
    temp_strips = strips

    # total files
    total_files = len(temp_batches)*len(temp_plates)*len(temp_bullets)

    #iterate over all batches and plates and bullets
    for bullet in temp_bullets:
      for plate in temp_plates:
        for batch in temp_batches:
          #print(batch)
        
          if (bullet == 'nb'): bulletnr = 0
          if (bullet == 'b'): bulletnr = 1
          

          # add chosen class to class numbers. When to much in class delete from sort_dirs to only put files in the right classes
          
          if "train" in sort_dirs and nb_plates["train"] >= (train_perc/100)*total_files: sort_dirs.remove("train")
          if "test" in sort_dirs and nb_plates["test"] >= (test_perc/100)*total_files: sort_dirs.remove("test")
          if "valid" in sort_dirs and nb_plates["valid"] >= (valid_perc/100)*total_files: sort_dirs.remove("valid")

          # generate number for selecting train, test or valid
          number = random.randint(0, len(sort_dirs)-1)   
          nb_plates[sort_dirs[number]] += 1   

          # copy all files from unsorted to sorted based on random number
          # create two datasets: one red and one white
          frompath = os.path.join(data_path, get_foldername(bnr=batch, pnr=plate))
          for color in temp_colors:
            imname = get_imname(bnr=batch, pnr=plate, bullet=bullet, color=color)
            fromfile = os.path.join(frompath,imname )

            # create url to put file; train,test,valid; good, medium, bad; imgname
            klasse = sort_dirs[number]+"/"+get_class(bnr=batch, pnr=plate, bullet=bulletnr, labels=labels)+"/"+imname
            tofile = os.path.join(sorted_path, color+"/", klasse )
            #print("fromfile: "+fromfile)
            #print("tofile  : "+tofile)
            shutil.copy2(fromfile, tofile)

    return nb_plates

def get_labels(label_path, delim=";"):
  labels = pd.read_csv(label_path,delimiter=delim)

  # bullet to 0 or 1
  labels.loc[labels['bullet'] !=1, 'bullet'] = 0
  # change values to float types
  labels["value"] = labels['value'].astype(str).str.replace(",", ".")
  #pd.to_numeric(labels["value"])
  labels["value"] = labels["value"].astype(float)
  return labels

def show_labels(labels, classes):
  plt.figure(figsize = (8,8))
  plt.pie(labels.groupby('Category').size(), labels = label, autopct='%1.1f%%', shadow=True, startangle=90)
  plt.show()

def show_image_batch(data_path):
  #print(data_path)
  fig,ax = plt.subplots(1,5,figsize = (15,3))
  images = os.listdir(data_path)
  img_class = os.path.basename(os.path.normpath(data_path))

  samples = random.sample(images, 5)

  for i,idx in enumerate(samples):
      path = os.path.join(data_path,idx)
      #print(img.imread(path).shape)
      ax[i].imshow(img.imread(path))

def show_image_classes(data_path, classes):
  for cl in classes:
    #print(cl)
    fig,ax = plt.subplots(1,5,figsize = (15,3))
    images = os.listdir(data_path+cl)
    img_class = os.path.basename(os.path.normpath(data_path+cl))

    samples = random.sample(images, 5)

    for i,idx in enumerate(samples):
        path = os.path.join(data_path+cl,idx)
        #print(img.imread(path).shape)
        ax[i].imshow(img.imread(path))

def get_mean_std(sorted_path):
  N_CHANNELS = 3
  # transform to tensor
  #transforms.ToPILImage(mode='RGB')
  transform = transforms.Compose([transforms.Resize((512,256)),
                                  transforms.CenterCrop(256),
                                  transforms.ToTensor()])
  # generate dataset
  dataset = torchvision.datasets.ImageFolder(sorted_path, transform=transform)
  full_loader = DataLoader(dataset = dataset, shuffle=False, num_workers=os.cpu_count())

  mean = torch.zeros(N_CHANNELS)
  std = torch.zeros(N_CHANNELS)
  #print('==> Computing mean and std..')
  for inputs, _labels in tqdm(full_loader):
      #print(inputs.shape)
      for i in range(N_CHANNELS):
          mean[i] += inputs[:,i,:,:].mean()
          std[i] += inputs[:,i,:,:].std()
  mean.div_(len(dataset))
  std.div_(len(dataset))
  #print(mean, std)
  return mean, std

def imshow(image, ax=None, title=None, normalize=True):
  if ax is None:
      fig, ax = plt.subplots()
  image = image.numpy().transpose((1, 2, 0))

  if normalize:
      image = std * image + mean
      image = np.clip(image, 0, 1)

  ax.imshow(image)
  ax.spines['top'].set_visible(False)
  ax.spines['right'].set_visible(False)
  ax.spines['left'].set_visible(False)
  ax.spines['bottom'].set_visible(False)
  ax.tick_params(axis='both', length=0)
  ax.set_xticklabels('')
  ax.set_yticklabels('')

  return ax

"""## Resnet model self built from pytorch website

https://pytorch.org/docs/stable/torchvision/models.html

testing different architectures
https://pytorch.org/tutorials/beginner/finetuning_torchvision_models_tutorial.html

downloading model with or without pretraining by setting True or False at pretrained 
and progress = True to show a progressbar

setting TORCH_MODEL_ZOO to a desired location to be able to reuse downloaded data later.
"""

# WandB – Login to your wandb account so you can log all your metrics
#wandb.login()

sweep_config = {
    'method': 'bayes',
    'metric': {
        'goal': 'maximize',
        'name': 'valid Accuracy'
    },    
    'parameters': {
        'batch_size': {
            'distribution': 'int_uniform',
            'min': 2,
            'max': 16
        },
        'epochs':{
            'min': 18,
            'max': 100,
            'distribution': 'int_uniform'
        },
        'lr':{
            'distribution': 'uniform',
            'max': 0.002,
            'min': 0.0001
        },
        'model_name': {
            'values': ['Resnet18', 'Alexnet', 'VGG11_bn', 'Squeezenet', 'Densenet']
        },
        'momentum' : {
            'distribution': 'uniform',
            'max': 1.8,
            'min': 0.45
        },
        'use_pretrained': {
            'values': ['True', 'False']
        },
        'num_workers' : {
            'value': 4
        },
        'num_classes': {
            'value': 3
        },
        'dataset_color': {
            'values': ['red', 'white']
        }
    }
}

# Initialize a new sweep
# Arguments:
#     – sweep_config: the sweep config dictionary defined above
#     – entity: Set the username for the sweep
#     – project: Set the project name for the sweep
#sweep_id = wandb.sweep(sweep_config, project="pytorch-TWI_spaghetti_sweep")

"""## Data

### organizing data

Getting data from one folder into training, test and validation folders

* Train
  * bad.     > 200
  * medium.  < 200 and > 150
  * good.    < 150
"""

# to sort data from unsorted path to sorted path in correct folders
# sort the files in 3 folders
# nb_plates = sort_data2(labels)

"""###Getting labels

"""

labels = get_labels(labels_path)
classes = ["good", "medium", "bad"]

get_class(3,1,1,labels) # check label

#print(labels.head())

#print(nb_plates)
#Using matplotlib
# Creating plot 
#fig = plt.figure(figsize =(10, 7))
#plt.pie(nb_plates.values(), labels = nb_plates.keys())
  
# show plot 
#plt.show()

"""###getting images

####show images
"""

show_image_batch(sorted_path+'white/train/bad/')
show_image_batch(sorted_path+'red/train/bad/')

#show_image_classes(train_path, classes)

"""#### define transformations

defining mean and std
"""

#mean, std = get_mean_std(sorted_path)
mean, std = [0.485, 0.456, 0.406], [0.229, 0.224, 0.225]

data_transforms = {
    'train': transforms.Compose([transforms.RandomAffine(degrees=4, translate=(0.2,0.2) , shear=(0.1,0.1)),
                                      transforms.Resize((224,224)),
                                      transforms.ToTensor(),
                                      transforms.Normalize(mean,std)
                                      ]),
    'valid': transforms.Compose([transforms.RandomAffine(degrees=4, translate=(0.2,0.2) , shear=(0.1,0.1)),
                                      transforms.Resize((224,224)),
                                      transforms.ToTensor(),
                                      transforms.Normalize(mean,std)
                                      ]),
    'test': transforms.Compose([transforms.Resize((224,224)),
                                     transforms.ToTensor(),
                                     transforms.Normalize(mean,std)
                                     ]),
                   
}

"""#### use folder dataloader to create dataset with transformations"""

red_datasets = {x: torchvision.datasets.ImageFolder(os.path.join(sorted_path, "red/", x), data_transforms[x]) for x in ['train', 'valid', 'test']}
white_datasets = {x: torchvision.datasets.ImageFolder(os.path.join(sorted_path, "white/", x), data_transforms[x]) for x in ['train', 'valid', 'test']}

"""## creating model

select device to run on
"""

# CPU or GPU

device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
#device

"""### helper functions"""

def test_model(model, dataloaders_dict):
  print("test")
  # test-the-model
  model.eval()  # it-disables-dropout
  correct = 0
  total = 0
  test_loss = 0
  example_images = []
  with torch.no_grad():
      
      for images, labels in dataloaders_dict["test"]:
          image = images
          label = labels
          images = images.to(device)
          labels = labels.to(device)
          outputs = model(images)

          test_loss += F.nll_loss(outputs, labels, reduction='sum').item()

          _, predicted = torch.max(outputs.data, 1)
          total += labels.size(0)
          correct += (predicted == labels).sum().item()
          for i,img in enumerate(image):
            #print("label.   : "+str(label[i]))
            #print("predicted: "+str(predicted[i]))
            #imshow(img)
            # WandB – Log images in your test dataset automatically, along with predicted and true labels by passing pytorch tensors with image data into wandb.Image
            example_images.append(wandb.Image(img, caption="Pred: {} Truth: {}".format(predicted[i], label[i])))

      test_acc = 100. * correct / len(dataloaders_dict["test"].dataset)
      # WandB – wandb.log(a_dict) logs the keys and values of the dictionary passed in and associates the values with a step.
      # You can log anything by passing it to wandb.log, including histograms, custom matplotlib objects, images, video, text, tables, html, pointclouds and other 3D objects.
      # Here we use it to log test accuracy, loss and some test images (along with their true and predicted labels).
      wandb.log({
          "Examples": example_images,
          "Test Accuracy": test_acc,
          "Test Loss": 100-test_acc})
            
      print('Test Accuracy of the model: {} %'.format(100 * correct / total))
  return model

def train_model(model, dataloaders, criterion, optimizer, num_epochs=25, is_inception=False):
    print("train")

    since = time.time()

    val_acc_history = []

    best_model_wts = copy.deepcopy(model.state_dict())
    best_acc = 0.0

    for epoch in range(num_epochs):
        #print('Epoch {}/{}'.format(epoch, num_epochs - 1))
        #print('-' * 10)

        # Each epoch has a training and validation phase
        for phase in ['train', 'valid']:
            if phase == 'train':
                model.train()  # Set model to training mode
            else:
                model.eval()   # Set model to evaluate mode

            running_loss = 0.0
            running_corrects = 0

            # Iterate over data.
            for inputs, labels in dataloaders[phase]:
                inputs = inputs.to(device)
                labels = labels.to(device)

                # zero the parameter gradients
                optimizer.zero_grad()

                # forward
                # track history if only in train
                with torch.set_grad_enabled(phase == 'train'):
                    # Get model outputs and calculate loss
                    # Special case for inception because in training it has an auxiliary output. In train
                    #   mode we calculate the loss by summing the final output and the auxiliary output
                    #   but in testing we only consider the final output.
                    if is_inception and phase == 'train':
                        # From https://discuss.pytorch.org/t/how-to-optimize-inception-model-with-auxiliary-classifiers/7958
                        outputs, aux_outputs = model(inputs)
                        loss1 = criterion(outputs, labels)
                        loss2 = criterion(aux_outputs, labels)
                        loss = loss1 + 0.4*loss2
                    else:
                        outputs = model(inputs)
                        loss = criterion(outputs, labels)

                    _, preds = torch.max(outputs, 1)

                    # backward + optimize only if in training phase
                    if phase == 'train':
                        loss.backward()
                        optimizer.step()

                # statistics
                running_loss += loss.item() * inputs.size(0)
                running_corrects += torch.sum(preds == labels.data)

            epoch_loss = running_loss / len(dataloaders[phase].dataset)
            epoch_acc = running_corrects.double() / len(dataloaders[phase].dataset)

            # WandB – wandb.log(a_dict) logs the keys and values of the dictionary passed in and associates the values with a step.
            # You can log anything by passing it to wandb.log, including histograms, custom matplotlib objects, images, video, text, tables, html, pointclouds and other 3D objects.
            # Here we use it to log test accuracy, loss and some test images (along with their true and predicted labels).
            wandb.log({
                phase+" Loss": epoch_loss,
                phase+" Accuracy": epoch_acc})

            #print('{} Loss: {:.4f} Acc: {:.4f}'.format(phase, epoch_loss, epoch_acc))

            # deep copy the model
            if phase == 'valid' and epoch_acc > best_acc:
                best_acc = epoch_acc
                best_model_wts = copy.deepcopy(model.state_dict())
            if phase == 'valid':
                val_acc_history.append(epoch_acc)

    time_elapsed = time.time() - since
    print('Training complete in {:.0f}m {:.0f}s'.format(time_elapsed // 60, time_elapsed % 60))
    print('Best val Acc: {:4f}'.format(best_acc))


    #test_model(model, dataloaders)
    # load best model weights
    # load final model to be able to see differences in wandb
    # model.load_state_dict(best_model_wts)
    return model, val_acc_history

def set_parameter_requires_grad(model, feature_extracting):
    if feature_extracting:
        for param in model.parameters():
            param.requires_grad = False

def initialize_model(model_name, num_classes, feature_extract, use_pretrained=True):
    print("initialize")
    # Initialize these variables which will be set in this if statement. Each of these
    #   variables is model specific.
    model_ft = None
    input_size = 0

    if model_name == "Resnet18":
        """ Resnet18
        """
        model_ft = models.resnet18(pretrained=use_pretrained)
        set_parameter_requires_grad(model_ft, feature_extract)
        num_ftrs = model_ft.fc.in_features
        model_ft.fc = nn.Linear(num_ftrs, num_classes)
        input_size = 224

    elif model_name == "Resnet":
        """ Resnet18
        """
        model_ft = models.resnet18(pretrained=use_pretrained)
        set_parameter_requires_grad(model_ft, feature_extract)
        num_ftrs = model_ft.fc.in_features
        model_ft.fc = nn.Linear(num_ftrs, num_classes)
        input_size = 224

    elif model_name == "Alexnet":
        """ Alexnet
        """
        model_ft = models.alexnet(pretrained=use_pretrained)
        set_parameter_requires_grad(model_ft, feature_extract)
        num_ftrs = model_ft.classifier[6].in_features
        model_ft.classifier[6] = nn.Linear(num_ftrs,num_classes)
        input_size = 224

    elif model_name == "VGG11_bn":
        """ VGG11_bn
        """
        model_ft = models.vgg11_bn(pretrained=use_pretrained)
        set_parameter_requires_grad(model_ft, feature_extract)
        num_ftrs = model_ft.classifier[6].in_features
        model_ft.classifier[6] = nn.Linear(num_ftrs,num_classes)
        input_size = 224

    elif model_name == "Squeezenet":
        """ Squeezenet
        """
        model_ft = models.squeezenet1_0(pretrained=use_pretrained)
        set_parameter_requires_grad(model_ft, feature_extract)
        model_ft.classifier[1] = nn.Conv2d(512, num_classes, kernel_size=(1,1), stride=(1,1))
        model_ft.num_classes = num_classes
        input_size = 224

    elif model_name == "Densenet":
        """ Densenet
        """
        model_ft = models.densenet121(pretrained=use_pretrained)
        set_parameter_requires_grad(model_ft, feature_extract)
        num_ftrs = model_ft.classifier.in_features
        model_ft.classifier = nn.Linear(num_ftrs, num_classes) 
        input_size = 224

    elif model_name == "Inception v3":
        """ Inception v3 
        Be careful, expects (299,299) sized images and has auxiliary output
        """
        model_ft = models.inception_v3(pretrained=use_pretrained)
        set_parameter_requires_grad(model_ft, feature_extract)
        # Handle the auxilary net
        num_ftrs = model_ft.AuxLogits.fc.in_features
        model_ft.AuxLogits.fc = nn.Linear(num_ftrs, num_classes)
        # Handle the primary net
        num_ftrs = model_ft.fc.in_features
        model_ft.fc = nn.Linear(num_ftrs,num_classes)
        input_size = 299

    else:
        print("Invalid model name, exiting...")
        exit()
    
    return model_ft, input_size

"""###Train

Setting Hyperparameters
"""

default_config = {  
        'batch_size': 12,
        'epochs':30,
        'lr':0.0005,
        'model_name': 'Resnet18',
        'momentum' : 1.2,
        'use_pretrained': 'True',
        'num_workers' : 4,
        'num_classes': 3,
        'dataset_color': 'white'
    }

wandb.init(config=default_config, project="pytorch-TWI_spaghetti_sweep")
config = wandb.config


def run():
    # WandB – Initialize a new run
    #run = wandb.init(config=sweep_config,project="pytorch-TWI_second_handmade_sweep")
    #wandb.watch_called = False # Re-run the model without restarting the runtime, unnecessary after our next release

    #config = wandb.config          # Initialize config
    #config = default_config

    if config.dataset_color == 'red':
      dataloaders_dict = {x: torch.utils.data.DataLoader(red_datasets[x], batch_size=config.batch_size, shuffle=True, num_workers=config.num_workers) for x in ['train', 'valid', 'test']}
    if config.dataset_color == 'white':
      dataloaders_dict = {x: torch.utils.data.DataLoader(white_datasets[x], batch_size=config.batch_size, shuffle=True, num_workers=config.num_workers) for x in ['train', 'valid', 'test']}

      # Initialize the pretrained version of the model used for this run
    pt_model,_ = initialize_model(config.model_name, config.num_classes, feature_extract=False, use_pretrained=config.use_pretrained)
    pt_model = pt_model.to(device)
    pt_optimizer = optim.SGD(pt_model.parameters(), lr=config.lr, momentum=config.momentum)
    pt_criterion = nn.CrossEntropyLoss()
    _,pt_hist = train_model(pt_model, dataloaders_dict, pt_criterion, pt_optimizer, num_epochs=config.epochs, is_inception=(config.model_name=="inception"))

    test_model(pt_model, dataloaders_dict)

    # WandB – Save the model checkpoint. This automatically saves a file to the cloud and associates it with the current run.
    torch.save(pt_model.state_dict(), os.path.join(models_path,'model.h5'))
    wandb.save(os.path.join(models_path,'model.h5'))

    #run.finish()

# use this run function call to test after changes and see full stack trace
#run()



# Initialize a new sweep
# Arguments:
#     – sweep_id: the sweep_id to run - this was returned above by wandb.sweep()
#     – function: function that defines your model architecture and trains it
#wandb.agent(sweep_id, run, count=50)

if __name__ == '__main__':
   run()