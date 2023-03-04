from rembg import remove
import cv2
from cv2 import dnn_superres
from PIL import Image,ImageDraw
target_width=1280
target_height=720

input_path=input("Enter the path for your image:\n")
input_text=input("Enter the text you want on the tumbnail:\n")
dr= dnn_superres.DnnSuperResImpl_create()
output_path = 'output.png'


input_img = cv2.imread(input_path)
image_width=input_img.shape[1]
image_height=input_img.shape[0]
text_margin=20


output = remove(input_img)
# upscale the image is required

# now taking the upscaled image and converting to pillow image

img = cv2.cvtColor(output, cv2.COLOR_BGR2RGBA)
cv2.imwrite(output_path, output)

final_upscaled_image=pil_image=Image.fromarray(img, mode='RGBA')
final_upscaled_image.show()
new_image = Image.new('RGBA',(target_width, target_height), (250,250,250))
new_image.paste(final_upscaled_image, (int(target_width/2),0))
drawer=ImageDraw.Draw(input_text, mode="RGBA")
drawer.text((text_margin,text_margin), "Hello, Image from the Image Drawer", fill=(255,0,0))
new_image.paste(final_upscaled_image)
new_image.show()
new_image.save("images_output/image_text.jpg")