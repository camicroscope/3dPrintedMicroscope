from PIL import Image
import os

im=Image.open('demo.png')
wpercent=(300/float(im.size[0]))
hsize=int((float(im.size[1]*float(wpercent))))
img=im.resize((300,hsize),Image.ANTIALIAS)
img.save('someimage.png')

print(os.path.exists("./static/stage_images/"+"60b6536846c2380032744ccf_stage_3.png"))
