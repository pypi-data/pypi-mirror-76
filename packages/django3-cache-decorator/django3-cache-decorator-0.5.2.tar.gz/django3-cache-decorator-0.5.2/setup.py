from setuptools import setup
from os import path
here = path.abspath(path.dirname(__file__))

version = '0.5.2'
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name = 'django3-cache-decorator',
    packages = ['django_cache_decorator'],
    license = 'MIT',
    version = version,
    description = 'Easily add caching to functions within a django project.',
    long_description=long_description,
    long_description_type="markdown",
    author = 'Richard Caceres',
    author_email = 'me@rchrd.net',
    url = 'https://github.com/ramwin/django-cache-decorator/',
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    data_files=[('README.md', ['README.md'])],
    keywords = "django caching decorator",
)
