from setuptools import setup

setup(
    name='hypergo',
    version='0.1',
    description='The hypergo library',
    author='Matthew Hansen',
    author_email='hypergo@mattian.com',
    package_dir = {"": "src"},
    install_requires=[
        "azure-functions",
        "azure-servicebus",
        "pyyaml",
        "glom"
        ],
)
