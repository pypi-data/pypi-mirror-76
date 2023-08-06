# import setuptools
# #可根据文档自行添加
# setuptools.setup(
#     name='galaxy dataset',
#     version='0.0.1',
#     author='Lifeng Liu',
#     author_email='liu_lf@zju.edu.cn',
#     #自动发现所有软件包和子软件包。在这种情况下软件包列表将为galaxydataset(包含__init__的)
#     packages=setuptools.find_packages(),
# )
from setuptools import setup, find_packages

from version import VERSION
GALAXY_VERSION = VERSION
setup(
    name='galaxy dataset',
    version=GALAXY_VERSION,
    packages=find_packages(),
    entry_points={
        "console_scripts": ['GFICLEE = predict.main:main']
    },
    install_requires=[
        "matplotlib==3.1.1",
        "pandas==0.25.0",
        "pyparsing==2.4.1.1",
        "pyrsistent==0.15.3",
        "python-dateutil==2.8.0",
        "torch==1.2.0",
        "torchvision==0.4.0",
    ],
    url='https://github.com/ZJU-DistributedAI/GalaxyDataset',
    license='GNU General Public License v3.0',
    author='Lifeng Liu',
    author_email='liu_lf@zju.edu.cn',
    description='This  manuscript dataset for non-iid dataset.'
)