from setuptools import find_packages,setup
from typing import List

def get_list_from_requirement(text_file: str)->List:
    requirement_list = []
    with open(text_file, 'r') as file:
        for line in file:
            line = line.rstrip()
            requirement_list.append(line)

    return requirement_list

setup(
    name='sensor',
    version='0.0.1',
    author='ravikanur',
    author_email='ravikanur@gmail.com',
    packages=find_packages(),
    install_requires= get_list_from_requirement('requirement.txt')
)
