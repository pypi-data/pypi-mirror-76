import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "ngocbienml",
    version="1.1.1",
    author="Nguyen Ngoc Bien",
    author_email="ngocbien.nguyen.vn@gmail.com",
    description="An ecosystem for machine learning project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url = "https://github.com/ngocbien",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.7.*',
    license='MIT',
    install_requires=[
        'numpy>=1.16.6',
        'scikit-learn>=0.20.4',
        'scipy>=0.19.0',
        'pandas>=0.24.2',
        'matplotlib>=2.2.5'
    ]
)