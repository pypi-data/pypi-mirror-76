import codecs
import os

from setuptools import setup


with open("README.md", "r") as fh:
    long_description = fh.read()


NAME = "qy_ip_parse"

PACKAGES = ["qy_ip_parse", ]


DESCRIPTION = "qy ip parse."

LONG_DESCRIPTION = long_description
LONG_DESCRIPTION_CONTENT_TYPE = 'text/markdown'

KEYWORDS = "python qy ip parse"

AUTHOR = "chenxiaolong"

AUTHOR_EMAIL = "cxiaolong6@gmail.com"


URL = ''

VERSION = "0.0.6"

LICENSE = "MIT"

INSTALL_REQUIRES = ["ipip-ipdb", "ipaddress", "oss2", 'redis']

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESCRIPTION_CONTENT_TYPE,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ],
    keywords=KEYWORDS,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    license=LICENSE,
    install_requires=INSTALL_REQUIRES,
    packages=PACKAGES,
    include_package_data=True,
    zip_safe=True,
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*",
)
