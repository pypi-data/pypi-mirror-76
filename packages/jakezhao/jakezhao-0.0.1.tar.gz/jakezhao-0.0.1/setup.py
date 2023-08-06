# from setuptools import setup
# setup(name='jakezhao',
#       version='0.1',
#       description='Help you survive from AM2 by Prof. Jake Zhao',
#       url='http://github.com/Pangbo15/jakezhao',
#       author='PangBo',
#       author_email='niko@pku.edu.cn',
#       license='MIT',
#       packages=,['jakezhao','filter']
#       zip_safe=False)

import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="jakezhao",
  version="0.0.1",
  author="Niko",
  author_email="niko@pku.edu.cn",
  description="Help you survive from AM2 by Prof.JakeZhao",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/pypa/sampleproject",
  packages=setuptools.find_packages(),
  classifiers=[
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
  ],
)