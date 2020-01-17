class KiwiError(Exception):
    pass


class KiwiInternalError(Exception):
    pass


class KiwiConnectionError(KiwiError):
    pass
