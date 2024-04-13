from abc import ABC, abstractmethod
from ....domain.config import Config
from ....router.utils.utils import PATCH_STORED_PROCEDURE, ERROR_MESSAGE, fetch_resources
from ..sqlstatements import get_one_from_table, create_statements_block, get_all_entities, delete_from_table
import json

class QueryExecutor(ABC):
    def __init__(self, table_name) -> None:
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
            with self.mysql.connection.cursor() as cur:
                cur.execute(delete_from_table().format(self.table_name, self.table_name), (id,))
                self.mysql.connection.commit()
                cur.close()
        except Exception as e:
            error_message = ERROR_MESSAGE.format(str(e))
            return error_message, 404

        return "Delete successfull"
     
    @abstractmethod
    def patch_registry(self, id, request):
        try:
            request_data = json.loads(request.data.decode('utf-8'))
            with self.mysql.connection.cursor() as cur:
                cur.callproc(PATCH_STORED_PROCEDURE, [self.table_name, id, json.dumps(request_data)])
                response = fetch_resources(cur)
                self.mysql.connection.commit()
                cur.close()

                return response[0]
        except Exception as e:
            error_message = ERROR_MESSAGE.format(str(e))
            return error_message, 500