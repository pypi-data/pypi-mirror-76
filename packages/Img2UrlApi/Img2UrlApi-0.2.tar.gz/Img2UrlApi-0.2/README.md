# Img2Url-API

API for image hosting eg. www.img2url.site

#Example:
###  import ###
from ImgUploader import ImgUploader

### init ###
url = "http://www.vitz.usermd.net"  
user_key = "LXJdKWdqR2UEfaOcgLdAupYlFXY"    
sec_key = "KMEXnv5PTvmevfIsZbv5Igo7Guc"  
img_uploader = ImgUploader(url, user_key, sec_key)    

### upload ###
for i in range(100):    
    print(i)    
    img_uploader.post_image("test.jpg")

### get ###
img = img_uploader.get_image(107)   
print(img)

### get all ###
imgs = img_uploader.get_images()    
print(imgs)

### remove ###
print(img_uploader.remove_image(109))

### removel all ###
print(img_uploader.remove_all())

