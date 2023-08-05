# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['prometheus_flask_instrumentator']

package_data = \
{'': ['*']}

install_requires = \
['flask>=1,<2', 'prometheus-client>=0.8,<0.9']

setup_kwargs = {
    'name': 'prometheus-flask-instrumentator',
    'version': '4.1.0',
    'description': 'Instruments Flask API transparently',
    'long_description': '# Prometheus Flask Instrumentator\n\n[![PyPI version](https://badge.fury.io/py/prometheus-flask-instrumentator.svg)](https://pypi.python.org/pypi/prometheus-flask-instrumentator/)\n[![Maintenance](https://img.shields.io/badge/maintained%3F-yes-green.svg)](https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity)\n[![downloads](https://img.shields.io/pypi/dm/prometheus-flask-instrumentator)](https://pypi.org/project/prometheus-flask-instrumentator/)\n\n![release](https://github.com/trallnag/prometheus-flask-instrumentator/workflows/release/badge.svg)\n![test branches](https://github.com/trallnag/prometheus-flask-instrumentator/workflows/test%20branches/badge.svg)\n[![codecov](https://codecov.io/gh/trallnag/prometheus-flask-instrumentator/branch/master/graph/badge.svg)](https://codecov.io/gh/trallnag/prometheus-flask-instrumentator)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\nSmall package to instrument your Flask app transparently.\n\n    pip install prometheus-flask-instrumentator\n\n## Fast Track\n\n```python\nfrom prometheus_flask_instrumentator import Instrumentator\n\nInstrumentator().instrument(app).expose(app)\n```\n\nWith this the Flask app is instrumented and all Prometheus metrics can be \nscraped via the `/metrics` endpoint. \n\nThe exporter includes the single metric `http_request_duration_seconds`. \nBasically everything around it can be configured and deactivated. These \noptions include:\n\n* Status codes are grouped into `2xx`, `3xx` and so on.\n* Requests without a matching template are grouped into the handler `none`.\n* Renaming of labels and the metric.\n* Regex patterns to ignore certain routes.\n* Decimal rounding of latencies.\n\nSee the *Example with all parameters* for all possible options or check \nout the documentation itself.\n\n## Example with all parameters\n\n```python\nfrom prometheus_flask_instrumentator import PrometheusFlaskInstrumentator\n\nPrometheusFlaskInstrumentator(\n    should_group_status_codes=False,\n    should_ignore_untemplated=False,\n    should_group_untemplated=False,\n    should_round_latency_decimals=True,\n    excluded_handlers=[\n        "admin",            # Unanchored regex.\n        "^/secret/.*$"],    # Full regex example.  \n    buckets=(1, 2, 3, 4,),\n    metric_name="flask_http"\n    label_names=("flask_method", "flask_handler", "flask_status",),\n    round_latency_decimals=3,\n).instrument(app).expose(app, "/prometheus_metrics")\n```\n\nIt is important to notice that you don\'t have to use the `expose()` method if \nadding the endpoint directly to the Flask app does not suit you. There are many \nother ways to expose the metrics.\n\nThe defaults are the following:\n\n```python\nshould_group_status_codes: bool = True,\nshould_ignore_untemplated: bool = False,\nshould_group_untemplated: bool = True,\nshould_round_latency_decimals: bool = False,\nexcluded_handlers: list = ["/metrics"],\nbuckets: tuple = Histogram.DEFAULT_BUCKETS,\nmetric_name: str = "http_request_duration_seconds",\nlabel_names: tuple = ("method", "handler", "status",),\nround_latency_decimals: int = 4,\n```\n\n## Prerequesites\n\n* `python = "^3.6"` (tested with 3.6 and 3.8)\n* `flask = "^1"` (tested with 1.1.2)\n* `prometheus-client = "^0.8.0"` (tested with 0.8.0)\n\n## Development\n\nDeveloping and building this package on a local machine requires \n[Python Poetry](https://python-poetry.org/). I recommend to run Poetry in \ntandem with [Pyenv](https://github.com/pyenv/pyenv). Once the repository is \ncloned, run `poetry install` and `poetry shell`. From here you may start the \nIDE of your choice.\n\nFor formatting, the [black formatter](https://github.com/psf/black) is used.\nRun `black .` in the repository to reformat source files. It will respect\nthe black configuration in the `pyproject.toml`.\n',
    'author': 'Tim Schwenke',
    'author_email': 'tim.schwenke+trallnag@protonmail.ch',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/trallnag/prometheus-flask-instrumentator',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
