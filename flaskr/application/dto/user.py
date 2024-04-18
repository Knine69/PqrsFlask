class UserDto:
    __document = ''
    __password = ''

    def __init__(self, document, password):
        self.__document = document
        self.__password = password

    def get_password(self):
        return self.__password
    
    def get_document(self):
        return self.__document