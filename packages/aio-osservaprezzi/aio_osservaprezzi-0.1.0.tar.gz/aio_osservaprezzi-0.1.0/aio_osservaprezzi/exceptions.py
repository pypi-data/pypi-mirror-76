"""Exceptions for aio_osservaprezzi."""


class OsservaPrezziException(Exception):
    """OsservaPrezzi generic exception."""

    pass


class OsservaPrezziConnectionError(OsservaPrezziException):
    """OsservaPrezzi connection error exception."""

    pass


class RegionNotFoundException(OsservaPrezziException):
    """RegionNotFoundException."""

    pass


class StationsNotFoundException(OsservaPrezziException):
    """StationsNotFoundException."""

    pass
