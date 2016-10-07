class AtriumError(Exception):
    pass


class BadRequestError(AtriumError):
    pass


class ConfigError(AtriumError):
    pass


class ConflictError(AtriumError):
    pass


class MaintenanceError(AtriumError):
    pass


class MethodNotAllowedError(AtriumError):
    pass


class NotFoundError(AtriumError):
    pass


class NetworkError(AtriumError):
    pass


# class RequestFailedError(AtriumError): pass


class RequestTimeoutError(AtriumError):
    pass


class ServerError(AtriumError):
    pass


class UnauthorizedError(AtriumError):
    pass


class UnprocessableEntityError(AtriumError):
    pass
