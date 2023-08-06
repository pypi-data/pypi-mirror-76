import os
import subprocess

from setuptools import setup, find_packages


def read_file(fname):
    return open(os.path.join(os.path.dirname(__file__), fname), encoding='utf-8').read()


def git_version():
    """
    Fetch version from git information
    """
    git_default_version = '0.1.0'
    try:
        git_tag = subprocess.check_output(['git', 'describe', '--tags'])
        if git_tag:
            return git_tag.strip()[1:].decode('utf-8')
    except Exception:
        return git_default_version


setup(name="ms-settings",
      version=git_version(),
      description="A simple setting tool for project",
      long_description=read_file('README.md'),
      long_description_content_type='text/markdown',
      url='http://gitlab.com/theo-l/py_settings',
      author='Liang Guisheng',
      author_email='theol.liang@gmail.com',
      license='MIT',
      classifiers=[
          'Programming Language :: Python :: 3',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
      ],
      keywords='python settings configuration',
      packages=["py_settings"],
      extras_require={'dev': read_file('requirements-dev.txt').strip().split('\n')[1:]})
