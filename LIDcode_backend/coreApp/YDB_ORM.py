import asyncio
import os

import ydb

def _check_quotes_suffix_and_prefix(*args):
    for i in args:
        if isinstance(i, str):
            yield _write_quotes_suffix_and_prefix(i)
        else:
            yield str(i)


def _write_quotes_suffix_and_prefix(word):
    # print("'" + word + "'")
    return "'" + word + "'"


class WhereConstructor:
    storage_conditions = []
    """
    [
     {
        'parameter': name,
        'operator': '==',
        'meaning': 'Ivan',
        'connection': 'and'
     },
    
     {
        'parameter': id,
        'operator': '>=',
        'meaning': 3,
        'connection': 'or'
     }
     ]
     :return "name=='Ivan' or id>=3"
     """

    def append(self, parameter, operator, meaning, connection="and"):
        self.storage_conditions.append({'parameter': parameter,
                             'operator': operator,
                             'meaning': meaning,
                             'connection': connection})

    def to_string(self):
        response = ''
        for o in range(len(self.storage_conditions)):
            condition = self.storage_conditions[o]
            response += f"{'' if o==0 else condition.get('connection')} {condition.get('parameter')}" \
                        f"{condition.get('operator')}{[i for i in _check_quotes_suffix_and_prefix(condition.get('meaning'))][0]} "
        self.storage_conditions.clear()
        self.storage_conditions = []
        return response


