from setuptools import setup, find_packages
import os
import sys

def find_scripts(scripts_path):
  base_path = os.path.abspath(scripts_path)
  return list(map(lambda path: os.path.join(scripts_path, path), 
           filter(lambda file_name: os.path.isfile(
             os.path.join(base_path, file_name)), os.listdir(base_path)
         )))

setup(
        name='memoru',
        version='0.1',
        author='ayu-mushi',
        author_email='ayu.mushi2015@gmail.com',
        url='https://github.com/ayu-mushi/memoru',
        scripts=find_scripts('lib/bin'),
        packages=find_packages('lib'),
        package_dir={'':'lib'},
        license='MIT')
