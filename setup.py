import os


from setuptools import setup
from setuptools import find_packages

here = os.path.abspath(os.path.dirname(__file__))


with open(os.path.join(here, 'README.md')) as f:
    README = f.read()


REQUIREMENTS = [
    'GoogleAppEngineCloudStorageClient'
]

setup(
    name='serve-static',
    version='0.0.1',
    description='server static',
    author='lucemia',
    author_email='lucemia@gmail.com',
    long_description=README,
    scripts=[],
    url='https://github.com/Tagtoo/serve-static',
    packages=find_packages(),
    license='Apache 2.0',
    platforms='Posix; MacOS X; Windows',
    include_package_data=True,
    zip_safe=False,
    install_requires=REQUIREMENTS,
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet',
    ]
)
