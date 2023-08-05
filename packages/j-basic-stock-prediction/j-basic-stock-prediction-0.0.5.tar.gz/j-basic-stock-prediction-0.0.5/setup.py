import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="j-basic-stock-prediction", # Replace with your own username
    version="0.0.5",
    author="dream.attempter",
    author_email="dream.attempter@gmail.com",
    description="Basic Stock Prediction",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=[
        'tensorflow>=2.3.0',
        'yfinance',
        'matplotlib'
    ],
    package_data={
        '': ['*.dylib']
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)