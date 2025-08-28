class CustomerData:
    def __init__(self, name:str, age:int, cookie:str, banner_id:int):
        self.name = str(name)
        self.age = int(age)
        self.cookie = str(cookie)
        self.banner_id = int(banner_id)
        
    def __repr__(self) -> str:
        return f"CustomerData(name={self.name}, age={self.age}, cookie={self.cookie}, banner_id={self.banner_id})"