# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['prometheus_fastapi_instrumentator']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.38.1,<=1.0.0', 'prometheus-client>=0.8.0,<0.9.0']

setup_kwargs = {
    'name': 'prometheus-fastapi-instrumentator',
    'version': '1.3.0',
    'description': 'Instrument your FastAPI with Prometheus metrics',
    'long_description': '# Prometheus FastAPI Instrumentator\n\n[![PyPI version](https://badge.fury.io/py/prometheus-fastapi-instrumentator.svg)](https://pypi.python.org/pypi/prometheus-fastapi-instrumentator/)\n[![Maintenance](https://img.shields.io/badge/maintained%3F-yes-green.svg)](https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity)\n[![downloads](https://img.shields.io/pypi/dm/prometheus-fastapi-instrumentator)](https://pypi.org/project/prometheus-fastapi-instrumentator/)\n\n![release](https://github.com/trallnag/prometheus-fastapi-instrumentator/workflows/release/badge.svg)\n![test branches](https://github.com/trallnag/prometheus-fastapi-instrumentator/workflows/test%20branches/badge.svg)\n[![codecov](https://codecov.io/gh/trallnag/prometheus-fastapi-instrumentator/branch/master/graph/badge.svg)](https://codecov.io/gh/trallnag/prometheus-fastapi-instrumentator)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\nInstrument your FastAPI with Prometheus metrics. Install with:\n\n    pip install prometheus-fastapi-instrumentator\n\n## Fast Track\n\n```python\nfrom prometheus_fastapi_instrumentator import Instrumentator\nInstrumentator().instrument(app).expose(app)\n```\n\nWith this single line FastAPI is instrumented and all Prometheus metrics used \nin the FastAPI app can be scraped via the added `/metrics` endpoint. \n\nThe exporter includes the single metric `http_request_duration_seconds` of \nthe type Histogram. A separate `http_requests_total` isn\'t necessary as the \ntotal can be retrieved with the `http_requests_total_count` series.\n\nThe Prometheus FastAPI Instrumentator (any idea for a short hand?) is highly\nconfigurable and has few handy features.\n\n* **Opt-out** (activated by default):\n    * Status codes are grouped into `2xx`, `3xx` and so on.\n    * Requests without a matching template are grouped into the handler `none`.\n    * Regex patterns to ignore certain routes.    \n* **Opt-in** (Deactivated by default):\n    * Control instrumentation and exposition of FastAPI at runtime by setting \n        an environment variable.\n    * Rounding of latencies to a certain decimal number.\n    * Completely ignore untemplated routes.\n    * Renaming of labels and the metric.\n\n\nSee the *Example with all parameters* for all possible options.\n\n## Example with all parameters\n\n```python\nfrom prometheus_fastapi_instrumentator import PrometheusFastApiInstrumentator\nPrometheusFastApiInstrumentator(\n    should_group_status_codes=False,\n    should_ignore_untemplated=True,\n    should_group_untemplated=False,\n    should_round_latency_decimals=True,\n    should_respect_env_var_existence=True,\n    excluded_handlers=["/metrics", "/admin"],\n    buckets=[1, 2, 3, 4, 5],\n    metric_name="my_custom_metric_name",\n    label_names=("method_type", "path", "status_code",),\n    round_latency_decimals=3,\n    env_var_name="PROMETHEUS",\n).instrument(app).expose(app, "/prometheus_metrics")\n```\n\n`instrument`: Instruments the given FastAPI based on the configuration in \nthe constructur of the exporter class.\n\n`expose`: Completely separate from `instrument` and not necessary for \ninstrumentation. Just a simple option to expose metrics by adding an endpoint \nto the given FastAPI. Supports multiprocess mode.\n\n## Prerequesites\n\n* `python = "^3.6"` (tested with 3.6 and 3.8)\n* `fastapi = ">=0.38.1, <=1.0.0"` (tested with 0.38.1 and 0.59.0)\n* `prometheus-client = "^0.8.0"` (tested with 0.8.0)\n\n## Development\n\nDeveloping and building this package on a local machine requires \n[Python Poetry](https://python-poetry.org/). I recommend to run Poetry in \ntandem with [Pyenv](https://github.com/pyenv/pyenv). Once the repository is \ncloned, run `poetry install` and `poetry shell`. From here you may start the \nIDE of your choice.\n\nFor formatting, the [black formatter](https://github.com/psf/black) is used.\nRun `black .` in the repository to reformat source files. It will respect\nthe black configuration in the `pyproject.toml`. For more information just \ntake a look at the GitHub workflow files.\n\n',
    'author': 'Tim Schwenke',
    'author_email': 'tim.schwenke+github@protonmail.ch',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/trallnag/prometheus-fastapi-instrumentator',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
