import json

class HttpResponse:

    DEFAULT_HEADERS = {
        'Access-Control-Allow-Origin': 'frontend_origin',
        'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS'
    }

    @staticmethod
    def generate_response(status_code, message):
        headers = HttpResponse.DEFAULT_HEADERS
        return {
            "statusCode": status_code,
            "headers": headers,
            "body": json.dumps({
                "message": message,
            }),
        }
    
    @classmethod
    def success(cls, message):
        return cls.generate_response(200, message)

    @classmethod
    def redirect(cls, message):
        return cls.generate_response(300, message)
    
    @classmethod
    def client_error(cls, message):
        return cls.generate_response(400, message)
    
    @classmethod
    def server_error(cls, message):
        return cls.generate_response(500, message)
