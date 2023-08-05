import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='panovid',
    version='1.0.0',
    author="Kyle Richards",
    author_email="kylelrichards11@gmail.com",
    description="Convert panoramic photos to scrolling videos",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kylelrichards11/panovid",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=["numpy", "opencv-python"]
)
