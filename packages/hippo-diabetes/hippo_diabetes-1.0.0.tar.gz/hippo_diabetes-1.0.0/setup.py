import setuptools

with open('README.md','r') as fh:
    long_description = fh.read()

setuptools.setup(
    name = 'hippo_diabetes',
    version = '1.0.0',
    author = 'author',
    author_email = 'author@gmail.com',
    description = 'Hippo package',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url = 'https://github.aetna.com/clinical-product-analytics/hippo/tree/master/src2',
    packages = setuptools.find_packages(),
    classifiers = [
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    python_requires = '>=3.6',
)