# ------------ Manager (Model objects handler) ------------ #
class BaseManager:
    connection = None
    sessionPool = None
    async def get_session(cls):
        cls.connection = await cls.sessionPool.acquire()
        print('session is get')

    @classmethod
    async def set_connection(cls):
        # if cls.connection is None:

        # connection = psycopg2.connect(**database_settings)
        # connection.autocommit = True  # https://www.psycopg.org/docs/connection.html#connection.commit
        # cls.connection = connection
        _endpoint = os.environ.get("ENDPOINT")
        _database = os.environ.get("DATABASE")
        # _endpoint = "grpcs://ydb.serverless.yandexcloud.net:2135"
        # _database = "/ru-central1/b1grhpet2bgap5qviuqc/etnkctir026i4aupjv13"
        _driver = ydb.aio.Driver(endpoint=_endpoint, database=_database,
                                 credentials=ydb.iam.ServiceAccountCredentials.from_file('coreApp/authorized_key.json',
                                                                                         iam_endpoint=None,
                                                                                         iam_channel_credentials=None))
        # coreApp /
        # session = await ydb.aio.SessionPool(_driver, size=10).acquire()
        # print('type(session)', type(session))
        # session = pool.acquire()

        pool = ydb.aio.SessionPool(_driver, size=10)
        session = await pool.acquire()
        cls.sessionPool = pool
        cls.connection = session

    async def close_connection(self):
        await self.sessionPool.release(self.connection)
        await self.sessionPool.stop()

    def __init__(self, model_class):
        self.model_class = model_class

    @classmethod
    def _get_cursor(cls):
        # print('_____________________--------------------', cls.connection, cls.sessionPool)
        return cls.connection.transaction()

    @classmethod
    def _execute_query(cls, query, params=None):
        cursor = cls._get_cursor()
        cursor.execute(query, params)


    async def select(self, *field_names, **where_settings):
        # await self.get_session()
        # print('________4444444_____--------------------', self.connection, self.sessionPool)
        await self.set_connection()
        # asyncio.get_event_loop().run_until_complete(self.set_connection())
        # Конструирование необходимых полей
        if len(field_names) != 0:
            field_names = (*field_names, "forSorted")
            fields_format = ', '.join(field_names)
            # fields_format = "*"
        else:
            fields_format = '*'
        # print('settings:', where_settings)
        # print('first separator------------------------------------------------------------')
        where = ''
        try:
            if where_settings['where_settings']:
                where += ' WHERE' + where_settings['where_settings'].to_string()
                where = where.replace("None", 'null')
                where = where.replace('==null', ' IS NULL')
                where = where.replace('!=null', ' IS NOT NULL')
                print(where)
        except KeyError:
            pass
        # print('second separator------------------------------------------------------------')

        query = f"SELECT {fields_format} FROM {self.model_class.table_name}" + where + " ORDER BY forSorted DESC"
        print('query', query)
        # Execute query
        cursor = self._get_cursor()
        # print('get cursor', cursor)
        # answer = cursor.execute(query, commit_tx=True)
        answer = await cursor.execute(query)
        # print(f'executed query at cursor {cursor} and answer is {answer}')
        # print(answer[0])
        # await answer
        # answer_list = []
        # print('beginning iterating through answer rows')
        # for i in answer[0].rows:
        #     answer_list.append(i)
        # print('ending iterating through answer rows')
        # print('answer_list', answer_list)

        # for o in answer_list:
        #     print('o', o)

        # return answer_list
        # await self.sessionPool.release(self.connection)
        # await self.close_connection()
        return answer

    async def upsert(self, **kwargs):
        print("self.model_class", self.model_class, self.model_class.table_name)
        # await self.get_session()
        await self.set_connection()
        # asyncio.get_event_loop().run_until_complete(self.set_connection())
        field_names = sorted(kwargs.keys())

        fields_format = ", ".join(field_names)

        values_placeholder_format = ", ".join(
            [
                f'({", ".join([i for i in _check_quotes_suffix_and_prefix(*[kwargs.get(i) for i in field_names])])})'])
        values_placeholder_format = values_placeholder_format.replace("None", "null")

        query = f"UPSERT INTO {self.model_class.table_name} ({fields_format}) " \
                f"VALUES {values_placeholder_format}"
        print(query)
        cursor = self._get_cursor()
        answer = await cursor.execute(query, commit_tx=True)
        # await self.sessionPool.release(self.connection)
        # await self.close_connection()
        return answer

    async def delete(self, id=None, **kwargs):
        # await self.get_session()
        # print(kwargs)
        await self.set_connection()
        # asyncio.get_event_loop().run_until_complete(self.set_connection())
        if id is None:
            return "Id parameter not found"

        # Build DELETE query
        query = f"DELETE FROM {self.model_class.table_name} " \
                f"WHERE id=={id}"
        print('delete query', query)
        # Execute query
        cursor = self._get_cursor()
        # print('after cursor')
        answer = await cursor.execute(query, commit_tx=True)
        # print('after answer')
        # await self.sessionPool.release(self.connection)
        # await self.close_connection()
        return answer


# ----------------------- Model ----------------------- #
class MetaModel(type):
    manager_class = BaseManager

    def _get_manager(cls):
        return cls.manager_class(model_class=cls)

    @property
    def objects(cls):
        return cls._get_manager()


class BaseModel(metaclass=MetaModel):
    table_name = ""

    def __init__(self, **row_data):
        for field_name, value in row_data.items():
            setattr(self, field_name, value)
#TODO
    def __repr__(self):
        attrs_format = ", ".join([f'{field}={value}' for field, value in self.__dict__.items()])
        return f"<{self.__class__.__name__}: ({attrs_format})>\n"



# ----------------------- Setup ----------------------- #

# BaseManager.set_connection(database_settings=DB_SETTINGS)
# class Participants(BaseModel):
#     manager_class = BaseManager
#     table_name = "participants"


async def main():
    await BaseManager.set_connection()
    # while True:
    #     await BaseManager.set_connection()
    #     await asyncio.sleep(5)
    #     # loop.create_task(main(loop))
    #
    #     loop = asyncio.get_event_loop()
    #     loop.create_task(main())

async def mainrunner():
    await main()
    await asyncio.sleep(2)
    loop = asyncio.get_event_loop()
    loop.create_task(mainrunner())


#asyncio.run(main())
