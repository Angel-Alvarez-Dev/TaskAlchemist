from .config import NOTION_TOKEN, NOTION_DATABASE_ID
from notion_client import Client

client = Client(auth=NOTION_TOKEN)

def get_pending_tasks():
    response = client.databases.query(
        **{
            "database_id": NOTION_DATABASE_ID,
            "filter": {
                "property": "Estado",
                "select": {"equals": "Pendiente"},
            },
        }
    )
    return response["results"]

def mark_task_as_done(task_id):
    client.pages.update(page_id=task_id, properties={
        "Estado": {"select": {"name": "Hecho"}}
    })
