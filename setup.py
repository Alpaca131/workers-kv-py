import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()


setuptools.setup(
    name="workers-kv.py",
    version="1.0",
    author="Alpaca131",
    author_email="iwa124816@gmail.com",
    description="An api wrapper of Cloudflare Workers KV for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Alpaca131/workers-kv-py",
    packages=setuptools.find_packages(),
    install_requires=[
        "requests>=2.25.1",
        "aiohttp>=3.8.1"
    ],
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
