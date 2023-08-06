# aiohttp-rate-limiter

[![Build Status](https://travis-ci.org/Flacy/aiohttp-rate-limiter.svg?branch=master)](https://travis-ci.org/Flacy/aiohttp-rate-limiter)

A library for control and limiting requests with aiohttp framework

### Usage
```python
from aiohttp import web
from aiohttp_rate_limiter import Config, setup


app = web.Application()
cfg = Config(method='fixed_window', max_requests=100)
setup(app, config=cfg)

web.run_app(app)
```

### Requirements:
* Python >= 3.7.x
* aiohttp >= 3.5.2
