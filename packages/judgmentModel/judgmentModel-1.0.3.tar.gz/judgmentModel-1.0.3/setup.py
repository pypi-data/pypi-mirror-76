from setuptools import setup, find_packages

# requirements = list(map(lambda x: x.strip(), open("requirements.txt").readlines()))

setup(
    name="judgmentModel",
    version="1.0.3",
    keywords="wenju xgboost gensim",
    description="A Chinese question judgment library",
    long_description="A Chinese question judgment library",
    license="MIT License",
    url="https://github.com/chendayin",
    author="dayin",
    author_email="760849607@qq.com",
    packages=find_packages(),
    package_data={'judgmentModel': ['data/test.dat']},
    include_package_data=True,
    platforms='any',
)
