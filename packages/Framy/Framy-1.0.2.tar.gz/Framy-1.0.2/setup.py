from setuptools import setup, find_packages

setup(
    name='Framy',
    version='1.0.2',
    description='simple web framework',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    py_modules=['startProject', 'info'],
    package_dir={'': 'Framy'},
    install_requires=[
        "jinja2 ~= 2.11.2",
    ],
    author='a276me',
    author_email='2230061@ncpachina.org',
    license='MIT',
)