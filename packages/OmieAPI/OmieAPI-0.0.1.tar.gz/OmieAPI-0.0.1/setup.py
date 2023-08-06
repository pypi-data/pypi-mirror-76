from setuptools import setup

setup(
    name='OmieAPI',
    version='0.0.1',
    packages=['OmieAPI'],
    url='https://github.com/btmluiz/OmieAPI',
    license='LICENSE.txt',
    author='BtmLuiz',
    author_email='luiz@selectbrasil.com.br',
    description='Pacote de ingração com Omie',
    install_requires=[
        'requests>=2.24.0'
    ],
    python_requires='>=3'
)
