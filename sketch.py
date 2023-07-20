
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

import os
import requests

import cv2
import numpy as np
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 

# instance of Options class allows
# us to configure Headless Chrome
options = Options()
  
# this parameter tells Chrome that
# it should be run without UI (Headless)
options.headless = True
  

MARGIN = 25

browserExe = "chrome" 
os.system("pkill "+ browserExe) 



def get_sketch(driver, filepath):
    sketch_image_path = filepath.replace(r'.png', r'_sketch.png')
    if os.path.isfile(sketch_image_path): 
        return sketch_image_path

    driver.get("https://www.photo-kako.com/en/sketch/")
    driver.find_element(By.XPATH,"/html/body/header/div[2]/span").click()
    driver.find_element_by_id("inputfile").send_keys(os.getcwd()+'/'+filepath)

    # get image url
    image_url = driver.find_element(By.XPATH,'//*[@id="image"]').get_attribute('data-src')
    print(image_url)
    # save image
    img_data = requests.get(image_url).content

    
    with open(sketch_image_path, 'wb') as handler:
        handler.write(img_data)
    return sketch_image_path




def upscale(img, ratio):
    print('Original Dimensions : ',img.shape)
    scale_percent = ratio # percent of original size
    print(ratio)

    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
      
    # resize image
    resized = cv2.resize(img, dim, interpolation = cv2.INTER_CUBIC)
     
    #---Sharpening filter----
    kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    img_sharpened = cv2.filter2D(resized, -1, kernel)

    print('Resized Dimensions : ',img_sharpened.shape)

    return img_sharpened


def put_a4(image_path, sketch_image_path, text):
    a4  = Image.open("a4.png")
    width_a4, height_a4 = a4.size

    sketch = cv2.imread(sketch_image_path, cv2.IMREAD_UNCHANGED)
    height_sketch, width_sketch = sketch.shape
    sketch = upscale(sketch, ratio=(width_a4-MARGIN*2)*100/width_sketch)

    # You may need to convert the color.
    sketch = cv2.cvtColor(sketch, cv2.COLOR_BGR2RGB)
    sketch_pil = Image.fromarray(sketch)
    width_sketch_pil, height_sketch_pil = sketch_pil.size

    # paste sketch
    Image.Image.paste(a4, sketch_pil, (MARGIN, height_a4-height_sketch_pil-MARGIN))

    # resize original image
    org_img = Image.open(image_path)
    org_img_width, org_img_height = org_img.size

    new_org_img_height = int(height_a4-height_sketch_pil-MARGIN*3)
    new_org_img_width = int((new_org_img_height/org_img_height)*org_img_width)
    
    org_img = org_img.resize((new_org_img_width, new_org_img_height))

    # paste original image
    Image.Image.paste(a4, org_img, (MARGIN*3, MARGIN))

    # add text
    draw = ImageDraw.Draw(a4)
    

    text_box_size = width_a4-new_org_img_width-MARGIN*7, height_a4-height_sketch_pil-MARGIN*5
    font_size = 1000

    if len(text.split('\n'))==2:
        line1, line2 = text.split('\n')
    else:
        line1 = text.split('\n')
        line2 = ''

    while True:
        font = ImageFont.truetype("Roboto-Medium.ttf", font_size)
        line1_text_width, line1_text_height = draw.textsize(line1, font=font)
        line2_text_width, line2_text_height = draw.textsize(line2, font=font)

        text_width = max([line1_text_width, line2_text_width])
        text_height = line1_text_height + line2_text_height + MARGIN

        if (text_width<text_box_size[0]) and (text_height<text_box_size[1]):
            break
        else:
            font_size = font_size-20

    
    draw.text((new_org_img_width + MARGIN*5 + (width_a4 - (new_org_img_width + MARGIN*7) - line1_text_width)/2, (height_a4 - height_sketch_pil - 2*MARGIN - text_height)/2),
        line1,(0,0,0),font=font)

    draw.text((new_org_img_width + MARGIN*5 + (width_a4 - (new_org_img_width + MARGIN*7) - line2_text_width)/2, (height_a4 - height_sketch_pil - 2*MARGIN - text_height)/2 + line1_text_height + MARGIN/2),
        line2,(0,0,0),font=font)
    
    font = ImageFont.truetype("Roboto-Light.ttf", 40)
    line3 = '(Nguồn: Thầy Thiện đăng trong Group FB "Kho Tiếng Anh của bọn trẻ con")'
    line3_text_width, line3_text_height = draw.textsize(line3, font=font)
    draw.text((new_org_img_width + MARGIN*5 + (width_a4 - (new_org_img_width + MARGIN*7) - line3_text_width)/2, height_a4 - height_sketch_pil-MARGIN*3),
        line3,(0,0,0),font=font)

    final_path = image_path.replace('images','finals')
    a4 = a4.save(final_path)

    return final_path



# initializing webdriver for Chrome with our options
driver = webdriver.Chrome(ChromeDriverManager().install(), 
                        desired_capabilities={}, 
                        options=options)



image_path = 'images/' + '1.png'
im = Image.open(image_path)
im = im.resize((750,int((750/im.size[0])*im.size[1])))
im.save(image_path)

sketch_image_path = get_sketch(driver, image_path)
text = "The forest"
final_path = put_a4(image_path, sketch_image_path, text)


# close browser after our manipulations
driver.close()




import sys
sys.exit()


strings = '''At the beach,
we put on sun block.

At the beach,
we play in the sea.

At the beach,
we build sand castles.

At the beach,
we chase crabs.

At the beach, we swim.

At the beach,
we go for a boat ride.

At the beach, we find shells.

At the beach,
we have a picnic.'''








data = strings.split('\n\n')


from fpdf import FPDF
pdf = FPDF()

file_count = 0
for each in data:
    print(each)
    file_count += 1
    image_path = 'images/' + str(file_count) + '.png'
    im = Image.open(image_path)
    im = im.resize((750,int((750/im.size[0])*im.size[1])))
    im.save(image_path)

    sketch_image_path = get_sketch(driver, image_path)
    text = each
    final_path = put_a4(image_path, sketch_image_path, text)

    pdf.add_page()
    pdf.image(final_path,0,0,209)

pdf.output("2A - At the beach.pdf", "F")



# close browser after our manipulations
driver.close()