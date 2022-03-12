from setuptools import setup, find_packages


setup(
    name='PortalNJAU',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        "httpx==0.22.0",
        "Pillow==9.0.1",
        "lxml==4.8.0",
        "bs4==0.0.1",
        "beautifulsoup4==4.10.0",
        "pycryptodome==3.14.1",
    ],
    url='https://github.com/spongxin/njau-portal-interface',
    license='MIT License',
    author='spongxin',
    author_email='spongxin@yeah.net',
    description='Portal crawler interface supporting asynchronous processing for NJAU'
)