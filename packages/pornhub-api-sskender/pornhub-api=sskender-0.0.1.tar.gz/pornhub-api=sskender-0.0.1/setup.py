import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pornhub-api=sskender", # Replace with your own username
    version="0.0.1",
    author="sskender",
    author_email="sskender@example.com",
    description="Unofficial API for pornhub.com in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sskender/pornhub-api",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)