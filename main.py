from rembg import remove
import cv2
input_path=input("Enter the path for your image")

output_path = 'output.png'

input_img = cv2.imread(input_path)
output = remove(input_img)
img = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)
cv2.imwrite(output_path, output)