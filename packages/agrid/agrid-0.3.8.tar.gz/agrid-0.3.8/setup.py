import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()



print('setuptools.find_packages() :', setuptools.find_packages())

setuptools.setup(
    name='agrid', 
    version="0.3.8",
    author="Tobias Staal",
    author_email="tobbetripitaka@gmail.com",
    description='A grid for spatial multidimensional processing',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/TobbeTripitaka/agrid',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)