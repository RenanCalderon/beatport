from setuptools import setup, find_packages

setup(
    name='beatport',
    version='0.0.1',
    description='Beatport Music Scraper',
    author='Renan Calderon',
    author_email='renan.cnv@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'beautifulsoup4',
        'requests',
        'mutagen',
        'python-Levenshtein',
    ],
)
