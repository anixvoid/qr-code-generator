from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="qr-code-generator",
    version="1.0.0",
    author="anixvoid",
    author_email="anixvoid@gmail.com",
    description="A simple QR code generator application",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/anixvoid/qr-code-generator",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "PyQt6>=6.4.0",
        "qrcode[pil]>=7.4.0",
        "Pillow>=9.5.0",
    ],
    entry_points={
        "console_scripts": [
            "qr-code-generator=src.main:main",
        ],
    },
    include_package_data=True,
)