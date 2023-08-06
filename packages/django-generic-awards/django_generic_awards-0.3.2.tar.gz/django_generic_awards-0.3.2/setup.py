from setuptools import find_packages, setup


def read(f):
    return open(f, 'r', encoding='utf-8').read()


VERSION = '0.3.2'

setup(
    name='django_generic_awards',
    version=VERSION,
    license='MIT',
    description='Django app to create and manage Awards for your Model objects.',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    author='Yuriy Tupychak',
    author_email='y.tupychak@seclgroup.com',
    packages=find_packages(exclude=['example_project*']),
    include_package_data=True,
    install_requires=['django>=3.0', 'django-tof>=0.3.2', 'Pillow>=7.2'],
    python_requires='>=3.6',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 3.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Internet :: WWW/HTTP',
    ],
)
