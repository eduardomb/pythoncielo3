from distutils.core import setup

setup(
    name='pythoncielo3',
    packages=['pythoncielo3'],
    version='0.0.3',
    description='Python integration for Cielo API 3.0',
    author='Eduardo Barbosa',
    author_email='eduardo.barbosa@ufmg.br',
    url='https://github.com/eduardomb/pythoncielo3',
    download_url='https://github.com/eduardomb/pythoncielo3/tarball/0.0.3',
    keywords=['cielo', 'api', 'webservice'],
    install_requires=['requests'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries',
        'Programming Language :: Python :: 3',
    ],
)
