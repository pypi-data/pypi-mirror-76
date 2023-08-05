# Custom exceptions
class HTTPError(Exception):
    def __init__(self,
                 status_code,
                 reason,
                 text):
        self.status = status_code
        self.status_code = status_code
        self.reason = reason
        self.message = text
        self.text = text
        Exception.__init__(self,
                           status_code,
                           reason,
                           text)
