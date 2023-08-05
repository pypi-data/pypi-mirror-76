import setuptools

with open('README.md', 'r') as readme:
    long_description = readme.read()

setuptools.setup(
    name='NeuralWaveFunction',
    version='0.0.1pre1',
    author='Adnan Dautovic',
    author_email='A.Dautovic@phyik.uni-muenchen.de',
    description='VMC with neural networks as test functions',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://gitlab.physik.uni-muenchen.de/A.Dautovic/neuralwavefunction',
    packages=setuptools.find_packages(),
    classifiers=[
        'Development Status :: 1 - Planning',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
    ],
)

