from abc import ABC, abstractmethod
from ....domain.config import Config
from ....application.router.utils.utils import PATCH_STORED_PROCEDURE, ERROR_MESSAGE, fetch_resources
from ....application.security.tokenmanager import JwtManager
from ..sqlstatements import get_one_from_table, create_statements_block, get_all_entities, delete_from_table
import json

class QueryExecutor(ABC):
    __manager = None
    def __init__(self, table_name) -> None:
        self.__manager = JwtManager()
        self.table_name = table_name
        self.mysql = Config.give_mysql_instance(Config)

    @abstractmethod
    def get_single_registry(self, id):
        try:
            with self.mysql.connection.cursor() as cur:
                cur.execute(get_one_from_table().format(self.table_name, self.table_name), create_statements_block({"id": id}))
                data = cur.fetchall()
                cur.close()
                return data
        except Exception as e:
            error_message = ERROR_MESSAGE.format(str(e))
            return error_message, 404
        
    @abstractmethod
    def get_registries(self):
        try:
            with self.mysql.connection.cursor() as cur:
                cur.execute(get_all_entities().format(self.table_name))
                data = cur.fetchall()
                cur.close()
                return data
        except Exception as e:
            error_message = ERROR_MESSAGE.format(str(e))
            return error_message, 500
    
    @abstractmethod
    def post_new(self):
        pass

    @abstractmethod
    def delete_registry(self, id):
        try:
            # with self.mysql.connection.cursor() as cur:
            #     cur.execute(delete_from_table().format(self.table_name, self.table_name), (id,))
            #     self.mysql.connection.commit()
            #     cur.close()
                print("Deleted record")
        except Exception as e:
            error_message = ERROR_MESSAGE.format(str(e))
            return error_message, 404

        return "Delete successfull"
     
    @abstractmethod
    def patch_registry(self, id, request):
        try:
            # request_data = json.loads(request.data.decode('utf-8'))
            # with self.mysql.connection.cursor() as cur:
                # cur.callproc(PATCH_STORED_PROCEDURE, [self.table_name, id, json.dumps(request_data)])
                # response = fetch_resources(cur)
                # self.mysql.connection.commit()
                # cur.close()
                # return response[0]
                print("Patched record")
        except Exception as e:
            error_message = ERROR_MESSAGE.format(str(e))
            return error_message, 500
        
    def validate_create_user_identity(self, token, document, isRestricted=True):
        result = self.__manager.validate_user_consult_identity(token, document, isRestricted)
        if "userValidated" in result:
            return result["userValidated"]
        else:
            return result["isAdmin"]
        
    def validate_and_process_admin_operations(self, request):
        try:
            validation = self.validate_identity(request)
            if validation["isAdmin"]:
                return True
            else:
                return self.return_unauthorized_error()
        except Exception as e:
            error_message = ERROR_MESSAGE.format(str(e))
            return error_message, 500

    def validate_identity(self, request):
        document = request.headers.get("documentId")
        return self.__manager.validate_user_consult_identity(request.headers.get("Authorization"), document)
    
    def return_unauthorized_error(self):
        return {"Error": "Unauthorized", "Code": 401}
    