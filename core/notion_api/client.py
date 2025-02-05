# core/notion_api/client.py
from notion_client import Client
import os


class NotionConnector:
    def __init__(self):
        self.client = Client(auth=os.getenv("NOTION_TOKEN"))

    def get_database(self, database_id: str):
        return self.client.databases.query(database_id)
