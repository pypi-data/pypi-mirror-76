from distutils.core import setup

setup(
  name = 'google_img_downloader',         # How you named your package folder (MyLib)
  packages = ['google_img_downloader',],   # Chose the same as "name"
  version = '0.3',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'google_img_downloader is a Python library that allow to download automatically image from google-image',   # Give a short description about your library
  author = 'TABARO Christian',                   # Type in your name
  author_email = 'tabarochristian@yahoo.com',      # Type in your E-Mail
  url = 'https://github.com/tbro2020/image-google-downloader',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/tbro2020/image-google-downloader',    # I explain this later on
  keywords = ['google', 'image', 'download','python','webdriver'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
    'pillow',
    'selenium',
    'urllib3',
  ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)