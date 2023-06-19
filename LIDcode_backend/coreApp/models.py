import os
from .YDB_ORM import BaseModel, BaseManager
import boto3

from boto3.dynamodb.conditions import Attr
from botocore.exceptions import ClientError


# from .businessLogic import get_max_table_id, create_table_item

# database = boto3.resource(
#     'dynamodb',
#     endpoint_url=os.environ.get("USER_STORAGE_URL"),
#     region_name='ru-central1',
#     aws_access_key_id=os.environ.get("AWS_ACCESS_KEY"),
#     aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY")
# )


# event = database.Table('event')
# sponsor = database.Table('sponsor')
# organizer = database.Table('organizer')
# team = database.Table('team')
# material = database.Table('material')
# participant = database.Table('participant')
# user = database.Table('user')
# test_table_2 = database.Table('test_table_2')

class Events(BaseModel):
    manager_class = BaseManager
    table_name = "events"


class Sponsors(BaseModel):
    manager_class = BaseManager
    table_name = "sponsors"


class Organizers(BaseModel):
    manager_class = BaseManager
    table_name = "organizers"


class Teams(BaseModel):
    manager_class = BaseManager
    table_name = "teams"


class Materials(BaseModel):
    manager_class = BaseManager
    table_name = "materials"


class Participants(BaseModel):
    manager_class = BaseManager
    table_name = "participants"


class Users(BaseModel):
    manager_class = BaseManager
    table_name = "users"


class EventMaterial(BaseModel):
    manager_class = BaseManager
    table_name = "event_material"


class EventOrganizer(BaseModel):
    manager_class = BaseManager
    table_name = "event_organizer"


class EventSponsor(BaseModel):
    manager_class = BaseManager
    table_name = "event_sponsor"
