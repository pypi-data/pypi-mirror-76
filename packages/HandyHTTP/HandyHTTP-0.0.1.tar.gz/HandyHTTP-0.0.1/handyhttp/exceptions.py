
class HTTPException(Exception):
    message: str
    code: int

    def pack(self):
        return dict(error=self.message), self.code


class HTTPClientError(HTTPException):
    pass


class HTTPNotAcceptable(HTTPException):
    code = 406
    message = 'This request is not acceptable'


class HTTPNotFound(HTTPException):
    code = 404
    message = 'Resource does not exist'


class HTTPConflict(HTTPException):
    code = 409
    message = 'A resource with this ID already exists'


class HTTPForbidden(HTTPException):
    code = 403
    message = 'You have insufficient permissions to access this resource.'


class HTTPDenied(HTTPException):
    code = 401
    message = 'Access to this resource is denied.'


class HTTPBadRequest(HTTPException):
    code = 400
    message = 'This request can not be fulfilled.'
