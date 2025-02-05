# core/notion_api/client.py
from notion_client import Client
import os

# core/notion_api/client.py


class NotionConnector:
    # ... existing code ...

    def mark_task_processed(self, page_id: str, file_path: str):
        """Update Notion task with file path and clear create flag"""
        self.client.pages.update(
            page_id,
            properties={
                "Filepath": {"url": file_path},
                "CreateFile": {"checkbox": False}
            }
        )
