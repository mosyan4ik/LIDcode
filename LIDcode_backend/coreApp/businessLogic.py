import json
from decimal import Decimal
import boto3
from boto3.dynamodb.conditions import Attr
# from models import participant


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
