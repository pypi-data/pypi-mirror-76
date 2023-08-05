# flake8: noqa

import pkg_resources


__version__ = pkg_resources.get_distribution("pybsc").version


from pybsc.split import nsplit
