import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="django-url-shortening",
    version="1.0.0",
    url='https://github.com/doubletapp/django-url-shortening',
    license='BSD',
    description="A URL shortening app for Django.",
    long_description=read('README.rst'),

    author='Doubletapp',
    author_email='info@doubletapp.ru',

    packages=find_packages('src'),
    package_dir={'': 'src'},

    install_requires=['setuptools', 'six'],

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
    ]
)
