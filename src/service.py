from src.errors import UserNotFound
from src.provider.postgres import PostgreSQL
from src.entity import *
class Service:
    def __init__(self):
        self.db=PostgreSQL()

    def search_set_by_string(self, search_string:str)->list[Set]:
        sets=self.db.search(search_string)
        return sets


    def get_set_info_by_id(self, id:str)->Set:
        set=self.db.get_set_by_id(id)
        set.instruction_link=self._get_instruction_link_by_id(set.id)
        return set


    def _get_instruction_link_by_id(self, id:str)->str:
        return f"https://www.lego.com/en-us/service/buildinginstructions/{id}"

    def create_user(self, user: UserData)->None:
        return self.db.create_user(user)

    def check_user_password(self, user_data:UserData)->bool:
        try:
            password=self.db.get_user_password_by_login(user_data.login)
        except UserNotFound:
            return False
        return password==user_data.password


    def add_set_to_user(self, login: str, set_id: int) -> None:
        return self.db.add_set_to_user(login, set_id)

    def delete_set_from_user(self, login:str, set_id:str)->None:
        return self.db.delete_set_from_user(login, set_id)

    def get_sets_by_user(self, login:str)->list[Set]:
        return self.db.get_sets_by_user(login)
    
    def search_sets_depending_on_user_sets(self, login:str, max_parts:int)->list[Set]:
        sets = self.db.search_sets_depending_on_user_sets(login, max_parts)
        return sets
        