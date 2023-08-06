"""
/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-08-13 17:20:35
 * @modify date 2020-08-13 17:26:18
 * @desc [
    Setup for AlexaUtils PyPi
 ]
 */
"""


##########
# Imports
##########

from setuptools import setup, find_packages


##########
# Setup variabless
##########

name = "alexautils"
version = "0.0.1"
description = "Utility methods to supplement Python ASK SDK"
author = "Jai Miles"
author_email = "jaimiles23@gmail.com"
keywords = ['Alexa', 'ssml', 'ask sdk']
url = 'https://github.com/jaimiles23/Alexa-Utils'
download_url = ''


##########
# Read files
##########

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()


##########
# SetUp args
##########

setup_args = dict(
    name = name,
    version = version,
    description = description,
    long_description_content_type = "text/markdown",
    long_description = README + '\n\n' + HISTORY,
    license = 'MIT',
    packages = find_packages(),
    author = author,
    author_email = author_email,
    keywords = keywords,
    url = url,
    download_url = download_url,
)


##########
# Requirements
##########

install_requires = [
    'ask-sdk-core == 1.11.0'
]


##########
# Setup
##########

if __name__ == '__main__':
    setup(**setup_args, install_requires = install_requires)