import setuptools

with open("README.md", "r", encoding="utf-8") as stream:
    long_description = stream.read()

setuptools.setup(
    name="osupyparser",
    version="1.0.8",  # TODO: update to 2.0.0
    author="lenforiee",
    author_email="lenforiee@gmail.com",
    description="A powerful package to parse osu! file formats.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lenforiee/osupyparser",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
