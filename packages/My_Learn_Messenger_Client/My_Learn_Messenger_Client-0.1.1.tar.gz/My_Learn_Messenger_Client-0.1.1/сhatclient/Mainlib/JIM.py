import json

from chatclient.сhatclient.Log.Log_decorators import log


class JIM(object):
    pass


@log
def get_message(client):
    """
    The utility for receiving and decoding a message accepts bytes and gives out a dictionary,
    if something else is received it gives a value error
    :param client:
    :return: dict
    """
    encoded_response = client.recv(10240)
    if isinstance(encoded_response, bytes):
        json_response = encoded_response.decode('utf-8')
        response = json.loads(json_response)
        if isinstance(response, dict):
            return response
        else:
            raise Exception('Decoding error')

    else:
        raise Exception


@log
def send_message(sock, message):
    """
    Message encoding and sending utility,
    takes a dictionary and sends it
    :param sock:
    :param message:
    :return: bytes
    """
    if not isinstance(message, dict):
        raise Exception('Encoding error')
    js_message = json.dumps(message)
    encoded_message = js_message.encode('utf-8')
    sock.send(encoded_message)


class JimResponse(JIM):

    def status_200(self):
        msg = {
            "response": 200,
            "alert": "Необязательное сообщение/уведомление"
        }
        print(msg)
        return msg

    def status_400(self):
        msg = {
            "response": 400,
            "error": "Bad Request"
        }
        print(msg)
        return msg

    def status_401(self):
        msg = {
            "response": 401,
            "error": "Name is already taken"
        }
        print(msg)
        return msg

    def status_402(self):
        msg = {
            "response": 402,
            "error": "This could be wrong password or no account with that name"
        }
        print(msg)
        return msg
