from setuptools import setup, find_packages

setup(
    name='houdiniUtils',
    version='0.1.0',
    packages=find_packages(include=['houdiniutils', 'houdiniutils.*']),
    include_package_data=True,
    package_data={
        'houdiniutils.textureTools': ['textureID.json', 'houUtils.shelf'],
    },
    install_requires=[
        # Add any dependencies here, if necessary
    ],
    author='Suhail',
    author_email='suhailece@gmail.com',
    description='A collection of utilities for Houdini',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/suhailphotos/houdiniUtils',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)
