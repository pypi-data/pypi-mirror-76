import setuptools

with open('requirements.txt', 'r', encoding='utf-16-le') as requirements:
    requires = [x.strip() for x in requirements.readlines()]
    requires[0] = requires[0][1:]

print(requires)

with open("README.md", "r") as fh:
    long_description = fh.read()

print("PACKAGES")
print(setuptools.find_packages())

setuptools.setup(
    name="MLProto",
    version="0.2.0",
    author="Luke Williams",
    author_email="williams.luke.2001@gmail.com",
    description="Modular Neural Network Protyping for Stock Market Prediction",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CSLukeW/MLProto",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'ProtoMake = MLProto.MLProto.ProtoMake:main'
        ]
    },
    install_requires=requires
)