"""
    
"""
from os import path
from codecs import open
from setuptools import setup

basedir = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(basedir, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='hello_image',
    version='0.0.0',
    url='https://github.com/hadi-muhammad/hello_image',
    license='MIT',
    author='Me',
    author_email='',
    description='test image for pypi docs',
    long_description=long_description,
    long_description_content_type='text/markdown',
    platforms='any',
    packages=['hello_image'],
    zip_safe=False,
    test_suite='test_image',
    include_package_data=True,
    install_requires=[
        'Flask'
    ],
    extras_require={
        'dev': [
            'coverage',
            'flake8',
            'tox',
        ],
     },
    keywords='flask extension development',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
