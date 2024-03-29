import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-peanut-store',
    version='0.0.1',
    packages=find_packages(exclude=["django_peanut_store"]),
    include_package_data=True,
    license='Apache-2.0 License',  # example license
    description='Inventory & Vending apps for Django.',
    long_description=README,
    url='https://github.com/softapr/django-peanut-store',
    author='Francisco Prieto',
    author_email='ifr.prieto@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.2.1',
        'Framework :: Django :: 2.2.4',  # replace "X.Y" as appropriate
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache-2.0 License',  # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)