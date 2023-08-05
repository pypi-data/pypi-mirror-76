from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='catratenvironment',
      version='0.0.1',
      author="Callum Welsh and Connor Fieweger",
      long_description=long_description,
      long_description_content_type="text/markdown",
      install_requires=['gym', 'numpy', 'pandas']  # And any other dependencies foo needs
)
