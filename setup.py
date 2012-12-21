#
# Copyright (c) 2013, Prometheus Research, LLC
#


from setuptools import setup


NAME = "sphinxcontrib-blog"
VERSION = "0.0.1"
DESCRIPTION = "A Sphinx Blog Extension"
LONG_DESCRIPTION = open('README').read()
AUTHOR = "Kirill Simonov (Prometheus Research, LLC)"
AUTHOR_EMAIL = "xi@resolvent.net"
LICENSE = "BSD"
URL = "http://bitbucket.org/prometheus/sphinxcontrib-blog"
DOWNLOAD_URL = "http://pypi.python.org/pypi/sphinxcontrib-blog"
CLASSIFIERS = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Documentation',
        'Topic :: Text Processing',
]
PLATFORMS = 'any'
REQUIRES = ['Sphinx', 'PyRSS2Gen']
PACKAGES = ['sphinxcontrib']
ZIP_SAFE = False
INCLUDE_PACKAGE_DATA = True
NAMESPACE_PACKAGES = ['sphinxcontrib']


setup(name=NAME,
      version=VERSION,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      license=LICENSE,
      url=URL,
      download_url=DOWNLOAD_URL,
      classifiers=CLASSIFIERS,
      platforms=PLATFORMS,
      requires=REQUIRES,
      packages=PACKAGES,
      zip_safe=ZIP_SAFE,
      include_package_data=INCLUDE_PACKAGE_DATA,
      namespace_packages=NAMESPACE_PACKAGES)

