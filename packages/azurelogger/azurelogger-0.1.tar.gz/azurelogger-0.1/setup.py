import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="azurelogger",
    version="0.1",
    author="Toni Skulj",
    author_email="t.skulj@hotmail.com",
    description="A Package that lets you easily log to a azure blob",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=['azure.storage.blob'],
    license='MIT'
)
