from setuptools import setup

setup(
    name='dotted',
    version='0.1.2',
    author='Carlos Escribano Rey',
    author_email='carlos@nettoys.es',
    url='https://github.com/carlosescri/DottedDict',
    packages=['dotted', 'dotted.test'],
    license=open('LICENSE').read(),
    description='Access dicts and lists with a dotted path notation.',
    long_description=open('README.rst').read(),
    install_requires=['six'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: Software Development'
    ]
)
