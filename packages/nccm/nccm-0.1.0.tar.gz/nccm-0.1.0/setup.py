import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='nccm',
    version='0.1.0',
    description='NCurses ssh Connection Manager',
    url='https://github.com/flyingrhinonz/nccm',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Kenneth Aaron',
    author_email='flyingrhino@orcon.net.nz',
    license='GNU GPLv3',
    packages=setuptools.find_packages(),
    install_requires=['PyYaml',],

    classifiers=[
        'Programming Language :: Python :: 3',
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: POSIX :: Linux',
    ],
    python_requires='>=3.5',
)


