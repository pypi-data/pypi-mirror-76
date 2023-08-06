from setuptools import setup, find_packages

setup(
    name='Framy',
    version='0.0.1.1',
    description='simple web framework',
    long_description=open('README.md').read(),
    py_modules=[],
    package_dir={'': 'Framy'},
    install_requires=[
        "jinja2 ~= 2.11.2",
    ],
    author='a276me',
    author_email='2230061@ncpachina.org',
    license='MIT',
)