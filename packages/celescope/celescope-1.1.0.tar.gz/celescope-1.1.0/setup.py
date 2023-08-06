import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="celescope", # Replace with your own username
    version="1.1.0",
    author="zhouyiqi",
    author_email="zhouyiqi@singleronbio.com",
    description="GEXSCOPE Single cell analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zhouyiqi91/CeleScope",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    package_data={
        'celescope.tools': ['*.R'],     # All R files 
        '': ['templates/*'],
    },
    include_package_data=True,
)
