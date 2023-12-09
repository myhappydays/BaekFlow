from setuptools import setup, find_packages

setup(
    name='baekflow',
    version='0.1.0',
    description='Baekjoon automation tool',
    author='Hwang Seokjun',
    author_email='seokjun0515@kakao.com',
    url='https://github.com/myhappydays/BaekFlow',
    packages=find_packages(),
    entry_points={
        'console_scripts': ['baek=baekflow.main:main']
    },
)