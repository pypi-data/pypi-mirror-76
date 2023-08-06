import setuptools

with open('README.md',"r") as f:
    readme_md = f.read()

setuptools.setup(
    name='petite',
    version='0.1.0',
    author='Kyoshiro Nonaka',
    author_email='kyo46n@gmail.com',
    description='GUI of Petit',
    long_description=readme_md,
    long_description_content_type='text/markdown',
    url='https://github.com/kyo46n/petite/',
    packages=setuptools.find_packages(),
    install_requires=['flask','numpy', 'pandas', 'scikit-learn', 'scipy', 'biopython', 'xlrd'],
    classifiers=[
        'Topic :: Scientific/Engineering :: Bio-Informatics'
    ],
    licence='MIT'
)