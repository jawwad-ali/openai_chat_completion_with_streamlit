from dotenv import load_dotenv,find_dotenv
from database import Database
from openai import OpenAI
from typing import Any

class BotModel:

    def __init__(self , name:str, model:str = 'gpt-3.5-turbo-16k') -> None:
        self.name:str = name
        self.model:str = model
        
        # load env vars
        load_dotenv(find_dotenv())

        self.client:OpenAI = OpenAI()
        self.db:Database = Database()
        
        # old messages
        self.messages = self.load_chat_history()

    def load_chat_history(self) -> []:
        return self.db.load_chat_history()

    # Saving Messages to shelve 
    def save_chat_history(self):
        self.db.save_chat_history(messages=self.messages)

    # Getting the saved messages back
    def get_messages(self)->[dict]:
        return self.messages
    
    def append_message(self , message:dict):
        self.messages.append(message)

    # Sending Messages to the GPTModel(Chat Completion API)
    def send_message(self , message)->Any:
        self.append_message(message)
        stream = self.client.chat.completions.create(
            model = self.model,
            messages = self.messages,  
            stream=True
        )
        return stream

    def delete_chat_history(self):
        self.messages = []
        self.save_chat_history()