"""Initialize the package."""

from .osservaprezzi import (  # noqa
    OsservaPrezzi,
    RegionNotFoundException,
    StationsNotFoundException,
    OsservaPrezziConnectionError,
)

from .models import Station, Fuel  # noqa
