from random import randint
from PIL import Image, ImageDraw

for x in range(50):
    redValue = randint(0, 255) 
    greenValue = randint(0, 255) 
    blueValue = randint(0, 255) 
    
    fileName = str("./allColors/pic") + str(x) + str(".png")

    img = Image.new(mode="RGB", size=(400, 400), color=(redValue, greenValue, blueValue))
    
    imgValue = str("Value: ") + str(x)
    imageDraw = ImageDraw.Draw(img)
    imageDraw.text((200, 200), imgValue, fill=(255, 255, 255))
    
    img.save(fileName, format="PNG")
