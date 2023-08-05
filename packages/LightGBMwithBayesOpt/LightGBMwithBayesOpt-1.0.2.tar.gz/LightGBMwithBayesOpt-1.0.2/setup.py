import setuptools
from os import path

from LightGBMwithBayesOpt import __version__

here = path.abspath(path.dirname(__file__))

air = [
    "bayesian-optimization>=1.1.0",
    "scikit-learn>=0.22.2.post1",
    "lightgbm>=2.3.1",
]


setuptools.setup(
    name='LightGBMwithBayesOpt',
    version=__version__,
    description='A Python toolkit of light gbm with bayesian optimizer.',
    url='https://github.com/gowun/LightGBMwithBayesOpt.git',
    author="Gowun Jeong",
    author_email='gowun.jeong@gmail.com',
    license='MIT',
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    zip_safe=False,
    #long_description=open('README.md').read(),
    install_requires=air,
    classifiers=["Programming Language :: Python :: 3",
                 "License :: OSI Approved :: MIT License",
                 "Operating System :: OS Independent",
                 ],
)