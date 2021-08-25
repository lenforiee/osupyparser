import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="OsuPyParser",
    version="1.0.4",
    author="lenforiee",
    author_email="lenforiee@misumi.me",
    description="A powerful package for parsing .osu and .osr extention files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lenforiee/osupyparser",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
