from pydantic import BaseModel

class Model:

    db_mapping={
        str:"varchar (80) ",
        int: 'integer',
        float : "float"

    }

    def __init__(self,table_name:str, fields: BaseModel):
        self.table_name=table_name
        self.fields=fields

    def __create_table__(self):
        return f'''
        create table if not exist {self.table_name} (
            {','.join([()])}
        )
        
        '''