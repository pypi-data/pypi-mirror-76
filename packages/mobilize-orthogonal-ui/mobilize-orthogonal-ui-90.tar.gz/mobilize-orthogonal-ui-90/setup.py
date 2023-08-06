import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mobilize-orthogonal-ui",
    version="90",
    author="Mobilize Engineering",
    author_email="noreply@mobilize.us",
    description="An orthogonal package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://mobilize.us",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    license='MIT',
)
