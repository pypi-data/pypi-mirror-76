import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name='make_sass_files',
    version='1.1.1',
    author="William L. Pickeral",
    author_email="willpickeral@gmail.com",
    description="A simple program to implement Sass 7-1 or 3-1 architecture",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wpickeral/make_sass_files",
    license="MIT",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    include_package_data=True
)
