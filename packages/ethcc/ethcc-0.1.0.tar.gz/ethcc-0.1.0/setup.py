from distutils.core import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
  name = 'ethcc',
  packages = ['ethcc'],
  version = '0.1.0',
  license='MIT',
  description = 'Ethereum smart contracts interface on top of web3py',
  author = 'origliante',
  author_email="please.visit.github@page.nowhere",
  url = 'https://github.com/origliante/ethcc',
  long_description=long_description,
  long_description_content_type="text/markdown",
  keywords = ['eth', 'ethereum', 'smart contracts', 'web3py', 'web3.py'],
  python_requires='>=3.6',
  install_requires=['web3',],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
)
