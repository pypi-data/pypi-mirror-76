import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="atudomain-git",
    version="2.0.1",
    author="Adrian Tuzimek",
    author_email="tuziomek@gmail.com",
    description="Convenience library for working with Git on Linux. Requires git >= 2.18.4",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/atudomain/atudomain-python-git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: BSD License",
        "Operating System :: POSIX :: Linux",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
    ],
    python_requires='>=3.5',
)
