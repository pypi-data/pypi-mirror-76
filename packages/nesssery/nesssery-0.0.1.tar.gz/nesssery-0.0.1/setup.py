from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Environment :: MacOS X',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='nesssery',
    version='0.0.1',
    description='A very basic calculator',
    long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.md').read(),
    url='',
    author='patrick sery',
    author_email='nesssery@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='calculator',
    packages=find_packages(),
    install_requires=['']
)
