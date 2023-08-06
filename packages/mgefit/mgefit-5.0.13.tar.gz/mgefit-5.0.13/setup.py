from setuptools import setup, find_packages
import re

package = "mgefit"

def find_version(package):
    version_file = open(package + "/__init__.py").read()
    rex = r'__version__\s*=\s*[\'"]([^\'"]*)[\'"]'
    return re.search(rex, version_file).group(1)

setup(name=package,
      version=find_version(package),
      description='MgeFit: Multi-Gaussian Expansion Fitting',
      long_description=open("README.rst").read(),
      long_description_content_type='text/x-rst',
      url='http://purl.org/cappellari/software',
      author='Michele Cappellari',
      author_email='michele.cappellari@physics.ox.ac.uk',
      license='Other/Proprietary License',
      packages=find_packages(),
      package_data={'': ['*.txt', '*.pdf',  'images/*.fits']},
      install_requires=['numpy', 'scipy', 'matplotlib', 'astropy'],
      classifiers=["Development Status :: 5 - Production/Stable",
                   "Intended Audience :: Developers",
                   "Intended Audience :: Science/Research",
                   "Operating System :: OS Independent",
                   "Programming Language :: Python :: 3"],
      zip_safe=True)
