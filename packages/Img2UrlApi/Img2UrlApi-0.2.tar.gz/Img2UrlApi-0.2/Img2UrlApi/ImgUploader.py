import base64
import json

from PIL import Image
import io

import requests

class ImgUploader:
    # urls
    POST_IMG = "/api/images"  # as base64
    GET_IMG = "/api/image"  # /id
    DEL_IMG = "/api/image"  # /id
    GET_ALL_IMG = "/api/images"
    COMPRESS = "/api/image/compress"  # /id/value not tested

    def __init__(self, base_url, userkey, seckey):
        self.url = base_url
        self.user_key = userkey
        self.sec_key = seckey

    def get_image(self, id):
        try:
            url = self.url + self.GET_IMG + "/" + str(id)
            headers = {"userkey": self.user_key, "seckey": self.sec_key}
            x = requests.get(url, headers=headers)
            return json.loads(x.text)
        except Exception as e:
            print("cant get image")
            print(e)

    def post_image(self, filepath):
        try:
            url = self.url + self.POST_IMG
            headers = {"userkey": self.user_key, "seckey": self.sec_key}
            bytes = self.__load_image_from_file(filepath)
            string = bytes.decode('utf-8')
            data = {"img_base64": "data:image/png;base64," + string}
            x = requests.post(url, data=data, headers=headers)
            return json.loads(x.text)
        except Exception as e:
            print("cant add image")
            print(e)

    def get_images(self):
        try:
            url = self.url + self.GET_ALL_IMG
            headers = {"userkey": self.user_key, "seckey": self.sec_key}
            x = requests.get(url, headers=headers)
            return json.loads(x.text)
        except Exception as e:
            print("cant get image")
            print(e)

    def remove_image(self, id):
        try:
            url = self.url + self.DEL_IMG + "/" + str(id)
            headers = {"userkey": self.user_key, "seckey": self.sec_key}
            x = requests.delete(url, headers=headers)
            return json.loads(x.text)
        except Exception as e:
            print("cant remove image")
            print(e)

    def remove_all(self):
        try:
            i = []
            url = self.url + self.GET_ALL_IMG
            headers = {"userkey": self.user_key, "seckey": self.sec_key}
            x = requests.get(url, headers=headers)
            photos_obj = json.loads(x.text)["images"]
            for photo in photos_obj:
                self.remove_image(photo["id"])
                i.append(photo)
            return i
        except Exception as e:
            print("cant get and remove all images")
            print(e)


    def __load_image_from_file(self, filepath):
        with open(filepath, "rb") as imageFile:
            bytes = base64.b64encode(imageFile.read())
            return bytes
