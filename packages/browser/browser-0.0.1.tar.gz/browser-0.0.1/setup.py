from setuptools import setup

setup(
    name='browser',
    version='0.0.1',
    description='convenience interface for web scraping',
    url='https://github.com/frnsys/browser',
    author='Francis Tseng',
    author_email='f@frnsys.com',
    license='GPLv3',

    packages=['browser'],
    install_requires=[
        'selenium==3.141.0',
        'lxml==4.5.0',
        'cssselect==1.0.3',
        'PyVirtualDisplay==0.2.4'
    ],
)