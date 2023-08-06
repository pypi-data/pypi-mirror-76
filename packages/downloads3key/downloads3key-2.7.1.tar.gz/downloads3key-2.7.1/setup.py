import io
import os
import re
from setuptools import setup, find_packages


def read(*filenames, **kwargs):
    encoding = kwargs.get("encoding", "utf-8")
    sep = kwargs.get("sep", os.linesep)
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)


def read_requirements():
    content = read("requirements.txt")
    # Strip commented lines.
    return [line for line in content.split(os.linesep) if not line.strip().startswith("#")]

def read_version():
    content = read(os.path.join(os.path.dirname(__file__), "downloads3key", "__init__.py"))
    return re.search(r"__version__ = \"([^']+)\"", content).group(1)

setup(
   name='downloads3key',
   version=read_version(),
   description='Utility to download all s3 versions of s3 key.',
   author='Chandan Mahajan',
   author_email='mahajan.chandan18@gmail.com',
   packages=['downloads3key'],  #same as name
   install_requires=read_requirements(), #external packages as dependencies
   license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
   long_description=read("README.md"),
   long_description_content_type="text/markdown",
   keywords = ['aws s3', 'download s3 key versions'],   # Keywords that define your package best
   python_requires='>=3.6',
   entry_points={
          'console_scripts': [
              'downloads3key = downloads3key.__main__:main'
          ]
      },
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Utilities"
    ]
)
