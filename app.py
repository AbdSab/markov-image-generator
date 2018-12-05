from PIL import Image
import os
import json
import random

N = 2
pattern = {}

#Training for one image function
def train(image):
    #Open Image
    im = Image.open(image).convert("RGB")

    #Get the sizes
    height, width = im.size

    #Store pixels to a list
    pixels = []
    for i in range(0, width):
        for j in range(0, height):
            pixels.append( im.getpixel((j, i)) )

    #Training
    l = len(pixels)
    for i in range(0, l-N-1):

        #Turn pixel to string
        pixel_string = ""
        for j in range(i, i+N):
            pixel_string += "".join([str(x) for x in pixels[j]])
        
        if pixel_string not in pattern:
            pattern[pixel_string] = []
        
        pattern[pixel_string].append(pixels[i+N+1])

#Training phase
def training(): 
    #Train with all images
    dir = os.listdir("pokemons")
    for i in dir:
        train("pokemons/"+i)

    #Save data to json file
    with open("data.json", "w") as out:
        json.dump(pattern, out)


#Generating image
def generate():
    #Open training data
    with open("data.json", "r") as out:
        pattern = json.load(out)

    #Create new image
    width = 64
    height = 64
    im = Image.new('RGB', (width,height), (0,0,0))
    im_pixels = im.load()

    pixels = [(0,0,0) for i in range(0, width*height)]

    for i in range(N+1,  width*height):
        #Pixels to string
        pixel_string = ""
        for j in range(i-N, i):
            pixel_string += "".join([str(x) for x in pixels[j]])
        
        #Take random color from trained pattern
        if pixel_string in pattern:
            pixels[i] = random.choice(pattern[pixel_string])
        else:
            continue


    #Insert generated pixels to the image
    for i in range(width):
        for j in range(height):
            im_pixels[j,i] = tuple(pixels[width*i + j])

    #Save the image
    im.save("image.png")

training()
generate()