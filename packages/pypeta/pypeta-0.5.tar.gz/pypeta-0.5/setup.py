from setuptools import setup,find_packages

def readme():
    with open('README.MD','r') as fh:
        return fh.read()
        
setup(
    author = 'JaylanLiu',
    author_email = 'liujilong@genomics.cn',

    name = 'pypeta',
    version = '0.5',
    description='BGI-PETA data APIs',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/JaylanLiu/pepeta',

    packages = find_packages(),
    install_requires=['pandas','numpy','requests'],

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ]
)