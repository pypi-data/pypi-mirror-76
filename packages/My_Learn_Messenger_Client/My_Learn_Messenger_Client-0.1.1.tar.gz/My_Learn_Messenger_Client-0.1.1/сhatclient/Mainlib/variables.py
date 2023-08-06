default_port = 7777
default_address = '127.0.0.1'
# for JIM message
ACTION = 'action'
TIME = 'time'
USER = 'user'
ACCOUNT_NAME = 'account_name'
SENDER = 'from'
DESTINATION = 'to'
DATA = 'bin'
PUBLIC_KEY = 'pubkey'
PRESENCE = 'presence'
RESPONSE = 'response'
ERROR = 'error'
MESSAGE = 'message'
MESSAGE_TEXT = 'mess_text'
EXIT = 'exit'
GET_CONTACTS = 'get_contacts'
LIST_INFO = 'data_list'
REMOVE_CONTACT = 'remove'
ADD_CONTACT = 'add'
USERS_REQUEST = 'get_users'
PUBLIC_KEY_REQUEST = 'pubkey_need'
ONLINE_USERS_REQUEST = 'online_users_request'

RESPONSE_200 = {RESPONSE: 200}

RESPONSE_202 = {RESPONSE: 202,
                LIST_INFO: None
                }

RESPONSE_400 = {
    RESPONSE: 400,
    ERROR: None
}

RESPONSE_205 = {
	RESPONSE: 205
}

RESPONSE_511 = {
	RESPONSE: 511,
	DATA: None
}