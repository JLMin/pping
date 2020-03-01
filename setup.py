from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='pping',
    version='0.0.1',
    author='JLMin',
    description='ping in python',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/JLMin/pping',
    keywords="ping icmp socket",
    license='MIT',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows'
    ],
    python_requires='>=3.6',
)
