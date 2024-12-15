from psycopg2 import pool, errors
from sqlalchemy.engine import row

from src.errors import *
from psycopg2.errorcodes import UNIQUE_VIOLATION
from psycopg2.extras import RealDictCursor
from src.entity import *
class PostgreSQL:
    def __init__(self):
        self.connection_pool=pool.SimpleConnectionPool(1,10,user='postgres',password='qwerty12345',database='postgres')

    def search(self,search_string:str)->list[Set]:
        with self.connection_pool.getconn() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(f"""
                select id,name,parts_volume from public.set 
                where text(id) like '%{search_string}%' OR name like '%{search_string}%'
            """)
                rows = cursor.fetchall()
                sets=[]
                for result in rows:
                    sets.append(Set(id=result["id"],name=result["name"],parts_volume=result["parts_volume"]))
                return sets


    def get_set_by_id(self,id:int)->Set:
        with self.connection_pool.getconn() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                select id,name,parts_volume,description, released,theme from public.set 
                where id = %s
            """, (id,))
                row = cursor.fetchone()
                return Set(id=row["id"], name=row["name"], description=row["description"],
                    released=row["released"], theme=row["theme"], parts_volume=row["parts_volume"])
    def create_user(self, user:UserData)->None:
        try:
            with self.connection_pool.getconn() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(f"""
                        insert into public.user_data(login, password) values (%s, %s)
                        """,(user.login, user.password))
        except errors.lookup(UNIQUE_VIOLATION):
            raise UserAlreadyExists

    def get_user_password_by_login(self, login:str)->str:
        with self.connection_pool.getconn() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    select password from public.user_data
                    where login = %s
                    """,(login,))
                row = cursor.fetchone()
                if row is None:
                    raise UserNotFound

                return row["password"]

    def add_set_to_user(self, login:str, set_id:int)->None:
        with self.connection_pool.getconn() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                select 1 from public.user_data
                where login = %s and %s= ANY(set_ids)
                """,(login,set_id,))
                if cursor.fetchone() is None:
                    cursor.execute("""
                        UPDATE public.user_data SET set_ids = set_ids || '{%s}'
                        where login = %s
                        """,(set_id,login,))

    def delete_set_from_user(self, login:str, set_id:int)->None:
        with self.connection_pool.getconn() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    UPDATE public.user_data SET set_ids = array_remove(set_ids, '%s')
                    where login = %s
                    """,(set_id,login,))

    # def search_by_sets(self,ids:list[int])->list[Set]:
    #     with self.connection_pool.getconn() as conn:
    #         with conn.cursor(cursor_factory=RealDictCursor) as cursor:
    #             cursor.execute(f"""
    #             select id,sum(volume) volume,color from public.part
    #             where set_id in {ids}""")
    #             user_set_rows = cursor.fetchall()
    #             cursor.execute(self._search_by_sets_query_generator(user_set_rows))
    #             result_rows = cursor.fetchall()
    #
    #
    #
    # def _search_by_sets_query_generator(self, rows:RealDictRow)->str:
    #     where_query_str:str = ""
    #
    #     for i in range(0, len(rows)):
    #         id = rows[i]["id"]
    #         volume = rows[i]["volume"]
    #         color = rows[i]["color"]
    #         where_query_str += f"(id = {id} and volume <= {volume} and color = '{color}')"
    #
    #         if i != len(rows)-1:
    #             where_query_str += " and "
    #
    #     return f"select set_id from public.part where {where_query_str}"



if __name__ == '__main__':
    c = PostgreSQL()
    print(c.add_set_to_user("proper1999",56578))

