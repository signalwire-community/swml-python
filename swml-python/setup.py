from setuptools import setup, find_packages

version = "1.0"

setup(
    name='swml-python',
    version=version,
    install_requires=[
        "PyYAML ~= 6.0"
    ],
    packages=find_packages(exclude=('tests', 'tests.*')),
    description='A Python wrapper for the new SignalWire product SWML (SignalWire MarkUp Language) ',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Devon White',
    author_email='devon.white@signalwire.com',
    url='https://github.com/Devon-White/SWML-python',
    license='LICENSE.txt',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Multimedia :: Sound/Audio :: Speech',
        'Topic :: Communications :: Telephony',
    ],
)
