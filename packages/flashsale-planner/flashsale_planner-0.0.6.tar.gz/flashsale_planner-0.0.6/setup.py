import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="flashsale_planner",
    version="0.0.6",
    author="Papan Yongmalwong",
    author_email="papillonbee@gmail.com",
    description="A package serving as a planning tool for sellers on Shopee flash sale",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/papillonbee/flashsale_planner",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)