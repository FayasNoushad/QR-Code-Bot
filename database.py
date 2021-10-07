import os
import motor.motor_asyncio


class Database:
    def __init__(self, url=os.environ.get("DATABASE_URL"), database_name="FnQRCodeBot"):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(url)
        self.db = self._client[database_name]
        self.col = self.db.users
        self.cache = {}
    
    def new_user(self, id):
        return dict(
            id = id,
            as_file = False
        )
    
    async def add_user(self, id):
        user = self.new_user(id)
        await self.col.insert_one(user)
    
    async def get_user(self, id):
        user = self.cache.get(id)
        if user is not None:
            return user
        
        user = await self.col.find_one({"id": int(id)})
        self.cache[id] = user
        return user
    
    async def is_user_exist(self, id):
        user = await self.col.find_one({'id':int(id)})
        return True if user else False
    
    async def total_users_count(self):
        count = await self.col.count_documents({})
        return count
    
    async def get_all_users(self):
        all_users = self.col.find({})
        return all_users
    
    async def delete_user(self, user_id):
        await self.col.delete_many({'id': int(user_id)})
    
    async def is_as_file(self, id):
        user = await self.get_user(id)
        return user.get("as_file", False)

    async def update_as_file(self, id, as_file):
        self.cache[id]["as_file"] = as_file
        await self.col.update_one({"id": id}, {"$set": {"as_file": as_file}})


db = Database()
