from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='NBprocessing',
    version='0.0.15',
    author="Nir Barazida",
    author_email="nirbarazida@gmail.com",
    description="Pre-processing database using pre-written functions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nirbarazida/NBprocessing",
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)

# install_requires=['pandas', 'numpy','matplotlib','seaborn']

# name = pip install name
# 0.0.X - unstable
# scripts - all the py file we
# will look for every file that has a __init__ and will load it
#  find_packages(exclude=['docs','test*'])
# scripts = ['check']


# twine upload --skip-existing dist/*
