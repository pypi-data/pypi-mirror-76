from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='wrapdll',
    version='0.1',
    author='YuvalZ',
    author_email='YuvalZan@dev.nul',
    description='Allows using python annotaions to wrap dlls using ctypes',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/YuvalZan/wrapdll',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    keywords='ctypes wrapper wrap',
    test_suite="wrapdll.tests",
    python_requires='>=3.6',
)
