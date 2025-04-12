from psycopg2 import pool, errors, connect
from sqlalchemy.engine import row

from src.errors import *
from psycopg2.errorcodes import UNIQUE_VIOLATION
from psycopg2.extras import RealDictCursor
from src.entity import *
class PostgreSQL:
    def __init__(self):
        self.connect=connect(user='postgres',password='qwerty12345',database='postgres')
    def search(self,search_string:str)->list[Set]:
        with self.connect as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(f"""
                select id,name, parts_volume, set_img_url   from relego.set 
                where text(id) like '%{search_string}%' OR name like '%{search_string}%'
            """)
                rows = cursor.fetchall()
                sets=[]
                for result in rows:
                    sets.append(Set(id=result["id"],name=result["name"],parts_volume=result["parts_volume"], image_link=result["set_img_url"]))
                return sets


    def get_set_by_id(self,id:int)->Set:
        with self.connect as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                select id,name,parts_volume,description, released, set_img_url, theme from relego.set 
                where id = %s
            """, (id,))
                row = cursor.fetchone()
                return Set(id=row["id"], name=row["name"], description=row["description"],
                    released=row["released"], theme=row["theme"], parts_volume=row["parts_volume"], image_link=row["set_img_url"])
    def create_user(self, user:UserData)->None:
        try:
            with self.connect as conn:
                with conn.cursor() as cursor:
                    cursor.execute(f"""
                        insert into relego.user_data(login, password) values (%s, %s)
                        """,(user.login, user.password))
        except errors.lookup(UNIQUE_VIOLATION):
            raise UserAlreadyExists

    def get_user_password_by_login(self, login:str)->str:
        with self.connect as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    select password from relego.user_data
                    where login = %s
                    """,(login,))
                row = cursor.fetchone()
                if row is None:
                    raise UserNotFound

                return row["password"]

    def add_set_to_user(self, login:str, set_id:int)->None:
        with self.connect as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                select 1 from relego.user_data
                where login = %s and %s= ANY(set_ids)
                """,(login,set_id,))
                if cursor.fetchone() is None:
                    cursor.execute("""
                        UPDATE relego.user_data SET set_ids = set_ids || '{%s}'
                        where login = %s
                        """,(set_id,login,))
                    
    def delete_set_from_user(self, login:str, set_id:int)->None:
        with self.connect as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    UPDATE relego.user_data SET set_ids = array_remove(set_ids, '%s')
                    where login = %s
                    """,(set_id,login,))
    def get_sets_by_user(self, login:str)->list[Set]:
        with self.connect as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                select set_ids from relego.user_data
                where login = %s
                """,(login,))
                user_set_ids=cursor.fetchone()
                if user_set_ids is None:
                    return []
                cursor.execute("""
                select name,id,parts_volume, set_img_url from relego.set
                where id=ANY(%s)
                """,(user_set_ids["set_ids"],))
                rows=cursor.fetchall()
                sets=[]
                for result in rows:
                    sets.append(Set(id=result["id"],name=result["name"],parts_volume=result["parts_volume"], image_link=result["set_img_url"]))
                return sets
    def search_sets_depending_on_user_sets(self, login:str, max_parts:int )->list[Set]:
            with self.connect as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    cursor.execute("""
                    select set_ids from relego.user_data
                    where login = %s
                    """,(login,))
                    user_set_ids=cursor.fetchone()["set_ids"]
                    cursor.execute("""
                    with set_details as (select part_id, sum(quantity) as sum_quantity
                    from relego.sets_to_parts
                    where sets_to_parts.set_id = ANY (%s)
                    group by part_id)
                    , irrelevant_sets as (select distinct (set_id) as set_id
                         from relego.sets_to_parts
                        left join set_details on set_details.part_id = relego.sets_to_parts.part_id
                         where (relego.sets_to_parts.part_id != ALL (select part_id from set_details))
                            OR (quantity > set_details.sum_quantity))
                        select s.name,s.id,s.parts_volume, s.set_img_url from relego.set as s
                        where (s.id != ALL (select irrelevant_sets.set_id from irrelevant_sets))
                        AND (s.id != ALL(%s));
                    """,(user_set_ids, user_set_ids,))
                    rows=cursor.fetchall()
                    sets=[]
                    for result in rows:
                        sets.append(Set(id=result["id"],name=result["name"],parts_volume=result["parts_volume"], image_link=result["set_img_url"]))
                    return sets



