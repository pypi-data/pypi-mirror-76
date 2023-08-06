from setuptools import setup


setup(
    name='aiohttp-rate-limiter',
    packages=['aiohttp_rate_limiter', 'aiohttp_rate_limiter/limiters'],
    version='0.0.3',
    author='Flacy',
    author_email='me@flacy.me',
    description='A library for control and limiting requests with aiohttp framework',
    url='https://github.com/Flacy/aiohttp-rate-limiter',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        'Development Status :: 3 - Alpha'
    ],
    install_requires=['aiohttp<4.0.0'],
    python_requires='>=3.7'
)
