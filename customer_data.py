from uuid import UUID

class CustomerData:
    def __init__(self, name:str, age:int, cookie:UUID, banner_id:int):
        self.name = name
        self.age = int(age)
        self.cookie = cookie
        self.banner_id = int(banner_id)
        
    def __repr__(self):
        return f"CustomerData(name={self.name}, age={self.age}, cookie={self.cookie}, banner_id={self.banner_id})"