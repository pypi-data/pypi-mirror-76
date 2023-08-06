from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='jphellow',
      version='0.0.1',
      description='say hello',
      long_description=long_description,
      long_description_content_type="text/markdown",
      py_modules=['jphelloworld'],
      package_dir={'': 'src'},
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
      ],
      python_requires='>=3.5',
      install_requires = ["wheel >=0.34",],
      )
