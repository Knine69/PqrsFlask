class Person:
    __id = 0
    __name = ''
    __email = ''
    __document = ''
    __password = ''
    __position = ''
    __role = ''
    __department = ''

    def __init__(self, person_data: dict):
        self.__id = person_data.get('person_id')
        self.__document = person_data.get('document_id')
        self.__password = person_data.get('password')
        self.__position = person_data.get('position')
        self.__role = person_data.get('role')
        self.__department = person_data.get('department_id')
        self.__name = person_data.get('name')
        self.__email = person_data.get('email')

    def get_password(self):
        return self.__password
    
    def get_document(self):
        return self.__document
    
    def get_position(self):
        return self.__position
    
    def get_role(self):
        return self.__role
    
    def get_department(self):
        return self.__department
    
    def get_id(self):
        return self.__id
    
    def get_name(self):
        return self.__name
    
    def get_email(self):
        return self.__email