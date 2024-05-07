
class GithubException(Exception):
    pass

class GithubExceptionUnauthorized(GithubException):
    pass

class GithubExceptionForbidden(GithubException):
    pass

class GithubExceptionNotFound(GithubException):
    pass

class GithubBadRefreshToken(GithubException):
    pass