from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

setup_args = dict(
    name='zibalPlatform',
    version='1.0.0',
    description='Zibal payment platform',
    long_description_content_type="text/markdown",
    long_description=README,
    license='MIT',
    packages=find_packages(),
    author='Yahya Kangi',
    author_email='yhy.kng@gmail.com',
    keywords=['Zibal', 'Payment', 'زیبال', 'درگاه پرداخت', 'درگاه زیبال', 'Platform', 'پلتفرم',],
    url='https://docs.zibal.ir/',
    download_url='https://pypi.org/project/zibalPlatform/'
)

classifiers=[
    "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

install_requires = [
    'requests'
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)