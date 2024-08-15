from setuptools import setup, find_packages

setup(
    name='houdiniutils',
    version='0.1.5',
    description='All related tools and utilities',
    author='Suhail',
    author_email='suhailece@gmail.com',
    license='MIT',
    packages=find_packages(),
    install_requires=[],
    python_requires='>=3.10.10',
    entry_points={
        'console_scripts': [
            'houdiniutils_post_install = houdiniutils.post_install:post_install',
        ],
    },
)
