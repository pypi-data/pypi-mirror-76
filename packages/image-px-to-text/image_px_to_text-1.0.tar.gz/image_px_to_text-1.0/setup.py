import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="image_px_to_text",
    version="1.0",
    author="Chaotic Kid",
    author_email="crazyanimations999@gmail.com",
    description="Get the color-info of ALL the pixels in your image",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://chaoticcoder.netlify.app",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
