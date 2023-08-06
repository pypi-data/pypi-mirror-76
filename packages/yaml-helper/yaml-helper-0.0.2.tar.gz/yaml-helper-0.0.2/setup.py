import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='yaml-helper',
    version='0.0.2',
    author='Randy Cahya Wihandika',
    author_email='rendicahya@gmail.com',
    description='Helper methods to read and write .yml files.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/rendicahya/yaml-helper',
    packages=setuptools.find_packages(),
    install_requires=['pyyaml'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
