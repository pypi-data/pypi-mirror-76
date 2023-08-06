from setuptools import setup, find_packages

setup(
    name="judgmentModel",
    version="1.0.7",
    keywords="wenju xgboost gensim",
    description="A Chinese question judgment library",
    long_description="A Chinese question judgment library",
    license="MIT License",
    url="https://github.com/chendayin",
    author="dayin",
    author_email="760849607@qq.com",
    packages=find_packages(),
    include_package_data=True,
    platforms='any',
    install_requires=['boto', 'boto3', 'botocore', 'certifi', 'chardet',
                      'DBUtils', 'docutils', 'gensim', 'idna', 'jiagu',
                      'jmespath', 'joblib', 'numpy', 'pandas', 'PyMySQL',
                      'python-dateutil', 'pytz', 'redis', 'requests', 's3transfer',
                      'scikit-learn', 'scipy', 'six', 'smart-open',
                      'threadpoolctl', 'urllib3', 'xgboost'],
)
