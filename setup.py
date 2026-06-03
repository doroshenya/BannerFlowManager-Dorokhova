from setuptools import setup, find_packages

setup(
    name='bannerflow-manager',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Django>=4.2',
        'djangorestframework',
        'Pillow',
        'pandas',
        'pytest',
        'pytest-django',
        'pytest-cov',
    ],
    entry_points={
        'console_scripts': [
            'bannerflow-manager=manage:main',
        ],
    },
    author="Дорохова Александра",
    description="Веб-приложение для управления игровыми рекламными баннерами",
    license="MIT",
    python_requires='>=3.11',
)