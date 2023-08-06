from setuptools import setup, find_packages


with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name='tf-train',
    version='1.3.0',
    url='https://github.com/TheDim0n/TensorflowTraining',
    license='MIT',
    author='TheDim0n',
    description='Additional package for Tensorflow',
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires='>=3.6',
    install_requires=['tensorflow==2.2'],
    zip_safe=False
)