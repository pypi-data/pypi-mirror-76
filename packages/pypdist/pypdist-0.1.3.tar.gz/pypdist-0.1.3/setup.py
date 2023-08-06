from setuptools import setup

with open('pypdist/README.md') as f:
    long_description = f.read()

setup(name='pypdist',
      version='0.1.3',
      description='Model data using univariate distributions',
      packages=['pypdist'],
      author="David Pinto",
      author_email="davidengaut@gmail.com",
      install_requires=[
          'pypdist',
      ],
      long_description = long_description,
      long_description_content_type="text/markdown",
      zip_safe=False)