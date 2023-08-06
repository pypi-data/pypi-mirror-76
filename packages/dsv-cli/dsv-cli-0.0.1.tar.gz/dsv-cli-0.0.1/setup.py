import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dsv-cli",
    version="0.0.1",
    author="Alberto Castelo",
    author_email="alberto.castelo.becerra@gmail.com",
    description="Versioning for Data Science",
    url="https://github.com/AlbertoCastelo/DSV",
    scripts=['./scripts/dsv'],
    packages=['lib.dsv'],
    # packages=setuptools.find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)

# we need post_install actions to activate the CLI utility
# check: https://stackoverflow.com/questions/17806485/execute-a-python-script-post-install-using-distutils-setuptools

