import requests

api_key = "e01b8c558006282122f8bee5acf122e4"




class RebrickableApi:
    def get_image_by_id(self, set_id:int)->str:
        response = requests.get(f"https://rebrickable.com/api/v3/lego/sets/{set_id}-1/?key={api_key}")
        # todo проверить код ответа - сделать с Дашей
        return response.json()["set_img_url"]




if __name__ == '__main__':
    api = RebrickableApi()
    print(api.get_image_by_id(43247))