import setuptools


with open('README.md', 'r') as fh:
    long_description = fh.read()


setuptools.setup(
    name='minirobots-turtle',
    version='0.2.1',
    author='Leo Vidarte',
    author_email='lvidarte@gmail.com',
    description='Python client for Minirobots Turtle Robot (includes Jupyter tutorial)',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://gitlab.com/minirobots/minirobots-turtle',
    packages=[
        'minirobots',
        'minirobots-tutorial'
    ],
    package_data={
        'minirobots': ['minirobots/**/*'],
        'minirobots-tutorial': [
            'minirobots-tutorial/**/*',
            'minirobots-tutorial/.jupyter/**/*'
        ],
    },
    include_package_data=True,
    scripts=[
        'bin/minirobots-shell',
        'bin/minirobots-tutorial'
    ],
    setup_requires=[
        'flake8'
    ],
    install_requires=[
        'requests==2.24.0',
        'jupyter==1.0.0',
        'ipython==7.17.0',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
 )
