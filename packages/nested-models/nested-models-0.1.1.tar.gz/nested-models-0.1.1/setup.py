from os import path
from setuptools import setup, find_packages

file_path = path.abspath(path.dirname(__file__))

with open(path.join(file_path, 'README.md')) as f:
    long_description = f.read()

package_metadata = {
    'name': 'nested-models',
    'version': '0.1.1',
    'description': 'Simple Model objects that can be validated and serialized/deserialized into various formats.',
    'long_description': long_description,
    'url': 'https://github.com/renderbox/django-permafrost/',
    'author': 'Grant Viklund',
    'author_email': 'renderbox@gmail.com',
    'license': 'MIT license',
    'classifiers': [
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    'keywords': ['serialization', 'json', 'yaml'],
}

setup(
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=[],
    extras_require={
        'build': [
            'setuptools',
            'wheel',
            'twine',
        ],
        'docs': [
            'coverage',
            'Sphinx',
        ],
    },
    **package_metadata
)