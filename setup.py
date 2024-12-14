from setuptools import setup, find_packages

setup(
    name="weather-pusher",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.1",
        "beautifulsoup4>=4.9.3", 
        "selenium>=4.0.0"
    ]
) 