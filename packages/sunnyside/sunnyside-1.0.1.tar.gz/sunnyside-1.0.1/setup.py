import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sunnyside",
    version="1.0.1",
    author="Jun Qi Li",
    author_email="JunQi.Li63@myhunter.cuny.com",
    description="Python wrapper for OpenWeather API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/junqili259/Sunnyside/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
