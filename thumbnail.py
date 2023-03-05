import numpy as np
from rembg import remove
import cv2
import os
from cv2 import dnn_superres
from PIL import Image,ImageDraw, ImageFont
from util import linear_gradient
font_path=os.path.join('static', 'MesloLGS NF Bold.ttf')

target_thumbnail_width=1280
target_thumbnail_height=720
text_margin=20

async def generate_thumbnail(img, title, subtitle):
    dr= dnn_superres.DnnSuperResImpl_create()
    try:
        #check if the image is valid
        input_img=img
        image_width=input_img.shape[1]

    except:
        print("Please enter the valid paath")
        exit(0)

    #remove the bg image
    removed_bg_image = remove(input_img)
    removed_bg_image1 = cv2.cvtColor(removed_bg_image, cv2.COLOR_RGBA2RGB)
    image_height = removed_bg_image1.shape[0]
    
    # upscale the image is required
    resized_img = cv2.resize(removed_bg_image1, (80, 160))
    path = 'LapSRN_x4.pb'
    dr.readModel(path)
    dr.setModel('lapsrn', 4)
    upscaled_img = dr.upsample(resized_img)
    # now taking the upscaled image and converting to pillow image
    


    #convert the image back to the pillow to add some text
    img = cv2.cvtColor(upscaled_img, cv2.COLOR_BGR2RGBA)
    final_upscaled_image=Image.fromarray(img, mode='RGBA')
    centerpiece_width = int(target_thumbnail_width/ 2)
    print("Center_piece_width", centerpiece_width)
    centerpiece_height = int((target_thumbnail_height / final_upscaled_image.width/2) * centerpiece_width)
    centerpiece_x = 0
    centerpiece_y = 0

    alpha_image = Image.new('RGBA', final_upscaled_image.size, (0, 0, 0, 0))
    alpha_draw = ImageDraw.Draw(alpha_image)
    alpha_draw.rectangle((0, 0, final_upscaled_image.size[0], final_upscaled_image.size[1]), fill=(255, 255, 255, 255))
    alpha_image.paste(final_upscaled_image, mask=final_upscaled_image)

  
    alpha_image=alpha_image.resize((centerpiece_width, centerpiece_height))
    thumbnail_image = Image.new('RGBA',(target_thumbnail_width, target_thumbnail_height), (250,250,250))

    # Add the linear gradient to the the background
    polygon = [(centerpiece_width, 0), (target_thumbnail_width, 0), (target_thumbnail_width, target_thumbnail_height), (centerpiece_width, target_thumbnail_width), (centerpiece_width, 0)]
    
    color1 = (255, 0, 0)
    color2 = (0, 255, 0)
    linear_gradient(thumbnail_image,polygon, (int(centerpiece_width), target_thumbnail_height),(int(centerpiece_width*1.5), target_thumbnail_height),color1,color2 )
    alpha_image.convert("RGBA")
    thumbnail_image.paste(alpha_image, (centerpiece_x, centerpiece_y), alpha_image)
    # Create new draw object and set font
    # Determine text box size and position
    
    text_width = int(thumbnail_image.width / 2)
    text_height = thumbnail_image.height
    draw = ImageDraw.Draw(thumbnail_image)
   

    # Split text into lines based on newline character
    text_lines = [title,subtitle]
    print(text_lines)

    # Determine maximum font size for text
    text_x = int(thumbnail_image.width / 2)
    text_y = 0
    # Set font size to maximum font size or 36 (whichever is smaller)
    for line in text_lines:
        
        horizontal_font_size = int(text_width / len(line))
        vertical_font_size=int(target_thumbnail_height/len(text_lines))
        print(horizontal_font_size, vertical_font_size)
        font_size=min(vertical_font_size, horizontal_font_size)
        font = ImageFont.truetype('./MesloLGS NF Bold.ttf',size=int(font_size))
        # Set font and text color
       
        draw.text((text_x, text_y), line, fill=(0, 0, 0), font=font)
        text_y=text_y+font_size
        

    thumbnail_image.save("images_output/image_text.png")
    open_cv_image=np.array(thumbnail_image)
    open_cv_image=open_cv_image[:,:,::-1].copy()
    
    return thumbnail_image