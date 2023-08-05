import setuptools

with open("readme.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="data_ntegration", 
    packages=setuptools.find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    version="0.1",
    license='MIT',
    author="weis",
    author_email="shaowei@funstory.ai",
    description="data_ntegration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    keywords=['data_integration'],
    python_requires='>=3.7',
    install_requires=[
        "pymysql==0.10.0",
        "kafka-python==2.0.1"
    ],
)