import setuptools

setuptools.setup(
    name='django-postgres-matviews',
    version='2020.8.6',
    install_requires=open('requirements.txt').read().splitlines(),
    packages=setuptools.find_packages()
)
