import setuptools

with open("requirements.txt", "r") as f:
    requirements = [line.replace("\n", "") for line in f.readlines()]

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("gdeltdoc/_version.py", "r") as g:
    version = "1.0.0"
    for line in g.readlines():
        if "version" in line:
            version = (
                line.split("=")[1].replace("\n", "").replace('"', "").replace(" ", "")
            )

setuptools.setup(
    name="gdeltdoc",
    version=version,
    author="Ateet Vatan",
    author_email="ateetv555@gmail.com",
    description="A client for the GDELT 2.0 Doc API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AteetVatan/MASX_AI_GDELT_API",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    install_requires=requirements,
)
