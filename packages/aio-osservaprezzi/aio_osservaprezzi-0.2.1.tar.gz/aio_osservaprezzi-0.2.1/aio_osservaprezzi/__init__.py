"""Initialize the package."""

from .osservaprezzi import OsservaPrezzi  # noqa

from .exceptions import (  # noqa
    RegionNotFoundException,
    StationsNotFoundException,
    OsservaPrezziConnectionError,
    OsservaPrezziException,
)

from .models import Station, Fuel  # noqa
