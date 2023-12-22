import shelve

class Database:
    def __init__(self , dbName:str = "chat_history"):
        self.dbName = dbName

    # Saving the chat to shelve file:
    def save_chat_history(self , messages:[dict]):
        with shelve.open(self.dbName) as db:
            db["messages"] = messages

    # Getting the old chats from shelve
    def load_chat_history(self) -> [dict]: 
        with shelve.open(self.dbName) as db: 
            return db.get("messages" , [])  