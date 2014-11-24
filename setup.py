from distutils.core import setup

setup(
    name='dotted',
    version='0.1.1',
    author='Carlos Escribano Rey',
    author_email='carlos@nettoys.es',
    url='https://github.com/carlosescri/DottedDict',
    packages=['dotted', 'dotted.test'],
    license=open('LICENSE').read(),
    description='Access dicts and lists with a dotted path notation.',
    long_description=open('README.txt').read(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development'
    ]
)
