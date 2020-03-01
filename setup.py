from setuptools import setup, find_packages

about = {}
with open('pping/__about__.py', encoding='utf8') as f:
    exec(f.read(), about)

with open('README.md', encoding='utf8') as f:
    readme = f.read()

setup(
    name=about['__name'],
    version=about['__version'],
    author=about['__author'],
    description=about['__description'],
    long_description=readme,
    long_description_content_type='text/markdown',
    url=about['__url'],
    license=about['__license'],
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ],
    python_requires='>=3.6',
)
