from rembg import remove
import cv2
from cv2 import dnn_superres
from PIL import Image,ImageDraw

target_width=1280
target_height=720
async def generate_thumbnail(img, title, subtitle):
    dr= dnn_superres.DnnSuperResImpl_create()
    try:
        input_img=img
        image_width=input_img.shape[1]
        image_height=input_img.shape[0]
        text_margin=20
    except:
        print("Please enter the valid paath")
        exit(0)



    output = remove(input_img)
    # upscale the image is required

    # now taking the upscaled image and converting to pillow image

    img = cv2.cvtColor(output, cv2.COLOR_BGR2RGBA)
    final_upscaled_image=Image.fromarray(img, mode='RGBA')
    final_upscaled_image.show()
    new_image = Image.new('RGBA',(target_width, target_height), (250,250,250))
    final_upscaled_image.convert("RGBA")
    new_image.paste(final_upscaled_image, (int(target_width/2),0),final_upscaled_image)
    drawer=ImageDraw.Draw(new_image)
    drawer.multiline_textbbox((text_margin,text_margin), title,  embedded_color=(255,0,0) )
    new_image.show()
    new_image.save("images_output/image_text.png")
    return new_image