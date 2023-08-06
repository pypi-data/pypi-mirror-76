import setuptools

with open("README.md", "r") as fh:

    long_description = fh.read()

setuptools.setup(

     name='Img2UrlApi',

     version='0.2',

     author="Patryk Organisciak",

     author_email="patrykorganisciak@gmail.com",

     description="Img2Url-Api for images hosting",

     long_description=long_description,

    long_description_content_type="text/markdown",

     url="https://github.com/Vitz/Img2Url-API",

     packages=setuptools.find_packages(),

     classifiers=[

         "Programming Language :: Python :: 3",

         "License :: OSI Approved :: MIT License",

         "Operating System :: OS Independent",

     ],

 )