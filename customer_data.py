from uuid import UUID

class CustomerData:
    def __init__(self, name:str, age:int, cookie:UUID, banner_id:int):
        self.name = name
        self.age = int(age)
        self.cookie = cookie
        self.banner_id = int(banner_id)