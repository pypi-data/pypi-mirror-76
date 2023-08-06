import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='minirobots-turtle',
    version='0.1',
    scripts=['bin/minirobots-shell'],
    author="Leo Vidarte",
    author_email="lvidarte@gmail.com",
    description="Python client for Minirobots Turtle Robot",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/minirobots/minirobots-turtle",
    packages=setuptools.find_packages(),
    install_requires=[
        "requests==2.24.0",
        "jupyter==1.0.0",
        "ipython==7.17.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
#    entry_points={
#        "console_scripts": [
#            "minirobots-shell=minirobots.__init__:shell",
#        ]
#    },
 )
