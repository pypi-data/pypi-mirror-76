from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='detect-binod',
      version='0.0.1',
      description='This package will detect binod word in image file',
      long_description=long_description,
      long_description_content_type="text/markdown",
      py_modules=['detect_binod'],
      package_dir={'': 'src'},
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
      ],
      url="https://github.com/jps892/detect_binod",
      author="Jeevan Prakash",
      author_email="jeevan14sliet@gmail.com",
      python_requires='>=3.5',
      install_requires = ["Pillow >=7.2.0",
        "pytesseract >=0.3.4",
        "Pillow >=7.2.0",],
      )
