import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="r3d",
    version="0.0.2",
    author="Mohammad Sadegh Alirezaie",
    author_email="alirezaie@sadegh.org",
    description="a python package for interacting with Marling Firmware and sending GCode",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/AlirezaieS/r3d",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)