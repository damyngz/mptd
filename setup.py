from setuptools import setup, find_packages

setup(
    name='mptd',
    version='0.1.4.9',
    packages=find_packages('src'),
    package_dir={'': './src'},
    python_requires='>=3.6',
    install_requires=['mysql-connector-python',
                      'PYYaml',
                      'v20']
    # url='https://github.com/damyngz/mptd.git'
)
