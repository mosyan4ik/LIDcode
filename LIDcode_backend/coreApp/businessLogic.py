import json
import os
from decimal import Decimal
import boto3
import ydb as ydb
import asyncio
from boto3.dynamodb.conditions import Attr

# from models import participant
# _endpoint = os.environ.get("ENDPOINT")
_endpoint = "grpcs://ydb.serverless.yandexcloud.net:2135"
# _database = os.environ.get("DATABASE")
_database = "/ru-central1/b1grhpet2bgap5qviuqc/etnkctir026i4aupjv13"
_driver = ydb.aio.Driver(endpoint=_endpoint, database=_database,
                         credentials=ydb.iam.ServiceAccountCredentials.from_file('authorized_key.json',
                                                                                 iam_endpoint=None,
                                                                                 iam_channel_credentials=None))


async def interaction_root_method(table_name, method='get', **attrib):
    table_name = "/" + table_name
    pool = ydb.aio.SessionPool(_driver, size=10)
    session = await pool.acquire()
    method_low_case = method.lower()
    resp = {}

    if method_low_case == 'get':
        resp["Items"] = []
        async for sets in await session.read_table(_database + table_name):
            resp["Items"] = resp.get("Items").extend([[row[::] for row in sets.rows]])
    elif method_low_case == 'post':
        id = None
        lst_id = []
        async for sets in await session.read_table(_database + table_name):
            lst_id.append([int(row[0]) for row in sets.rows])
        id = max(lst_id) + 1
        resp["Items"] = await upsert_simple(session, _database, id=id, **attrib)
    elif method_low_case == 'update':
        resp["Items"] = await upsert_simple(session, _database, **attrib)
    elif method_low_case == 'delete':
        resp["Items"] = await delete_simple(session, _database, **attrib)

    await pool.release(session)
    await pool.stop()
    await _driver.stop()
    return resp


async def upsert_simple(session, path, table_name, **attrib):
    atr = {}
    resp = {}
    for i, j in attrib.items():
        atr[i] = j
    await session.transaction().execute(
        """
        PRAGMA TablePathPrefix("{}");
        UPSERT INTO {} (id, name, emailAdress, phoneNumbers, universityCourse, universityFaculty, organization, contact, coach, main, reserve) VALUES
            ({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {});
        """.format(path, table_name[1:], atr.get("id"), atr.get("name"), atr.get("emailAdress"),
                   atr.get("phoneNumbers"), atr.get("universityCourse"), atr.get("universityFaculty"),
                   atr.get("organization"), atr.get("contact"), atr.get("coach"), atr.get("main"), atr.get("reserve")),
        commit_tx=True,
    )
    resp["Items"] = await session.transaction().execute(
        """
        PRAGMA TablePathPrefix("{}");
        SELECT * FROM {} WHERE id=={};
        """.format(path, table_name[1:], atr.get("id")),
        commit_tx=True,
    )
    return resp



async def delete_simple(session, path, table_name, **attrib):
    resp = {}
    id = None
    for i, j in attrib.items():
        if i == 'id':
            id = j
    await session.transaction().execute(
        """
        PRAGMA TablePathPrefix("{}");
        DELETE FROM {} 
        WHERE id == {};
        """.format(path, table_name[1:], id),
        commit_tx=True,
    )
    resp["Items"] = await session.transaction().execute(
        """
        PRAGMA TablePathPrefix("{}");
        SELECT * FROM {} WHERE id=={};
        """.format(path, table_name[1:], id),
        commit_tx=True,
    )
    return resp


# def get_max_table_id(table):
#     data_table = []
#     async for sets in await session.read_table(_database + table_name):
#         resp["Items"] = resp.get("Items").extend([[row[::] for row in sets.rows]])
#     if len(data_table['Items']) == 0:
#         return 0
#     mxi = max([i['id'] for i in data_table['Items']])
#     return mxi

def get_max_table_id(table):
    data_table = table.scan(
        FilterExpression=Attr('id').ne(-1)
    )
    if len(data_table['Items']) == 0:
        return 0
    mxi = max([i['id'] for i in data_table['Items']])
    return mxi


def get_data_table(table):
    return table.scan()


def update_table_item(table, id, **atrib):
    print(atrib.items())
    for i, j in atrib.items():
        print(f"set {i}='{j}'")
        respouce = table.update_item(Key={'id': id},
                                     UpdateExpression=f"set {i}=:n",
                                     ExpressionAttributeValues={
                                         ':n': j
                                     }
                                     )
        # print(respouce['ResponseMetadata']['HTTPStatusCode'])
    return table.scan(
        FilterExpression=Attr('id').eq(id)
    )


def create_table_item(table, **attrib):
    # print(table.name)
    # print(attrib.items())
    mxi = get_max_table_id(table)
    attr = {}
    for i, j in attrib.items():
        attr[i] = j
    attr['id'] = mxi + 1
    table.put_item(
        Item=attr
    )
    return table.scan(
        FilterExpression=Attr('id').eq(mxi)
    )


def delete_table_item(table, id):
    table.delete_item(
        Key={'id': id}
    )
    return table.scan(
        FilterExpression=Attr('id').eq(id)
    )


# def get_from_table(table, **eque) -> json:
#     ans_i_j = {}
#     for i, j in eque.items():
#         ans_i_j[i] = j
#     print(ans_i_j)
#     ans = {}
#     for i in ans_i_j:
#         print(i, ans_i_j.get(i))
#         print(type(i), type(ans_i_j.get(i)))
#         ans[i] = table.scan(
#             FilterExpression = Attr(i).contains(ans_i_j.get(i)) | Attr(i).eq(ans_i_j.get(i))
#         )
#     return ans


if __name__ == '__main__':
    pass
    # delete_table_item(test_table_2, 3)
    # create_table_item(participant, name="Oleg", emailAdress='mroleg@mail.ru', phoneNumbers='89998887766',
    #                   organization='unit', universityFaculty='IVT', universityCourse='3')
    # update_table_item(test_table_2, 1, name="Igor")
    # get_data = get_from_table(test_table_2, name='Ivan', id_test_person=2)
    # print(get_data['name'])
    # print(get_data['id_test_person'])
    #
