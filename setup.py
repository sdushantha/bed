import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='bed',
    version='21.05.2020',
    author='Siddharth Dushantha',
    author_email='siddharth.dushantha@gmail.com',
    description='A very simple command line Browser Extension Downloader',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/sdushantha/bed',
    entry_points={'console_scripts': ['bed=bed.__main__:main']},
    install_requires=['requests', 'colorama', 'bs4', 'lxml'],
    packages=['bed']
)

