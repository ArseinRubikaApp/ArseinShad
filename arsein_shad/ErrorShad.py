from .Error import ErrorMethod, TOO_REQUESTS


class ErrorShad:
    def __init__(self, ERROR):
        if ERROR["status_det"] == "INVALID_AUTH":
            self.Error = "re"
            self.state = (
                "AuthError: User authentication is invalid and must be re-entered"
            )
        elif ERROR["status_det"] == "NOT_REGISTERED":
            self.Error = "re"
            self.state = "NOT_REGISTERED: The user's device is not registered and must be registered"
        elif ERROR["status_det"] == "INVALID_INPUT":
            self.Error = "ra"
            raise ErrorMethod("ًInput value in the method is incorrect")
        elif ERROR["status_det"] == "TOO_REQUESTS":
            self.Error = "ra"
            raise TOO_REQUESTS("ًThe number of requests has been exceeded")
