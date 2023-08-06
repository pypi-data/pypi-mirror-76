from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='awsreport',
    author="Gabriel 'bsd0x' Dutra",
    author_email="gmdutra.bsd@gmail.com",
    version='3.0.0',
    description="AWSReport is a tool for analyzing amazon resources.",
    include_package_data=True,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bsd0x/awsreport",
    packages=find_packages(include=['awsreport', 'awsreport.*']),
    entry_points={"console_scripts": ["awsreport=awsreport.__main__:main"]},
    keywords=["aws", "report", "amazon"],
    install_requires = [
        'boto3',
        'colorama'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
        "Topic :: Communications :: Email"
    ],
    zip_safe=False
)
