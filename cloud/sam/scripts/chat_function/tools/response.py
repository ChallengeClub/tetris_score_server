import json

class HttpResponse:

    DEFAULT_HEADERS = {
        'Access-Control-Allow-Headers': 'Content-Type, Authorization, X-Amz-Date, X-Api-Key, X-Amz-Security-Token, ,X-Amz-User-Agent,Origin, Accept, token, id, HEAD,X-CSRF-TOKEN',
        'Access-Control-Allow-Origin': 'http://localhost:8080',
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
