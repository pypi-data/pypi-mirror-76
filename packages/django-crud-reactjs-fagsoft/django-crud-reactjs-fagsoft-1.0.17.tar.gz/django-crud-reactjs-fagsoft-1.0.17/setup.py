from setuptools import find_packages
from setuptools import setup

setup(
    name="django-crud-reactjs-fagsoft",
    version="1.0.17",
    packages=find_packages(),
    install_requires=[
        'djangorestframework>=3.11.0',
        'django-rest-knox>=3.1.4',
        'django-imagekit>=4.0.2',
        'pilkit>=2.0',
        'django>=3.0.6',
        'django-webpack-loader>=0.7.0',
        'django-silk>=4.0.1',
        'Pillow>=7.1.0',
        'cryptography>=2.9',
    ],
    long_description="file: README.rst",
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django :: 3.0',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP'
    ],
    author="Fabio A Garcia S",
    author_email="fabio.garcia.sanchez@gmail.com",
    description="A Django app create apps with reactjs",
    license="PSF",
    include_package_data=True
)
