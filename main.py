import discord
import os
from discord.ext import commands
import pandas as pd
import numpy as np
import requests
import shutil
import uuid
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.models import Model
from pathlib import Path
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm_notebook as tqdm

import asyncio

client =  discord.Client(intents=discord.Intents.default())
bot = commands.Bot(command_prefix='.', intents=discord.Intents.default())


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    message.channel.send('Hello! I am your Virtual Shopping Assistant. Do you want to try it out ?')
    if message.content.startswith(('hello', 'Hello', 'Hi')):
        await message.channel.send('Hello! I am your Virtual Shopping Assistant. I can find products similar to the image of product you upload. Do you want to try it out ?')
    if message.content.startswith(('Yes', 'yes', "YES")):
            await message.channel.send('Please upload the product image.')    
    if message.content.startswith(('No', 'no', 'NO')):
        await message.channel.send('Sad to see you go.')          
        
    if (message.attachments[0]):
            await message.channel.send("Product image has been received. Please wait for the top 5 similar products.")
            url = message.attachments[0].url            # check for an image, call exception if none found
                
    else:
            print("Error: No attachments")
            await message.channel.send("No attachments detected!") 
            
                
            
    if url[0:26] == "https://cdn.discordapp.com":   # look to see if url is from discord
                        r = requests.get(url, stream=True)
                        imageName = str(uuid.uuid4()) + '.jpg'      # uuid creates random unique id to use for image names
                        with open('/Users/jyotibhandari/Documents/Machine Learning /Project/Inputimages_from_bot/'+imageName, 'wb') as out_file:
                            print('Saving image: ' + imageName)
                            shutil.copyfileobj(r.raw, out_file)     # save image (goes to project directory)
                        
    class Feature_Extractor:
        def __init__(self):
            
            # Using the VGG-16 as the model/architecture and ImageNet as the weight
            basicmodel = VGG16(weights='imagenet')
            
            # Customizing the model for returning the features from a fully-connected layer
            self.model = Model(inputs=basicmodel.input, outputs=basicmodel.get_layer('fc1').output)
        
        def extract_image(self, img_file):
            # Resizing the image
            img_file = img_file.resize((224, 224))
            # Converting the image color space
            img_file = img_file.convert('RGB')
            # Reformatting the image by converting the image to array and preprocessing the image
            img_array = image.img_to_array(img_file)
            img_array = np.expand_dims(img_array, axis=0)
            img_array = preprocess_input(img_array)
            # Extract Features
            feature = self.model.predict(img_array)[0]
            return feature / np.linalg.norm(feature)

    Input_image= Image.open('/Users/jyotibhandari/Documents/Machine Learning /Project/Inputimages_from_bot/'+ imageName  )
    print (Input_image)  
    features_data_df = pd.read_csv("/Users/jyotibhandari/Documents/Machine Learning /Project/feature_extraction.csv")
    
    
    f_e = Feature_Extractor()
    query = f_e.extract_image(Input_image)
    # Calculate the  distance (similarity) between the images based on the features
    features_data = features_data_df.drop(columns = ['image'])
    features_data = features_data.values
    distance = np.linalg.norm(features_data - query, axis=1)

    # Extract 20 images that have lowest distance
    ids = np.argsort(distance)[:30]
    similar_imgs = features_data_df.iloc[ids,:]['image']
    scores = pd.DataFrame({'image': similar_imgs,
                        'img_distance': distance[ids]})
    scores = scores.reset_index(drop=True)

    
    files=[]
    await message.channel.send('The Top five Similar Products Are: ')
    for i in range(5*1):
        score = scores['img_distance'][i]
        files.append ('/Users/jyotibhandari/Documents/Machine Learning /Project/Flipkart_images_final/' + scores['image'][i])
        await message.channel.send(file=discord.File(files[i])) 

    if message.content.startswith(('Bye', 'BYE', 'bye')):
        await message.channel.send('Bye! Thank you for trying this feature. ') 

client.run('MTA1MDEwOTU1Njg1ODA0ODU1NQ.G7h5lT.K00ruNJ4THASOSFC-bYcZiJRmIABhEc217VmMA')

