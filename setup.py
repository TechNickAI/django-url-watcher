import os
from setuptools import setup, find_packages

ROOT = os.path.abspath(os.path.dirname(__file__))

setup(
    name='django-url-watcher',
    version='0.1',
    description='Django app to poll urls and check their contents',
    long_description=open(os.path.join(ROOT, 'README')).read(),
    author='Nick Sullivan',
    author_email='nick@sullivanflock.com',
    url='http://github.com/gorillamania/django-url-watcher',
    license='None yet',
    packages=find_packages(exclude=['testapp','testapp/*']),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
