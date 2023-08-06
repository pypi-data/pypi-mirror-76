from distutils.core import setup

version = '0.0.7'
name = 'swagger_integration_tests'
url = f'https://github.com/SamuelJansen/{name}/'

setup(
    name = name,
    packages = [
        name,
        f'{name}/api',
        f'{name}/api/src',
        f'{name}/api/src/service'
    ],
    version = version,
    license = 'MIT',
    description = 'python swagger integration tests helper',
    author = 'Samuel Jansen',
    author_email = 'samuel.jansenn@gmail.com',
    url = url,
    download_url = f'{url}archive/v{version}.tar.gz',
    keywords = ['swagger', 'python swagger helper', 'python swagger', 'swagger helper'],
    install_requires = [
        'python_helper',
        'python_selenium_helper'
    ],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8'
    ]
)
