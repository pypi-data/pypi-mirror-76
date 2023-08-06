
import setuptools
with open("README.md", "r") as fh:
  long_description = fh.read()

print(setuptools.find_packages(where="src"))

setuptools.setup(
  name="pyrfdata",
  version="0.0.1",
  author="Prasanna Pendse",
  author_email="prasanna.pendse@gmail.com",
  description="Short description of pyrfdata",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/prasanna/pyrfdata",
  package_dir={"": "src"},
  packages=setuptools.find_packages(where="src"),
  entry_points={
    'console_scripts': [
      'pyrfdata=pyrfdata.pyrfdata:main',
    ],
  },
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: Apache Software License",
    "Operating System :: OS Independent",
  ],
  python_requires='>=3.6',
)
