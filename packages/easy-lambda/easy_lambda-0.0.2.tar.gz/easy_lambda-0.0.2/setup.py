
# Use this command for deploy.
#   python3 setup.py sdist bdist_wheel && python3 -m twine upload --skip-existing dist/*

import io
from setuptools import find_packages, setup
from glob import glob


slash_conv = lambda x: [p.replace("\\", "/") for p in x]
data_files = [('create', slash_conv(glob('easy_lambda/create/*'))),
              ('others', slash_conv(glob('easy_lambda/others/*')))]

setup(name='easy_lambda',
      version='0.0.2',
      description='',
      long_description="Please refer to the https://github.com/da-huin/easy_lambda",
      long_description_content_type="text/markdown",
      url='https://github.com/da-huin/easy_lambda',
      download_url='https://github.com/da-huin/easy_lambda/archive/master.zip',
      author='JunYeong Park',
      author_email='dahuin000@gmail.com',
      license='MIT',
      data_files=data_files,
      packages=find_packages(),
      install_requires=["boto3", "pyzip", "pyyaml", "pyfolder"],
      classifiers=[
          'Programming Language :: Python :: 3',
      ]
      )
