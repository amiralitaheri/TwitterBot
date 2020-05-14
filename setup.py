import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="TwitterBot",
    version="2020.4.30",
    author="Amirali Taheri",
    author_email="amiralitaheri64@gmail.com",
    description="a Twitter bot that will find and retweet computer engineering related tweets",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/amiralitaheri/TwitterBot",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 1 - Planning",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],  # available at https://pypi.org/classifiers/
    entry_points={  # points to where the cli is located
        "console_scripts": [
            'python-cli-template = src.__main__:main'
        ]
    }
)
