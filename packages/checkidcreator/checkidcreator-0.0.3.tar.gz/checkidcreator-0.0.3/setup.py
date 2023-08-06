from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Education',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
]

setup(
    name='checkidcreator',
    version='0.0.3',
    description='A program to generate a random id of any length greater than 1 with a check digit.',
    long_description=open('README.txt').read() + '\n\n' +
    open('CHANGELOG.txt').read(),
    url='',
    author='Pratham Aggarwal',
    author_email='me@prathamaggarwal.com',
    license='MIT',
    classifiers=classifiers,
    keywords='id generator, check id, id creator',
    packages=find_packages(),
    install_requires=['']
)
