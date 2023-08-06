import setuptools


long_description = "Currently a work in progress"


setuptools.setup(
    name="BrawlMoon",
    version="v0.1.0",
    author="Kyando",
    author_email="amehikoji@gmail.com",
    description="Handler for the Brawl Stars API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Kyando2/BrawlMoon",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)