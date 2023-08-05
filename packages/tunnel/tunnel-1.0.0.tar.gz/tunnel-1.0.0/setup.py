from setuptools import setup, find_packages

setup(
    name="tunnel",
    version="1.0.0",
    license="MIT",
    author="Seongmin Park",
    author_email="llov0708@gmail.com",
    description="Stream everything.",
    long_description=open("README.md").read(),
    url="https://www.github.com/seongminp/straw",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
