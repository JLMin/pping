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
    license='MIT',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ],
    python_requires='>=3.6',
)
