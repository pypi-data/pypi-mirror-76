from setuptools import setup, find_packages

setup(
    name="judgmentModel",
    version="1.0.6",
    keywords="wenju xgboost gensim",
    description="A Chinese question judgment library",
    long_description="A Chinese question judgment library",
    license="MIT License",
    url="https://github.com/chendayin",
    author="dayin",
    author_email="760849607@qq.com",
    packages=find_packages(),
    package_data={'judgmentModel': ['2020_08_05_18_08_danmu_XG.model']},
    include_package_data=True,
    platforms='any',
    install_requires=['boto>=2.49.0', 'boto3>=1.14.13', 'botocore>=1.17.13', 'certifi>=2020.6.20', 'chardet>=3.0.4',
                      'DBUtils>=1.3', 'docutils>=0.15.2', 'gensim>=3.8.3', 'idna>=2.10', 'jiagu>=0.2.3',
                      'jmespath>=0.10.0', 'joblib>=0.15.1', 'numpy>=1.19.0', 'pandas>=1.0.5', 'PyMySQL>=0.9.3',
                      'python-dateutil>=2.8.1', 'pytz>=2020.1', 'redis>=3.5.3', 'requests>=2.24.0', 's3transfer>=0.3.3',
                      'scikit-learn>=0.23.1', 'scipy>=1.5.0', 'six>=1.15.0', 'sklearn>=0.0', 'smart-open>=2.0.0',
                      'threadpoolctl>=2.1.0', 'urllib3>=1.25.9', 'xgboost>=1.1.1'],
)
