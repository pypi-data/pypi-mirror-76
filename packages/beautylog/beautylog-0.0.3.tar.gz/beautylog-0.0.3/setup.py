import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="beautylog",
    version="0.0.3",
    author="AglarGil",
    author_email="aglargilwang@gmail.com",
    description="Let your code generate logs automatically",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Aglargil/beautylog",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)