import setuptools
import hashlib
import re

with open("README.md", "r") as fh:
    content = fh.read()
    arr = content.split("\n")
    long_description = "\n".join(arr[3:])


with open("libra/version.py", "r") as fp:
    try:
        version = re.findall(
            r"^version = \"([0-9\.]+)\"", fp.read(), re.M
        )[0]
    except IndexError:
        raise RuntimeError("Unable to determine version.")


install_requires=[
    'canoser>=0.8.2',
    # 'more-itertools', # only used in libra/proof/definition.py
    'PyNaCl',
]

tests_require = [
    'pytest',
]


if not 'sha3_256' in hashlib.algorithms_available:
    #only exec under sdist, not bdist_wheel
    #if add pysha3 always, it will be failed under windows without c++ compiler installed.
    install_requires.append("pysha3")

setuptools.setup(
    name="libra-core",
    version=version,
    author="yuan xinyu",
    author_email="yuan_xin_yu@hotmail.com",
    description="Libra core types and functions for python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MoveOnLibra/libra-core.git",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    tests_require=tests_require,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
