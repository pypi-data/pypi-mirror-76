# python3 setup.py sdist && python3 -m twine upload --verbose dist/pylogtail-*.tar.gz(n[-1])

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pylogtail",
    version="0.9.2",
    author="Jinn Koriech",
    author_email="python-logtail@mx.ixydo.com",
    description="Process log file lines that have not been read.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/ixydo/python-logtail",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
