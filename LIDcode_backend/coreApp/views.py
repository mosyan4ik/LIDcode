import asyncio
import base64
import re

import ydb
from rest_framework.renderers import JSONRenderer

from .YDB_ORM import WhereConstructor, mainrunner, MetaModel, main
from rest_framework.response import Response
#from adrf.views import APIView
from rest_framework.views import APIView
import datetime
import time
from .models import *
import uuid
import jwt
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from .uploadFileClass import FileHosting

from django.core.mail import send_mail
from smtplib import SMTPDataError

# from .YDB_ORM import main


async def wrapper_select(mod_class: MetaModel, request, *args, **kwargs):
    print('args', args)
    print('kwargs', kwargs)
    data = mod_class.objects.select(*args, **kwargs)
    awaited_data = await data
    for _ in awaited_data[0].rows:
        pass
    print(f'--------------------- OBJECT is SELECT -- {mod_class}')
    return awaited_data


async def wrapper_post(mod_class: MetaModel, request_dict, *args, **kwargs):
    print("mod_class", mod_class, type(mod_class), mod_class)
    print("request_dict", request_dict)
    where_wrapper_post = WhereConstructor()
    print('request_dict', request_dict)
    where_wrapper_post.append('id', '==', request_dict['id'], 'and')
    await mod_class.objects.upsert(
        **request_dict
    )

    data = mod_class.objects.select(*args, where_settings=where_wrapper_post)
    awaited_data = await data
    for item in awaited_data[0].rows:
        print(item)
    print(f'--------------------- OBJECT {request_dict["id"]} is POST -- {mod_class}')
    return awaited_data


async def wrapper_delete(mod_class: MetaModel, request_dict, *args, **kwargs):
    where_wrapper_delete = WhereConstructor()
    if isinstance(request_dict['id'], bytes):
        where_wrapper_delete.append('id', '==', request_dict['id'].decode("utf-8"), 'or')
        print('request_dict[id].decode', request_dict['id'].decode("utf-8"))
        await mod_class.objects.delete(id="'" + request_dict['id'].decode("utf-8") + "'")
    else:
        where_wrapper_delete.append('id', '==', request_dict['id'], 'or')
        await mod_class.objects.delete(id="'" + request_dict['id'] + "'")
    data = mod_class.objects.select(*args, where_settings=where_wrapper_delete)
    awaited_data = await data
    for item in awaited_data[0].rows:
        print(item)
    if isinstance(request_dict['id'], bytes):
        print(f'--------------------- OBJECT {request_dict["id"].decode("utf-8")} is DELETE -- {mod_class}')
    else:
        print(f'--------------------- OBJECT {request_dict["id"]} is DELETE -- {mod_class}')
    return awaited_data

def token_check(token_auth_local):
    jwtd = jwt.decode(
        token_auth_local,
        os.environ.get("TOKEN_WORD"), algorithms=["HS256"])
    vr = int(time.mktime(datetime.datetime.now().timetuple())) + 3 * 60 * 60
    return jwt.encode({"login": jwtd['login'], "exp": vr, "access": jwtd['access']}, os.environ.get("TOKEN_WORD"), algorithm="HS256")

def get_link_file(obj):
    if obj:
        data = re.match("data:(?P<type>.*?);(?P<encoding>.*?),(?P<data>.*)", obj).groupdict()  # request.data['image']
        # data = data.split(',')
        # print("data", data[0])
        path_file = f"./coreApp/static/{str(uuid.uuid4())}.{data['type'].split('/')[-1]}"
        with open(path_file, "wb") as fh:
            fh.write(base64.decodebytes(bytes(data['data'], "ascii")))
            fh.close()
        # path = default_storage.save(f'./coreApp/static/{str(data)}', ContentFile(data.read()))
        tmp_file = os.path.join(settings.MEDIA_ROOT, path_file)
        bt = FileHosting()
        urlstr = bt.upload_file(tmp_file)
        os.remove(tmp_file)
        return urlstr
    return None

class ObjAPIView(APIView):
    model = None
    renderer_classes = [JSONRenderer]
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())

    # если ускорить, то вкл:
    # loop.create_task(mainrunner())
    # и убрать из select upseart delete в ydb_orm set_connection

    def get(self, request):
        token_auth = None
        if "HTTP_AUTHORIZATION" in request.META:
            token_auth = request.META['HTTP_AUTHORIZATION'].split(' ')[-1]
            try:
                token_auth = token_check(token_auth)
            except:
                return Response({"status": 'user is not authorized'})
        else:
            return Response({"status": 'user is not authorized'})
        answer_dict = {'token': token_auth}
        args = []
        where_constr = None
        print("request.GET", request.GET)
        print("request.data", request.data)
        # print(type(request.GET['Columns']), request.GET['Columns'].split(', '))

        if 'Columns' in request.GET.keys():
            print('Columns')
            for item in request.GET['Columns'].split(', '):
                print(item)
                args.append(item)
        if 'id' in request.GET.keys():
            where_constr = WhereConstructor()
            print('id')
            for item in request.GET['id'].split(', '):
                print(item)
                # where_constr.append(item['parameter'], item['operator'], item['meaning'], item['connection'])
                where_constr.append("id", "==", item, "or")
        ans = self.loop.run_until_complete(wrapper_select(self.model, request, *args, where_settings=where_constr))
        # print(request.data.keys(), request.data.values(), 'Columns' in request.data.keys())
        # ans = self.loop.run_until_complete(wrapper_select(self.model, request))
        list_object = []

        for item in ans[0].rows:
            list_object.append(item)
        list_object = list_object
        len_of_obj = len(list_object)
        if 'onList' in request.GET.keys():
            len_of_obj = len(list_object)
            count_elem_on_list = 10
            number_of_list = int(request.GET['onList']) - 1
            mn = count_elem_on_list * number_of_list
            mx = count_elem_on_list * (number_of_list+1) if count_elem_on_list * (number_of_list+1) < len_of_obj else len_of_obj
            print(mn, mx, list_object[mn:mx])
            answer_dict['Items'] = list_object[mn:mx]
        else:
            answer_dict['Items'] = list_object

        answer_dict["CountList"] = len_of_obj
        return Response(answer_dict)

    def post(self, request):
        token_auth = None
        if "HTTP_AUTHORIZATION" in request.META:
            token_auth = request.META['HTTP_AUTHORIZATION'].split(' ')[-1]
            try:
                token_auth = token_check(token_auth)
            except:
                return Response({"status": 'user is not authorized'})
        else:
            return Response({"status": 'user is not authorized'})
        list_participants = []
        print('Items', type(request.data['Items']))
        for request_item in request.data['Items']:
            request_item['id'] = str(uuid.uuid4())
            request_item['forSorted'] = int(time.mktime(datetime.datetime.now().timetuple()))
            resp = []
            resp.append(self.loop.run_until_complete(wrapper_post(self.model, request_item)))
            for i in resp:
                for item in i[0].rows:
                    list_participants.append(item)
        # return Response({"Items": list_participants, 'token': token_auth})
        return Response({'token': token_auth})

    def put(self, request):
        token_auth = None
        if "HTTP_AUTHORIZATION" in request.META:
            token_auth = request.META['HTTP_AUTHORIZATION'].split(' ')[-1]
            try:
                token_auth = token_check(token_auth)
            except:
                return Response({"status": 'user is not authorized'})
        else:
            return Response({"status": 'user is not authorized'})
        list_participants = []
        print('Items', type(request.data['Items']))
        for request_item in request.data['Items']:
            resp = []
            resp.append(self.loop.run_until_complete(wrapper_post(self.model, request_item)))
            for i in resp:
                for item in i[0].rows:
                    list_participants.append(item)
        # return Response({"Items": list_participants, 'token': token_auth})
        return Response({'token': token_auth})

    def delete(self, request):
        token_auth = None
        if "HTTP_AUTHORIZATION" in request.META:
            token_auth = request.META['HTTP_AUTHORIZATION'].split(' ')[-1]
            try:
                token_auth = token_check(token_auth)
            except:
                return Response({"status": 'user is not authorized'})
        else:
            return Response({"status": 'user is not authorized'})
        list_participants = []
        print('Items', type(request.GET['id']))
        for request_item in [{'id': i} for i in request.GET['id'].split(', ')]:
            request_item['id'] = request_item['id'].encode('utf-8')
            resp = self.loop.run_until_complete(wrapper_delete(self.model, request_item))
            request_item['id'] = request_item['id'].decode('utf-8')
            list_participants = []
            for item in resp[0].rows:
                list_participants.append(item)
        if len(list_participants) != 0 and len(request.GET['id'].split(', ')):
            # return Response({"Items": list_participants, "token": token_auth})
            return Response({"token": token_auth})
        return Response({'status': 'deletion error', 'token': token_auth})

class WrapperClass(ObjAPIView):
    def cascade_func(self, local_model, request_item, match_field, func, filter_value=False):

        list_obj_on_delete = []
        obj_id_list_where_constr = ['id']
        obj_on_delete_list_where_constr = WhereConstructor()
        obj_on_delete_list_where_constr.append(match_field, '==', request_item['id'])
        print("obj_on_delete_list_where_constr", obj_on_delete_list_where_constr)
        obj_id_on_delete_list = self.loop.run_until_complete(wrapper_select(local_model, request_item,
                                                                            *obj_id_list_where_constr,
                                                                            where_settings=obj_on_delete_list_where_constr))
        print("obj_id_on_delete_list", obj_id_on_delete_list)
        obj_on_delete_list = []
        for item in obj_id_on_delete_list[0].rows:
            obj_on_delete_list.append(item)
            print('obj_on_delete_list.item', item)
        for item in obj_on_delete_list:
            if filter_value:
                filt_where = WhereConstructor()
                filt_where.append(match_field, '==', request_item['id'])
                resp = self.loop.run_until_complete(func(local_model, item, where_settings=filt_where))
            else:
            # print("item", item, type(item), type(item['id']))
                resp = self.loop.run_until_complete(func(local_model, item))
            list_obj_on_delete = []
            for itm in resp[0].rows:
                list_obj_on_delete.append(itm)
        return list_obj_on_delete

    def filterSPORMA(self, request, model, connection_model, string_of_table, parameter_string, operator='=='):
        local_list = []
        local_args = [string_of_table]
        local_where_constr = WhereConstructor()
        print("request.GET['id'].split(', ')", request.GET['id'].split(', '))
        elem = [i for i in request.GET['id'].split(', ')]
        print("elem", elem)
        for i in elem:
            print("elem.i", i)
            local_where_constr.append(parameter_string, '==', i, 'or')
        id_list_sponsors = self.loop.run_until_complete(
            wrapper_select(connection_model, request, *local_args, where_settings=local_where_constr))
        local_where_constr.storage_conditions.clear()
        if len(id_list_sponsors) > 0 and len(id_list_sponsors[0].rows) > 0:
            print("id_list_sponsors", id_list_sponsors)
            for i in id_list_sponsors:
                print("id_list_sponsors.i", i.rows)
                for item in i.rows:
                    print("id_list_sponsors.i.item", item)
                    local_and_or = 'or' if operator == '==' else 'and'
                    local_where_constr.append('id', operator, item[string_of_table].decode("utf-8"), local_and_or)
            sl = self.loop.run_until_complete(
                wrapper_select(model, request, where_settings=local_where_constr))
            for i in sl[0].rows:
                local_list.append(i)
            print('----model, local_list, sl----', model, local_list, sl)
            return local_list
        if operator == "!=":
            sl = self.loop.run_until_complete(wrapper_select(model, request))
            for i in sl[0].rows:
                local_list.append(i)
            return local_list
        return []
    def filterTM(self, request, model, flag=True):
        team_list_answer = []
        team_id_constructor = WhereConstructor()
        elem = [i for i in request.GET['id'].split(', ')]
        for i in elem:
            if flag:
                team_id_constructor.append('event_id', '==', i, 'or')
            else:
                team_id_constructor.append('event_id', '==', None, 'or')
        tl = self.loop.run_until_complete(
            wrapper_select(model, request, where_settings=team_id_constructor))
        for i in tl[0].rows:
            count_participant_on_team_where = WhereConstructor()
            count_participant_on_team_where.append(parameter='team_id', operator='==', meaning=i['id'].decode('utf-8'), connection='and')
            count_participant_on_team_where.append(parameter='main', operator='==', meaning=True, connection='and')
            count_participant_on_team = self.loop.run_until_complete(wrapper_select(ParticipantsAPIView.model, request, where_settings=count_participant_on_team_where))
            i['count_participants'] = len(count_participant_on_team[0].rows)
            team_list_answer.append(i)
        return team_list_answer


    def statusNow(self, item):
        date_now = datetime.datetime.now()
        date_format = '%Y-%m-%dT%H:%M'
        if 'dateRegister' in item:
            # print(datetime.datetime.utcfromtimestamp(item['dateRegister']).strftime(date_format))
            item['dateRegister'] = datetime.datetime.fromtimestamp(item['dateRegister']).strftime(date_format)
            if date_now < datetime.datetime.strptime(item['dateRegister'], date_format):
                item['statusNow'] = "Ожидание регистрации"
            elif date_now >= datetime.datetime.strptime(item['dateRegister'], date_format):
                item['statusNow'] = "Регистрация открыта"
        if 'dateCloseRegister' in item:
            # print(datetime.datetime.utcfromtimestamp(item['dateCloseRegister']).strftime(date_format))
            item['dateCloseRegister'] = datetime.datetime.fromtimestamp(item['dateCloseRegister']).strftime(
                date_format)
            if date_now >= datetime.datetime.strptime(item['dateCloseRegister'], date_format):
                item['statusNow'] = "Регистрация закрыта"
        if 'dateStart' in item:
            # print(datetime.datetime.utcfromtimestamp(item['dateStart']).strftime(date_format))
            item['dateStart'] = datetime.datetime.fromtimestamp(item['dateStart']).strftime(date_format)
            if date_now >= datetime.datetime.strptime(item['dateStart'], date_format):
                item['statusNow'] = "Соревнование открыто"
        if 'dateEnd' in item:
            # print(datetime.datetime.utcfromtimestamp(item['dateEnd']).strftime(date_format))
            item['dateEnd'] = datetime.datetime.fromtimestamp(item['dateEnd']).strftime(date_format)
            if date_now >= datetime.datetime.strptime(item['dateEnd'], date_format):
                item['statusNow'] = "Соревнование закрыто"
        if 'timePublicationAdditionalMaterial' in item:
            item['timePublicationAdditionalMaterial'] = datetime.datetime.fromtimestamp(
                item['timePublicationAdditionalMaterial']).strftime(date_format)
            if date_now >= datetime.datetime.strptime(item['timePublicationAdditionalMaterial'], date_format):
                item['statusMaterials'] = True
            else:
                item['statusMaterials'] = False
        return item


class ParticipantsAPIView(ObjAPIView):
    model = Participants


class TeamsAPIView(WrapperClass):
    model = Teams

    def get(self, request):
        token_auth = None
        if "HTTP_AUTHORIZATION" in request.META:
            token_auth = request.META['HTTP_AUTHORIZATION'].split(' ')[-1]
            try:
                token_auth = token_check(token_auth)
            except:
                return Response({"status": 'user is not authorized'})
        else:
            return Response({"status": 'user is not authorized'})
        answer_dict = {'token': token_auth}
        args = []
        where_constr = None
        if 'Columns' in request.GET.keys():
            print('Columns')
            for item in request.GET['Columns'].split(', '):
                print(item)
                args.append(item)
        if 'id' in request.GET.keys():
            where_constr = WhereConstructor()
            print('id')
            for item in request.GET['id'].split(', '):
                print(item)
                # where_constr.append(item['parameter'], item['operator'], item['meaning'], item['connection'])
                where_constr.append("id", "==", item, "or")
        if 'event_id' in request.GET.keys():
            where_constr = WhereConstructor()
            where_constr.append("event_id", "==", request.GET['event_id'], "or")

        ans = self.loop.run_until_complete(wrapper_select(self.model, request, *args, where_settings=where_constr))
        # print(request.data.keys(), request.data.values(), 'Columns' in request.data.keys())
        # ans = self.loop.run_until_complete(wrapper_select(self.model, request))
        list_teams = []
        event_list = []
        for item in ans[0].rows:
            list_teams.append(item)
            if 'event_id' in item and item['event_id'] is not None:
                count_participants_where_constr = WhereConstructor()
                count_participants_where_constr.append(parameter='id', operator='==', meaning=item['event_id'].decode('utf-8'))
                count_participants_on_event = self.loop.run_until_complete(
                    wrapper_select(EventsAPIView.model, request, 'minNumberOfParticipants', 'maxNumberOfParticipants', 'name',
                               where_settings=count_participants_where_constr))
                for event_info in count_participants_on_event[0].rows:
                    event_list.append(event_info)

            # self, local_model, request_item, match_field, func
        #--------------------------------------------------------------------------------------------
        if "id" in request.GET.keys():
            participants_list = []
            for request_item in [i for i in request.GET['id'].split(', ')]:
                print("request_item", request_item)
                # participants_list.append(self.cascade_func(ParticipantsAPIView.model, request_item, 'team_id', wrapper_select))
                participants_id_constructor = WhereConstructor()
                participants_id_constructor.append('team_id', '==', request_item, 'or')
                tl = self.loop.run_until_complete(
                    wrapper_select(ParticipantsAPIView.model, request, where_settings=participants_id_constructor))
                for i in tl[0].rows:
                    participants_list.append(i)


            return Response({"TeamData": list_teams, "ParticipantData": participants_list, "EventData": event_list, "token": token_auth})
            # return Response({"token": token_auth})
        answer_dict['Items'] = list_teams
        len_of_obj = len(list_teams)
        if 'onList' in request.GET.keys():
            count_elem_on_list = 10
            number_of_list = int(request.GET['onList']) - 1
            mn = count_elem_on_list * number_of_list
            mx = count_elem_on_list * (number_of_list + 1) if count_elem_on_list * (
                        number_of_list + 1) < len_of_obj else len_of_obj
            print(mn, mx, list_teams[mn:mx])
            answer_dict['Items'] = list_teams[mn:mx]
        else:
            answer_dict['Items'] = list_teams

        answer_dict["CountList"] = len_of_obj
        # if 'onList' in request.GET.keys():
        #     print("request.GET['onList']", request.GET['onList'])
        #     if bool(request.GET['onList']):
        #         count_elem_on_list = 10
        #         len_of_obj = len(list_teams)
        #         count_list = (len_of_obj // count_elem_on_list) + 1
        #         print("count_list", count_list)
        #         for item in range(count_list):
        #             print(item)
        #             mn = count_elem_on_list * item
        #             mx = count_elem_on_list * (item+1) if count_elem_on_list * (item+1) < len_of_obj else len_of_obj
        #             print(mn, mx, list_teams[mn:mx])
        #             answer_dict[f'ItemsList{str(item)}'] = list_teams[mn:mx]


        return Response(answer_dict)

    def post(self, request):
        token_auth = None
        if "HTTP_AUTHORIZATION" in request.META:
            token_auth = request.META['HTTP_AUTHORIZATION'].split(' ')[-1]
            try:
                token_auth = token_check(token_auth)
            except:
                return Response({"status": 'user is not authorized'})
        else:
            return Response({"status": 'user is not authorized'})
        list_team_data = []
        request.data['TeamData']['id'] = str(uuid.uuid4())
        request.data['TeamData']['forSorted'] = int(time.mktime(datetime.datetime.now().timetuple()))
        resp = []
        # print("request.data['TeamData']", request.data['TeamData'])
        resp.append(self.loop.run_until_complete(wrapper_post(self.model, request.data['TeamData'])))
        for i in resp:
            for item in i[0].rows:
                list_team_data.append(item)

        try:
            list_participants = []
            # print('TeamListParticipantsData', type(request.data['TeamListParticipantsData']))
            for request_item in request.data['TeamListParticipantsData']:
                request_item['id'] = str(uuid.uuid4())
                request_item['forSorted'] = int(time.mktime(datetime.datetime.now().timetuple()))
                request_item['team_id'] = request.data['TeamData']['id']
                if 'event_id' in request.data['TeamData']:
                    # print('==================', type(request.data['TeamData']['event_id']), len(request.data['TeamData']['event_id']), request.data['TeamData']['event_id'], type(''), request.data['TeamData']['event_id'] != "")
                    request_item['event_id'] = request.data['TeamData']['event_id']
                else:
                    request_item['event_id'] = None

                resp = []
                resp.append(self.loop.run_until_complete(wrapper_post(ParticipantsAPIView.model, request_item)))
                for i in resp:
                    for item in i[0].rows:
                        list_participants.append(item)
        except:
            resp = self.loop.run_until_complete(wrapper_delete(self.model, request.data['TeamData']))
            list_participants = []
            for item in resp[0].rows:
                list_participants.append(item)
            return Response({'status': 'add error', 'token': token_auth})
        if "event_id" in request.data['TeamData']:
            where_constr_for_email = WhereConstructor()
            where_constr_for_email.append('id', '==', request.data['TeamData']['event_id'])
            # print("where_constr_for_email", where_constr_for_email)
            event_name_select = self.loop.run_until_complete(wrapper_select(EventsAPIView.model, request, 'name', where_settings=where_constr_for_email))
            # print(event_name_select)
            event = []
            for item in event_name_select[0].rows:
                event.append(item)
            # print(event[0]['name'].decode('utf-8'))
            if len(event) > 0:
                event = event[0]['name'].decode('utf-8')
                text = "принята."
                print('------', [i['emailAdress'].decode('utf-8') for i in list_participants])

                try:
                    send_mail("LIDcode event status", f"Ваша заявка регистрации на соревнование '{event}' "
                                                      f"{text}",
                              settings.EMAIL_HOST_USER, [i['emailAdress'].decode('utf-8') for i in list_participants])
                except SMTPDataError as e:
                    print('There was an error sending an email: ', e)
        # return Response({"TeamData": list_team_data, "TeamListParticipantsData": list_participants, 'token': token_auth})
        return Response({'token': token_auth})

    def put(self, request):
        token_auth = None
        if "HTTP_AUTHORIZATION" in request.META:
            token_auth = request.META['HTTP_AUTHORIZATION'].split(' ')[-1]
            try:
                token_auth = token_check(token_auth)
            except:
                return Response({"status": 'user is not authorized'})
        else:
            return Response({"status": 'user is not authorized'})
        list_team_data = []
        # print('TeamData', request.data['TeamData'])
        # print(request.data['TeamData'])
        resp = []
        # print("request.data['TeamData']", request.data['TeamData'])
        if 'event_id' in request.data['TeamData'].keys():
            if request.data['TeamData']["event_id"] == "":
                request.data['TeamData']['event_id'] = None
        else:
            request.data['TeamData']['event_id'] = None
        resp.append(self.loop.run_until_complete(wrapper_post(self.model, request.data['TeamData'])))
        for i in resp:
            for item in i[0].rows:
                list_team_data.append(item)

        # participants_id_list_args = ['id']
        # participants_id_list_where_constr = WhereConstructor()
        # participants_id_list_where_constr.append('team_id', '==', request.data['TeamData']['id'])
        # id_list_participants = self.loop.run_until_complete(
        #     wrapper_select(ParticipantsAPIView.model, request, *participants_id_list_args,
        #                    where_settings=participants_id_list_where_constr))
        # participants_id_list_before = []
        # for item in id_list_participants[0].rows:
        #     participants_id_list_before.append(item['id'])
        # print('participants_id_list_before', participants_id_list_before)
        # participants_id_list_after = [i.get('id') for i in request.data['TeamListParticipantsData']]
        # print('participants_id_list_after', participants_id_list_after)
        # participants_id_list_on_delete = list(
        #     set(participants_id_list_before).symmetric_difference(set(participants_id_list_after)))
        # print('participants_id_list_on_delete', participants_id_list_on_delete)
        # for item in [{'id': i} for i in participants_id_list_on_delete]:
        #     print('item', item)
        #     resp = self.loop.run_until_complete(wrapper_delete(ParticipantsAPIView.model, item))
        #     list_participants = []
        #     for item in resp[0].rows:
        #         list_participants.append(item)
        #     print("list_participants", list_participants)

        participants_id_list_on_delete = self.cascade_func(ParticipantsAPIView.model, request.data['TeamData'],
                                                           'team_id',
                                                           wrapper_delete)
        for _ in participants_id_list_on_delete:
            pass

        try:
            list_participants = []
            # print('TeamListParticipantsData', type(request.data['TeamListParticipantsData']))
            for request_item in request.data['TeamListParticipantsData']:
                if 'id' not in request_item.keys():
                    request_item['id'] = str(uuid.uuid4())
                request_item['team_id'] = request.data['TeamData']['id']
                request_item['event_id'] = request.data['TeamData']['event_id']
                request_item['forSorted'] = int(time.mktime(datetime.datetime.now().timetuple()))
                resp = []
                resp.append(self.loop.run_until_complete(wrapper_post(ParticipantsAPIView.model, request_item)))
                for i in resp:
                    for item in i[0].rows:
                        list_participants.append(item)
        except:
            resp = self.loop.run_until_complete(wrapper_delete(self.model, request.data['TeamData']))
            list_participants = []
            for item in resp[0].rows:
                list_participants.append(item)
            return Response({'status': 'add error', "token": token_auth})
        # return Response({"TeamData": list_team_data, "TeamListParticipantsData": list_participants, 'token': token_auth})
        return Response({'token': token_auth})

    def delete(self, request):
        token_auth = None
        if "HTTP_AUTHORIZATION" in request.META:
            token_auth = request.META['HTTP_AUTHORIZATION'].split(' ')[-1]
            try:
                token_auth = token_check(token_auth)
            except:
                return Response({"status": 'user is not authorized'})
        else:
            return Response({"status": 'user is not authorized'})
        list_team = []
        list_participants_on_delete = []
        print('Items', type(request.GET['id'].split(', ')))
        for request_item in [{'id': i} for i in request.GET['id'].split(', ')]:
            request_item['id'] = request_item['id'].encode('utf-8')
            resp = self.loop.run_until_complete(wrapper_delete(self.model, request_item))
            request_item['id'] = request_item['id'].decode('utf-8')
            list_team = []
            for item in resp[0].rows:
                list_team.append(item)

            list_participants_on_delete = self.cascade_func(ParticipantsAPIView.model, request_item, 'team_id',
                                                            wrapper_delete)
            # for item in resp[0].rows:
            #     list_participants_on_delete.append(item)

        # return Response({"TeamData": list_team, "ParticipantData": list_participants_on_delete, 'token': token_auth})
        return Response({'token': token_auth})


class MaterialsAPIView(ObjAPIView):
    model = Materials
    def get(self, request):
        token_auth = None
        if "HTTP_AUTHORIZATION" in request.META:
            token_auth = request.META['HTTP_AUTHORIZATION'].split(' ')[-1]
            try:
                token_auth = token_check(token_auth)
            except:
                return Response({"status": 'user is not authorized'})
        else:
            return Response({"status": 'user is not authorized'})
        answer_dict = {'token': token_auth}
        args = []
        where_constr = None
        print("request.GET", request.GET)
        print("request.data", request.data)
        # print(type(request.GET['Columns']), request.GET['Columns'].split(', '))

        if 'Columns' in request.GET.keys():
            print('Columns')
            for item in request.GET['Columns'].split(', '):
                print(item)
                args.append(item)
        if 'id' in request.GET.keys():
            where_constr = WhereConstructor()
            print('id')
            for item in request.GET['id'].split(', '):
                print(item)
                # where_constr.append(item['parameter'], item['operator'], item['meaning'], item['connection'])
                where_constr.append("id", "==", item, "or")
        if 'event_id' in request.GET.keys():

            event_search_where_constr = WhereConstructor()
            event_search_where_constr.append("event_id", "==", request.GET['event_id'], "or")
            materials_this_event = self.loop.run_until_complete(wrapper_select(EventMaterialAPIView.model, request, 'material_id', where_settings=event_search_where_constr))
            if 'id' not in request.GET.keys() and len(materials_this_event[0].rows) > 0:
                where_constr = WhereConstructor()

            if len(materials_this_event[0].rows) > 0:
                for item in materials_this_event[0].rows:
                    where_constr.append("id", "==", item['material_id'].decode('utf-8'), "or")
                    print("item /////////////////////////////", item)
                    print("item['material_id'] /////////////////////////////", item['material_id'])
            else:
                where_constr = WhereConstructor()
                where_constr.append('id', '==', 'pass')

        ans = self.loop.run_until_complete(wrapper_select(self.model, request, *args, where_settings=where_constr))
        # print(request.data.keys(), request.data.values(), 'Columns' in request.data.keys())
        # ans = self.loop.run_until_complete(wrapper_select(self.model, request))
        list_object = []

        for item in ans[0].rows:
            list_object.append(item)
        list_object = list_object
        len_of_obj = len(list_object)
        if 'onList' in request.GET.keys():
            len_of_obj = len(list_object)
            count_elem_on_list = 10
            number_of_list = int(request.GET['onList']) - 1
            mn = count_elem_on_list * number_of_list
            mx = count_elem_on_list * (number_of_list+1) if count_elem_on_list * (number_of_list+1) < len_of_obj else len_of_obj
            print(mn, mx, list_object[mn:mx])
            answer_dict['Items'] = list_object[mn:mx]
        else:
            answer_dict['Items'] = list_object

        answer_dict["CountList"] = len_of_obj
        return Response(answer_dict)

    def post(self, request):
        token_auth = None
        if "HTTP_AUTHORIZATION" in request.META:
            token_auth = request.META['HTTP_AUTHORIZATION'].split(' ')[-1]
            try:
                token_auth = token_check(token_auth)
            except:
                return Response({"status": 'user is not authorized'})
        else:
            return Response({"status": 'user is not authorized'})
        list_obj = []
        print('Items', type(request.data['Items']))
        for request_item in request.data['Items']:
            request_item['id'] = str(uuid.uuid4())
            request_item['forSorted'] = int(time.mktime(datetime.datetime.now().timetuple()))
            if "file" in request_item.keys():
                request_item['file'] = get_link_file(request_item['file'])
            resp = []
            resp.append(self.loop.run_until_complete(wrapper_post(self.model, request_item)))
            for i in resp:
                for item in i[0].rows:
                    list_obj.append(item)
        # return Response({"Items": list_obj, "token": token_auth})
        return Response({"token": token_auth})

    def put(self, request):
        token_auth = None
        if "HTTP_AUTHORIZATION" in request.META:
            token_auth = request.META['HTTP_AUTHORIZATION'].split(' ')[-1]
            try:
                token_auth = token_check(token_auth)
            except:
                return Response({"status": 'user is not authorized'})
        else:
            return Response({"status": 'user is not authorized'})
        list_participants = []
        print('Items', type(request.data['Items']))
        for request_item in request.data['Items']:
            if "file" in request_item.keys():
                request_item['file'] = get_link_file(request_item['file'])
            resp = []
            resp.append(self.loop.run_until_complete(wrapper_post(self.model, request_item)))
            for i in resp:
                for item in i[0].rows:
                    list_participants.append(item)
        # return Response({"Items": list_participants, 'token': token_auth})
        return Response({'token': token_auth})


class OrganizersAPIView(ObjAPIView):
    model = Organizers

    def post(self, request):
        token_auth = None
        if "HTTP_AUTHORIZATION" in request.META:
            token_auth = request.META['HTTP_AUTHORIZATION'].split(' ')[-1]
            try:
                token_auth = token_check(token_auth)
            except:
                return Response({"status": 'user is not authorized'})
        else:
            return Response({"status": 'user is not authorized'})
        list_obj = []
        print('Items', type(request.data['Items']))
        for request_item in request.data['Items']:
            request_item['id'] = str(uuid.uuid4())
            request_item['forSorted'] = int(time.mktime(datetime.datetime.now().timetuple()))
            if 'imageDef' in request_item.keys():
                request_item['imageDef'] = get_link_file(request_item['imageDef'])
            if 'imageHor' in request_item.keys():
                request_item['imageHor'] = get_link_file(request_item['imageHor'])
            if 'imageVer' in request_item.keys():
                request_item['imageVer'] = get_link_file(request_item['imageVer'])
            resp = []
            resp.append(self.loop.run_until_complete(wrapper_post(self.model, request_item)))
            for i in resp:
                for item in i[0].rows:
                    list_obj.append(item)
        # return Response({"Items": list_obj, "token": token_auth})
        return Response({"token": token_auth})

    def put(self, request):
        token_auth = None
        if "HTTP_AUTHORIZATION" in request.META:
            token_auth = request.META['HTTP_AUTHORIZATION'].split(' ')[-1]
            try:
                token_auth = token_check(token_auth)
            except:
                return Response({"status": 'user is not authorized'})
        else:
            return Response({"status": 'user is not authorized'})
        list_participants = []
        print('Items', type(request.data['Items']))
        for request_item in request.data['Items']:
            if 'imageDef' in request_item.keys():
                request_item['imageDef'] = get_link_file(request_item['imageDef'])
            if 'imageHor' in request_item.keys():
                request_item['imageHor'] = get_link_file(request_item['imageHor'])
            if 'imageVer' in request_item.keys():
                request_item['imageVer'] = get_link_file(request_item['imageVer'])
            resp = []
            resp.append(self.loop.run_until_complete(wrapper_post(self.model, request_item)))
            for i in resp:
                for item in i[0].rows:
                    list_participants.append(item)
        # return Response({"Items": list_participants, "token": token_auth})
        return Response({"token": token_auth})


class SponsorsAPIView(ObjAPIView):
    model = Sponsors

    def post(self, request):
        token_auth = None
        if "HTTP_AUTHORIZATION" in request.META:
            token_auth = request.META['HTTP_AUTHORIZATION'].split(' ')[-1]
            try:
                token_auth = token_check(token_auth)
            except:
                return Response({"status": 'user is not authorized'})
        else:
            return Response({"status": 'user is not authorized'})
        list_obj = []
        print('Items', type(request.data['Items']))
        for request_item in request.data['Items']:
            request_item['id'] = str(uuid.uuid4())
            request_item['forSorted'] = int(time.mktime(datetime.datetime.now().timetuple()))
            if 'imageDef' in request_item.keys():
                request_item['imageDef'] = get_link_file(request_item['imageDef'])
            if 'imageHor' in request_item.keys():
                request_item['imageHor'] = get_link_file(request_item['imageHor'])
            if 'imageVer' in request_item.keys():
                request_item['imageVer'] = get_link_file(request_item['imageVer'])

            resp = []
            resp.append(self.loop.run_until_complete(wrapper_post(self.model, request_item)))
            for i in resp:
                for item in i[0].rows:
                    list_obj.append(item)
        # return Response({"Items": list_obj, 'token':token_auth})
        return Response({'token': token_auth})

    def put(self, request):
        token_auth = None
        if "HTTP_AUTHORIZATION" in request.META:
            token_auth = request.META['HTTP_AUTHORIZATION'].split(' ')[-1]
            try:
                token_auth = token_check(token_auth)
            except:
                return Response({"status": 'user is not authorized'})
        else:
            return Response({"status": 'user is not authorized'})
        list_participants = []
        print('Items', type(request.data['Items']))
        for request_item in request.data['Items']:
            if 'imageDef' in request_item.keys():
                request_item['imageDef'] = get_link_file(request_item['imageDef'])
            if 'imageHor' in request_item.keys():
                request_item['imageHor'] = get_link_file(request_item['imageHor'])
            if 'imageVer' in request_item.keys():
                request_item['imageVer'] = get_link_file(request_item['imageVer'])

            resp = []
            resp.append(self.loop.run_until_complete(wrapper_post(self.model, request_item)))
            for i in resp:
                for item in i[0].rows:
                    list_participants.append(item)
        # return Response({"Items": list_participants, 'token': token_auth})
        return Response({'token': token_auth})


class EventsAPIView(WrapperClass):
    model = Events

    def get(self, request):
        token_auth = None
        if "HTTP_AUTHORIZATION" in request.META:
            token_auth = request.META['HTTP_AUTHORIZATION'].split(' ')[-1]
            try:
                token_auth = token_check(token_auth)
            except:
                return Response({"status": 'user is not authorized'})
        else:
            return Response({"status": 'user is not authorized'})
        answer_dict = {'token': token_auth}
        args = []
        where_constr = None
        if 'Columns' in request.GET.keys():
            print('Columns')
            for item in request.GET['Columns'].split(', '):
                print(item)
                args.append(item)
        if 'id' in request.GET.keys():
            where_constr = WhereConstructor()
            print('id')
            for item in request.GET['id'].split(', '):
                print(item)
                # where_constr.append(item['parameter'], item['operator'], item['meaning'], item['connection'])
                where_constr.append("id", "==", item, "or")
        event_data = self.loop.run_until_complete(
            wrapper_select(self.model, request, *args, where_settings=where_constr))
        # print(request.data.keys(), request.data.values(), 'Columns' in request.data.keys())
        # ans = self.loop.run_until_complete(wrapper_select(self.model, request))
        list_event_data = []

        for item in event_data[0].rows:
            item = self.statusNow(item)
            list_event_data.append(item)

        if "id" in request.GET.keys():
            sponsors_list = []
            organizers_list = []
            materials_list = []
            team_list = []

            sponsors_all_list = self.filterSPORMA(request, SponsorsAPIView.model, EventSponsorAPIView.model,
                                                  'sponsor_id', "event_id", '!=')
            organizers_all_list = self.filterSPORMA(request, OrganizersAPIView.model, EventOrganizerAPIView.model,
                                                    'organizer_id', "event_id", '!=')
            materials_all_list = self.filterSPORMA(request, MaterialsAPIView.model, EventMaterialAPIView.model,
                                                   'material_id', "event_id", '!=')



            # sponsors_all_list = []
            # sal = self.loop.run_until_complete(
            #     wrapper_select(SponsorsAPIView.model, request))
            # for i in sal[0].rows:
            #     sponsors_all_list.append(i)

            # organizers_all_list = []
            # oal = self.loop.run_until_complete(
            #     wrapper_select(OrganizersAPIView.model, request))
            # for i in oal[0].rows:
            #     organizers_all_list.append(i)

            # materials_all_list = []
            # mal = self.loop.run_until_complete(
            #     wrapper_select(MaterialsAPIView.model, request))
            # for i in mal[0].rows:
            #     materials_all_list.append(i)
            sponsors_list = self.filterSPORMA(request, SponsorsAPIView.model, EventSponsorAPIView.model, 'sponsor_id',
                                              "event_id")

            organizers_list = self.filterSPORMA(request, OrganizersAPIView.model, EventOrganizerAPIView.model,
                                            'organizer_id', "event_id")

            materials_list = self.filterSPORMA(request, MaterialsAPIView.model, EventMaterialAPIView.model,
                                           'material_id', "event_id")

            team_list = self.filterTM(request, TeamsAPIView.model)

            team_free_list = self.filterTM(request, TeamsAPIView.model, False)

            # team_id_constructor = WhereConstructor()
            # # team_id_constructor.append('event_id', '==', )
            # elem = [i.get('meaning') for i in request.data['Where'] if i.get('parameter') == 'id']
            # for i in elem:
            #     team_id_constructor.append('event_id', '==', i['meaning'], 'or')
            # tl = self.loop.run_until_complete(
            #     wrapper_select(TeamsAPIView.model, request, where_settings=team_id_constructor))
            # for i in tl[0].rows:
            #     team_list.append(i)

            return Response({
                "EventData": list_event_data,
                "SponsorEventData": sponsors_list,
                "OrganizerEventData": organizers_list,
                "MaterialEventData": materials_list,
                "SponsorOtherData": sponsors_all_list,
                "OrganizerOtherData": organizers_all_list,
                "MaterialOtherData": materials_all_list,
                "TeamEventData": team_list,
                "TeamOtherData": team_free_list,
                'token': token_auth
            })

        len_of_obj = len(list_event_data)
        if 'onList' in request.GET.keys():
            count_elem_on_list = 10
            number_of_list = int(request.GET['onList']) - 1
            mn = count_elem_on_list * number_of_list
            mx = count_elem_on_list * (number_of_list + 1) if count_elem_on_list * (
                        number_of_list + 1) < len_of_obj else len_of_obj
            print(mn, mx, list_event_data[mn:mx])
            answer_dict['Items'] = list_event_data[mn:mx]
        else:
            answer_dict['Items'] = list_event_data

        answer_dict["CountList"] = len_of_obj
        # answer_dict['Items'] = list_event_data
        # if 'onList' in request.GET.keys():
        #     print("request.GET['onList']", request.GET['onList'])
        #     if bool(request.GET['onList']):
        #         count_elem_on_list = 10
        #         len_of_obj = len(list_event_data)
        #         count_list = (len_of_obj // count_elem_on_list) + 1
        #         print("count_list", count_list)
        #         for item in range(count_list):
        #             print(item)
        #             mn = count_elem_on_list * item
        #             mx = count_elem_on_list * (item + 1) if count_elem_on_list * (item + 1) < len_of_obj else len_of_obj
        #             print(mn, mx, list_event_data[mn:mx])
        #             answer_dict[f'ItemsList{str(item)}'] = list_event_data[mn:mx]

        return Response(answer_dict)

    def post(self, request):
        token_auth = None
        if "HTTP_AUTHORIZATION" in request.META:
            token_auth = request.META['HTTP_AUTHORIZATION'].split(' ')[-1]
            try:
                token_auth = token_check(token_auth)
            except:
                return Response({"status": 'user is not authorized'})
        else:
            return Response({"status": 'user is not authorized'})
        answer_dict = {'token': token_auth}
        list_event_data = []
        request.data['EventData']['id'] = str(uuid.uuid4())
        request.data['EventData']['forSorted'] = int(time.mktime(datetime.datetime.now().timetuple()))
        if 'imageDef' in request.data['EventData'].keys():
            request.data['EventData']['imageDef'] = get_link_file(request.data['EventData']['imageDef'])
        if 'imageHor' in request.data['EventData'].keys():
            request.data['EventData']['imageHor'] = get_link_file(request.data['EventData']['imageHor'])
        if 'imageVer' in request.data['EventData'].keys():
            request.data['EventData']['imageVer'] = get_link_file(request.data['EventData']['imageVer'])
        date_format = '%Y-%m-%dT%H:%M'
        if "maxNumberOfTeam" in request.data['EventData']:
            request.data['EventData']['maxNumberOfTeam'] = int(request.data['EventData']['maxNumberOfTeam'])
        if "minNumberOfParticipants" in request.data['EventData']:
            request.data['EventData']['minNumberOfParticipants'] = int(
                request.data['EventData']['minNumberOfParticipants'])
        if "maxNumberOfParticipants" in request.data['EventData']:
            request.data['EventData']['maxNumberOfParticipants'] = int(
                request.data['EventData']['maxNumberOfParticipants'])
        if 'dateStart' in request.data['EventData']:
            request.data['EventData']['dateStart'] = int(
                time.mktime(
                    datetime.datetime.strptime(request.data['EventData']['dateStart'], date_format).timetuple()))
        if 'dateEnd' in request.data['EventData']:
            request.data['EventData']['dateEnd'] = int(
                time.mktime(datetime.datetime.strptime(request.data['EventData']['dateEnd'], date_format).timetuple()))
        if 'dateRegister' in request.data['EventData']:
            request.data['EventData']['dateRegister'] = int(
                time.mktime(
                    datetime.datetime.strptime(request.data['EventData']['dateRegister'], date_format).timetuple()))
        if 'dateCloseRegister' in request.data['EventData']:
            request.data['EventData']['dateCloseRegister'] = int(time.mktime(
                datetime.datetime.strptime(request.data['EventData']['dateCloseRegister'], date_format).timetuple()))
        if 'timePublicationAdditionalMaterial' in request.data['EventData']:
            request.data['EventData']['timePublicationAdditionalMaterial'] = int(time.mktime(
                datetime.datetime.strptime(request.data['EventData']['timePublicationAdditionalMaterial'],
                                           date_format).timetuple()))

        resp = []
        resp.append(self.loop.run_until_complete(wrapper_post(self.model, request.data['EventData'])))
        for i in resp:
            for item in i[0].rows:
                list_event_data.append(item)

        # model_tag_dict = {"OrganizersList": (OrganizersAPIView.model, [],),
        #                   "SponsorsList": (SponsorsAPIView.model, [],),
        #                   "MaterialsList": (MaterialsAPIView.model, [],)}
        # # list_obj = []
        # for i in model_tag_dict.keys():
        #     print('i', type(request.data[i]))
        #     for request_item in request.data[i]:
        #         local_model = model_tag_dict[i][0]
        #         get_list_id = self.loop.run_until_complete(get_new_id(local_model, request_item))
        #         list_id = []
        #         for variable_id in get_list_id[0].rows:
        #             list_id.append(variable_id.get('id'))
        #         if len(list_id) != 0:
        #             new_id = max(list_id) + 1
        #         else:
        #             new_id = 0
        #         request_item['id'] = new_id
        #         resp = []
        #         resp.append(self.loop.run_until_complete(wrapper_post(local_model, request_item)))
        #         for i in resp:
        #             for item in i[0].rows:
        #                 model_tag_dict[i][1].append(item)
        answer_dict["Items"] = list_event_data
        # for i in model_tag_dict.keys():
        #     answer_dict[i] = model_tag_dict[i][1]

        return Response(answer_dict)

    def put(self, request):
        token_auth = None
        if "HTTP_AUTHORIZATION" in request.META:
            token_auth = request.META['HTTP_AUTHORIZATION'].split(' ')[-1]
            try:
                token_auth = token_check(token_auth)
            except:
                return Response({"status": 'user is not authorized'})
        else:
            return Response({"status": 'user is not authorized'})
        answer_dict = {'token': token_auth}
        list_event_data = []
        # get_list_id = self.loop.run_until_complete(get_new_id(self.model, request.data['EventData']))
        # list_id = []
        # for variable_id in get_list_id[0].rows:
        #     list_id.append(variable_id.get('id'))
        # if len(list_id) != 0:
        #     new_id = max(list_id) + 1
        # else:
        #     new_id = 0
        # request.data['EventData']['id'] = new_id
        resp = []
        if 'imageDef' in request.data['EventData'].keys():
            request.data['EventData']['imageDef'] = get_link_file(request.data['EventData']['imageDef'])
        if 'imageHor' in request.data['EventData'].keys():
            request.data['EventData']['imageHor'] = get_link_file(request.data['EventData']['imageHor'])
        if 'imageVer' in request.data['EventData'].keys():
            request.data['EventData']['imageVer'] = get_link_file(request.data['EventData']['imageVer'])
        if 'results' in request.data['EventData'].keys():
            request.data['EventData']['results'] = get_link_file(request.data['EventData']['results'])
        date_format = '%Y-%m-%dT%H:%M'
        if "maxNumberOfTeam" in request.data['EventData']:
            request.data['EventData']['maxNumberOfTeam'] = int(request.data['EventData']['maxNumberOfTeam'])
        if "minNumberOfParticipants" in request.data['EventData']:
            request.data['EventData']['minNumberOfParticipants'] = int(
                request.data['EventData']['minNumberOfParticipants'])
        if "maxNumberOfParticipants" in request.data['EventData']:
            request.data['EventData']['maxNumberOfParticipants'] = int(
                request.data['EventData']['maxNumberOfParticipants'])
        if 'dateStart' in request.data['EventData']:
            request.data['EventData']['dateStart'] = int(
                time.mktime(
                    datetime.datetime.strptime(request.data['EventData']['dateStart'], date_format).timetuple()))
        if 'dateEnd' in request.data['EventData']:
            request.data['EventData']['dateEnd'] = int(
                time.mktime(datetime.datetime.strptime(request.data['EventData']['dateEnd'], date_format).timetuple()))
        if 'dateRegister' in request.data['EventData']:
            request.data['EventData']['dateRegister'] = int(
                time.mktime(
                    datetime.datetime.strptime(request.data['EventData']['dateRegister'], date_format).timetuple()))
        if 'dateCloseRegister' in request.data['EventData']:
            request.data['EventData']['dateCloseRegister'] = int(time.mktime(
                datetime.datetime.strptime(request.data['EventData']['dateCloseRegister'], date_format).timetuple()))
        if 'timePublicationAdditionalMaterial' in request.data['EventData']:
            request.data['EventData']['timePublicationAdditionalMaterial'] = int(time.mktime(
                datetime.datetime.strptime(request.data['EventData']['timePublicationAdditionalMaterial'],
                                           date_format).timetuple()))

        resp.append(self.loop.run_until_complete(wrapper_post(self.model, request.data['EventData'])))
        for i in resp:
            for item in i[0].rows:
                list_event_data.append(item)
        # TODO команды и участники
        model_tag_dict = {"OrganizersList": (OrganizersAPIView.model, [], EventOrganizerAPIView.model, "organizer_id"),
                          "SponsorsList": (SponsorsAPIView.model, [], EventSponsorAPIView.model, "sponsor_id"),
                          "MaterialsList": (MaterialsAPIView.model, [], EventMaterialAPIView.model, "material_id"),
                          # "EventOrganizerList": (EventOrganizerAPIView.model, [],),
                          # "EventSponsorList": (EventSponsorAPIView.model, [],),
                          # "EventMaterial": (EventMaterialAPIView.model, [],),
                          "TeamsList": (TeamsAPIView.model, [], False)}
        # list_obj = []
        for i in model_tag_dict.keys():
            print('type(request.data[i]', type(request.data[i]))
            # if not model_tag_dict[i][2]:
            #     self.cascade_func(TeamsAPIView.model, request.data['EventData'], 'event_id', wrapper_delete)
            if model_tag_dict[i][2]:
                obj_list_on_delete = self.cascade_func(model_tag_dict[i][2], request.data['EventData'],
                                                   'event_id',
                                                   wrapper_delete)
                print("obj_list_on_delete", obj_list_on_delete)
            if not model_tag_dict[i][2]:
                obj_team_on_delete_where = WhereConstructor()
                obj_team_on_delete_where.append('event_id', '==', request.data['EventData']['id'])
                obj_list_on_delete = self.loop.run_until_complete(wrapper_select(model_tag_dict[i][0], None, where_settings=obj_team_on_delete_where))
                print("+++ obj_list_on_delete", obj_list_on_delete)
                for id_team_del in obj_list_on_delete:
                    print("+++ id_team_del", id_team_del.rows)
                    for id_team in id_team_del.rows:
                        print('+++ id_team', id_team)
                        id_team['event_id'] = None
                        for p in id_team:
                            if isinstance(id_team[p], bytes):
                                id_team[p] = id_team[p].decode('utf-8')
                        self.loop.run_until_complete(wrapper_post(TeamsAPIView.model, id_team))

            for request_item in request.data[i]:
                local_model = model_tag_dict[i][0]
                # get_list_id = self.loop.run_until_complete(get_new_id(local_model, request_item))
                # list_id = []
                # for variable_id in get_list_id[0].rows:
                #     list_id.append(variable_id.get('id'))
                # if len(list_id) != 0:
                #     new_id = max(list_id) + 1
                # else:
                #     new_id = 0
                # request_item['id'] = new_id
                if model_tag_dict[i][2]:
                    print("model_tag_dict[i][2] create new ", model_tag_dict[i][2])
                    # obj_list_on_delete = self.cascade_func(model_tag_dict[i][2], request.data['EventData'],
                    #                                        'event_id',
                    #                                        wrapper_delete)
                    # print("obj_list_on_delete", obj_list_on_delete)
                    # for _ in obj_list_on_delete:
                    #     pass

                    new_connection_obj = {'id': str(uuid.uuid4()),
                                          "event_id": request.data['EventData']['id'],
                                          model_tag_dict[i][3]: request_item['id'],
                                          "forSorted": int(time.mktime(datetime.datetime.now().timetuple()))}
                    resp = []
                    resp.append(self.loop.run_until_complete(wrapper_post(model_tag_dict[i][2], new_connection_obj)))
                    # for _ in resp[0].rows:
                    #     pass
                elif not model_tag_dict[i][2]:
                    # pass
                    # self.cascade_func(local_model, request.data['EventData'],
                    #                                        'event_id',
                    #                                        wrapper_delete)
                    request_item['event_id'] = None
                    self.loop.run_until_complete(wrapper_post(local_model, request_item))

                # for _ in obj_list_on_delete:
                #     pass
                resp = []
                request_team_item_where = WhereConstructor()
                if not model_tag_dict[i][2]:
                    obj_list_select = self.cascade_func(ParticipantsAPIView.model, request_item, 'team_id',
                                                        wrapper_select, filter_value=True)
                    print("--------------------obj_list_select", obj_list_select)
                    for j in obj_list_select:
                        j['event_id'] = request.data['EventData']['id']
                        j['team_id'] = request_item['id']
                        j['forSorted'] = int(time.mktime(datetime.datetime.now().timetuple()))
                        for k in j.keys():
                            if isinstance(j[k], bytes):
                                j[k] = j[k].decode('utf-8')
                        print("--------------------obj_list_select.j", j)
                        self.loop.run_until_complete(wrapper_post(ParticipantsAPIView.model, j))
                    for j in request_item.keys():
                        if isinstance(request_item[j], bytes):
                            request_item[j] = request_item[j].decode('utf-8')

                    request_team_item_where.append('id', '==', request_item['id'], 'and')
                    request_team_item = []
                    request_team_item.append(self.loop.run_until_complete(wrapper_select(TeamsAPIView.model, request_item, where_settings=request_team_item_where)))
                    request_team_item_where.append('id', '==', request_item['id'], 'and')
                    # print('request_team_item ---', request_team_item)
                    # print('request_team_item[0] ---', request_team_item[0])
                    # print('request_team_item[0].rows ---', request_team_item[0].rows, type(request_team_item[0].rows))
                    # print('request_team_item[0].rows[0] ---', request_team_item[0].rows[0], type(request_team_item[0].rows[0]))
                    for o in request_team_item:
                        print('llllllllllllllllllllllllllllllllllllllllllllllllllllllll', o, o[0].rows)
                        for u in o[0].rows:
                            print()
                            print('u', u)
                            print()
                            request_team_item = u
                            print('-=--------------------=================------', request_team_item)
                            # request_team_item = dict(u)
                    for j in request_team_item.keys():
                        if isinstance(request_team_item[j], bytes):
                            request_team_item[j] = request_team_item[j].decode('utf-8')
                    request_team_item['forSorted'] = int(time.mktime(datetime.datetime.now().timetuple()))
                    request_team_item["event_id"] = request.data['EventData']['id']
                    self.loop.run_until_complete(wrapper_post(local_model, request_team_item))
                    # for j in resp:
                    #     print('j', j)
                    #     for item in j[0].rows:
                    #         print('j[0].rows.item', item, i)
                    #         print('j[0].rows.item', item, i, model_tag_dict[i], model_tag_dict[i][1])
                    #         model_tag_dict[i][1].append(item)
                    # continue
                if not model_tag_dict[i][2]:
                    resp.append(self.loop.run_until_complete(wrapper_select(local_model, request_item, where_settings=request_team_item_where)))
                else:
                    where_construct_finally_select = WhereConstructor()
                    where_construct_finally_select.append('id', '==', request_item['id'], 'or')
                    resp.append(self.loop.run_until_complete(wrapper_select(local_model, request_item, where_settings=where_construct_finally_select)))
                for j in resp:
                    print('j', j)
                    for item in j[0].rows:
                        print('j[0].rows.item', item, i)
                        print('j[0].rows.item', item, i, model_tag_dict[i], model_tag_dict[i][1])
                        model_tag_dict[i][1].append(item)

        answer_dict["EventData"] = list_event_data
        for i in model_tag_dict.keys():
            print("answer_dict", answer_dict)
            answer_dict[i] = model_tag_dict[i][1]

        return Response(answer_dict)

    # def cascade_delete(self, local_model, request_item):
    #     list_obj_on_delete = []
    #     obj_id_list_where_constr = ['id']
    #     obj_on_delete_list_where_constr = WhereConstructor()
    #     obj_on_delete_list_where_constr.append('event_id', '==', request_item['id'])
    #     obj_id_on_delete_list = self.loop.run_until_complete(wrapper_select(local_model, request_item,
    #                                                                           *obj_id_list_where_constr,
    #                                                                           where_settings=obj_on_delete_list_where_constr))
    #     obj_on_delete_list = []
    #     for item in obj_id_on_delete_list[0].rows:
    #         obj_on_delete_list.append(item)
    #     for item in obj_on_delete_list:
    #         resp = self.loop.run_until_complete(wrapper_delete(local_model, item))
    #         list_obj_on_delete = []
    #         for itm in resp[0].rows:
    #             list_obj_on_delete.append(itm)
    #     return list_obj_on_delete

    def delete(self, request):
        token_auth = None
        if "HTTP_AUTHORIZATION" in request.META:
            token_auth = request.META['HTTP_AUTHORIZATION'].split(' ')[-1]
            try:
                token_auth = token_check(token_auth)
            except:
                return Response({"status": 'user is not authorized'})
        else:
            return Response({"status": 'user is not authorized'})
        list_events = []
        list_teams_on_delete = []
        list_participants_on_delete = []
        list_materials_on_delete = []
        for request_item in [{'id': i} for i in request.GET['id'].split(', ')]:
            print('request_item', request_item)
            request_item['id'] = request_item['id'].encode('utf-8')
            resp = self.loop.run_until_complete(wrapper_delete(self.model, request_item))
            request_item['id'] = request_item['id'].decode('utf-8')
            list_events = []
            for item in resp[0].rows:
                list_events.append(item)

            list_teams_on_delete = self.cascade_func(TeamsAPIView.model, request_item, 'event_id', wrapper_delete)
            list_participants_on_delete = self.cascade_func(ParticipantsAPIView.model, request_item, 'event_id',
                                                            wrapper_delete)
            list_materials_on_delete = self.cascade_func(EventMaterialAPIView.model, request_item, 'event_id',
                                                         wrapper_delete)
            list_sponsors_on_delete = self.cascade_func(EventSponsorAPIView.model, request_item, 'event_id',
                                                        wrapper_delete)
            list_organizers_on_delete = self.cascade_func(EventOrganizerAPIView.model, request_item, 'event_id',
                                                          wrapper_delete)

        return Response({"EventData": list_events,
                         "TeamData": list_teams_on_delete,
                         "ParticipantData": list_participants_on_delete,
                         "MaterialData": list_materials_on_delete,
                         'token': token_auth})


class UsersAPIView(ObjAPIView):
    model = Users

    def post(self, request):
        token_auth = None
        if "HTTP_AUTHORIZATION" in request.META:
            token_auth = request.META['HTTP_AUTHORIZATION'].split(' ')[-1]
            try:
                token_auth = token_check(token_auth)
            except:
                return Response({"status": 'user is not authorized'})
        else:
            return Response({"status": 'user is not authorized'})
        list_participants = []
        print('Items', type(request.data['Items']))
        for request_item in request.data['Items']:
            check_login_where_constr = WhereConstructor()
            check_login_where_constr.append('login', "==", request_item['login'])
            list_identical_login = self.loop.run_until_complete(
                wrapper_select(self.model, request_item, where_settings=check_login_where_constr))

            if len(list_identical_login[0].rows) > 0:
                return Response({"status": "this login already exists", 'token': token_auth})
            request_item['id'] = str(uuid.uuid4())
            request_item['forSorted'] = int(time.mktime(datetime.datetime.now().timetuple()))
            resp = []
            resp.append(self.loop.run_until_complete(wrapper_post(self.model, request_item)))
            for i in resp:
                for item in i[0].rows:
                    list_participants.append(item)
        # return Response({"Items": list_participants, 'token': token_auth})
        return Response({'token': token_auth})

    def delete(self, request):
        token_auth = None
        if "HTTP_AUTHORIZATION" in request.META:
            token_auth = request.META['HTTP_AUTHORIZATION'].split(' ')[-1]
            try:
                token_auth = token_check(token_auth)
            except:
                return Response({"status": 'user is not authorized'})
        else:
            return Response({"status": 'user is not authorized'})
        list_participants = []
        login = jwt.decode(token_auth, os.environ.get("TOKEN_WORD"), algorithms=["HS256"])['login']
        check_id_on_login_where_constr = WhereConstructor()
        check_id_on_login_where_constr.append('login', '==', login)
        protected_id = self.loop.run_until_complete(wrapper_select(self.model, request, 'id', where_settings=check_id_on_login_where_constr))

        if len(protected_id)>0:
            protected_id_value = [o for o in protected_id[0].rows][0]['id'].decode('utf-8')
        else:
            protected_id_value = False
        print('Items', type(request.GET['id'].split(', ')))
        for request_item in [{'id': i} for i in request.GET['id'].split(', ')]:
            if protected_id_value:
                if request_item['id'] == protected_id_value:
                    continue
            request_item['id'] = request_item['id'].encode('utf-8')
            resp = self.loop.run_until_complete(wrapper_delete(self.model, request_item))
            request_item['id'] = request_item['id'].decode('utf-8')
            list_participants = []
            for item in resp[0].rows:
                list_participants.append(item)
        if len(list_participants) != 0 and len(request.GET['id'].split(', ')):
            # return Response({"Items": list_participants, "token": token_auth})
            return Response({"token": token_auth})
        return Response({'status': 'deletion error', 'token': token_auth})

class EventMaterialAPIView(ObjAPIView):
    model = EventMaterial


class EventOrganizerAPIView(ObjAPIView):
    model = EventOrganizer


class EventSponsorAPIView(ObjAPIView):
    model = EventSponsor


class EventsOnMainListAPIView(WrapperClass):
    model = Events

    def get(self, request):
        args = ['name', 'statusNow', 'minNumberOfParticipants', 'maxNumberOfParticipants', 'description', 'imageDef', 'imageHor', 'imageVer', 'id']
        event_data = self.loop.run_until_complete(
            wrapper_select(self.model, request))
        list_event_data = []
        for item in event_data[0].rows:
            for j in item.keys():
                if isinstance(item[j], bytes):
                    item[j] = item[j].decode('utf-8')
            item = self.statusNow(item)
            if "basic" in request.GET.keys():
                print(f'item == {item}, "basic", statusNow == {item["statusNow"]}')
                if item['statusNow'] != "Соревнование закрыто" and item['status'] == '2':
                    item_dict = {}
                    for i in args:
                        item_dict[i] = item[i]
                    list_event_data.append(item_dict)
            else:
                print(f'item == {item}, "NO BASIC", statusNow == {item["statusNow"]}')
                if item['statusNow'] == "Соревнование закрыто" and item['status'] == '2':
                    item_dict = {}
                    for i in args:
                        item_dict[i] = item[i]
                    list_event_data.append(item_dict)
        answer_dict = {}
        len_of_obj = len(list_event_data)
        if 'onList' in request.GET.keys():
            count_elem_on_list = 10
            number_of_list = int(request.GET['onList']) - 1
            mn = count_elem_on_list * number_of_list
            mx = count_elem_on_list * (number_of_list + 1) if count_elem_on_list * (
                    number_of_list + 1) < len_of_obj else len_of_obj
            print(mn, mx, list_event_data[mn:mx])
            answer_dict['Items'] = list_event_data[mn:mx]
        else:
            answer_dict['Items'] = list_event_data

        answer_dict["CountList"] = len_of_obj
        return Response(answer_dict)

class EventInfoAllAPIView(WrapperClass):
    model = Events

    def get(self, request):
        args = []
        where_constr = None
        if 'id' in request.GET.keys():
            where_constr = WhereConstructor()
            print('id')
            for item in request.GET['id'].split(', '):
                print(item)
                # where_constr.append(item['parameter'], item['operator'], item['meaning'], item['connection'])
                where_constr.append("id", "==", item, "or")
            event_data = self.loop.run_until_complete(
                wrapper_select(self.model, request, *args, where_settings=where_constr))
            # print(request.data.keys(), request.data.values(), 'Columns' in request.data.keys())
            # ans = self.loop.run_until_complete(wrapper_select(self.model, request))
            list_event_data = []

            for item in event_data[0].rows:
                for j in item.keys():
                    if isinstance(item[j], bytes):
                        item[j] = item[j].decode('utf-8')
                item = self.statusNow(item)
                if item['status'] != '2':
                    return Response({'EventData': []})
                list_event_data.append(item)
                sponsors_list = self.filterSPORMA(request, SponsorsAPIView.model, EventSponsorAPIView.model,
                                                  'sponsor_id',
                                                  "event_id")

                organizers_list = self.filterSPORMA(request, OrganizersAPIView.model, EventOrganizerAPIView.model,
                                                    'organizer_id', "event_id")
                if item['statusMaterials']:
                    materials_list = self.filterSPORMA(request, MaterialsAPIView.model, EventMaterialAPIView.model,
                                                   'material_id', "event_id")
                else:
                    materials_list = []
                if 'regulations' in item.keys():
                    del item['regulations']
                return Response({
                                    "EventData": list_event_data,
                                    "SponsorData": sponsors_list,
                                    "OrganizerData": organizers_list,
                                    "MaterialData": materials_list
                                 })
        else:
            return Response({
                "EventData": []
            })
class EventInfoRegulationsAPIView(WrapperClass):
    model = Events

    def get(self, request):
        args = []
        if 'id' in request.GET.keys():
            where_constr = WhereConstructor()
            print('id')
            for item in request.GET['id'].split(', '):
                print(item)
                where_constr.append("id", "==", item, "or")
            event_data = self.loop.run_until_complete(
                wrapper_select(self.model, request, *args, where_settings=where_constr))
            list_event_data = []

            for item in event_data[0].rows:
                for j in item.keys():
                    if isinstance(item[j], bytes):
                        item[j] = item[j].decode('utf-8')
                item = self.statusNow(item)
                if item['status'] != '2':
                    return Response({'EventData': []})
                if 'regulations' in item.keys():
                    list_event_data.append({'name': item['name'], 'regulations': item['regulations']})

                return Response({
                                    "EventData": list_event_data
                                 })
        else:
            return Response({
                "EventData": []
            })


class EventCheckRegistrationAPIView(WrapperClass):
    model = Events

    def get(self, request):
        args = []
        if 'id' in request.GET.keys():
            where_constr = WhereConstructor()
            print('id')
            for item in request.GET['id'].split(', '):
                print(item)
                where_constr.append("id", "==", item, "or")
            event_data = self.loop.run_until_complete(
                wrapper_select(self.model, request, *args, where_settings=where_constr))
            list_event_data = []

            for item in event_data[0].rows:
                for j in item.keys():
                    if isinstance(item[j], bytes):
                        item[j] = item[j].decode('utf-8')
                item = self.statusNow(item)
                if item['status'] != '2' or item['statusNow'] != "Регистрация открыта":
                    return Response({'EventData': []})
                answer_dict = {}
                if 'minNumberOfParticipants' in item.keys():
                    # list_event_data.append({'minNumberOfParticipants': item['minNumberOfParticipants']})
                    answer_dict['minNumberOfParticipants'] = item['minNumberOfParticipants']
                else:
                    return Response({
                        "EventData": []
                    })
                if 'maxNumberOfParticipants' in item.keys():
                    # list_event_data.append({'maxNumberOfParticipants': item['maxNumberOfParticipants']})
                    answer_dict['maxNumberOfParticipants'] = item['maxNumberOfParticipants']
                else:
                    return Response({
                        "EventData": []
                    })
                if 'maxNumberOfTeam' in item.keys():
                    # list_event_data.append({'maxNumberOfTeam': item['maxNumberOfTeam']})
                    answer_dict['maxNumberOfTeam'] = item['maxNumberOfTeam']
                else:
                    return Response({
                        "EventData": []
                    })

                return Response({
                                    "EventData": [answer_dict]
                                 })
        else:
            return Response({
                "EventData": []
            })

class TeamRegistrationAPIView(WrapperClass):
    model = Teams

    def post(self, request):
        where_constr = WhereConstructor()
        print('id')
        where_constr.append("id", "==", request.data["TeamData"]['event_id'], "or")
        event_data = self.loop.run_until_complete(
            wrapper_select(EventsAPIView.model, request, where_settings=where_constr))

        where_construct = WhereConstructor()
        print('id')
        where_construct.append("event_id", "==", request.data["TeamData"]['event_id'], "or")
        event_limit_data = self.loop.run_until_complete(
            wrapper_select(TeamsAPIView.model, request, where_settings=where_construct))

        for item in event_data[0].rows:
            for j in item.keys():
                if isinstance(item[j], bytes):
                    item[j] = item[j].decode('utf-8')
            item = self.statusNow(item)
            print("item", item)
            if item['status'] != '2' or item['statusNow'] != "Регистрация открыта":
                return Response({'EventData': []})
            elif len([item for item in event_limit_data[0].rows]) >= int(item['maxNumberOfTeam']):
                return Response({"EventData": ['maxNumberOfTeam limit']})
            else:
                list_team_data = []
                request.data['TeamData']['id'] = str(uuid.uuid4())
                request.data['TeamData']['forSorted'] = int(time.mktime(datetime.datetime.now().timetuple()))
                resp = []
                # print("request.data['TeamData']", request.data['TeamData'])
                resp.append(self.loop.run_until_complete(wrapper_post(self.model, request.data['TeamData'])))
                for i in resp:
                    for item in i[0].rows:
                        list_team_data.append(item)

                try:
                    list_participants = []
                    # print('TeamListParticipantsData', type(request.data['TeamListParticipantsData']))
                    for request_item in request.data['TeamListParticipantsData']:
                        request_item['id'] = str(uuid.uuid4())
                        request_item['forSorted'] = int(time.mktime(datetime.datetime.now().timetuple()))
                        request_item['team_id'] = request.data['TeamData']['id']
                        if 'event_id' in request.data['TeamData']:
                            # print('==================', type(request.data['TeamData']['event_id']), len(request.data['TeamData']['event_id']), request.data['TeamData']['event_id'], type(''), request.data['TeamData']['event_id'] != "")
                            request_item['event_id'] = request.data['TeamData']['event_id']
                        else:
                            request_item['event_id'] = None

                        resp = []
                        resp.append(self.loop.run_until_complete(wrapper_post(ParticipantsAPIView.model, request_item)))
                        for i in resp:
                            for item in i[0].rows:
                                list_participants.append(item)
                except:
                    resp = self.loop.run_until_complete(wrapper_delete(self.model, request.data['TeamData']))
                    list_participants = []
                    for item in resp[0].rows:
                        list_participants.append(item)
                    return Response({"TeamData": "ERROR", "TeamListParticipantsData": "ERROR"})
                try:
                    if "event_id" in request.data['TeamData']:
                        where_constr_for_email = WhereConstructor()
                        where_constr_for_email.append('id', '==', request.data['TeamData']['event_id'])
                        # print("where_constr_for_email", where_constr_for_email)
                        event_name_select = self.loop.run_until_complete(wrapper_select(EventsAPIView.model, request, 'name', where_settings=where_constr_for_email))
                        # print(event_name_select)
                        event = []
                        for item in event_name_select[0].rows:
                            event.append(item)
                        # print(event[0]['name'].decode('utf-8'))
                        if len(event) > 0:
                            event = event[0]['name'].decode('utf-8')
                            text = "принята."
                            print('------', [i['emailAdress'].decode('utf-8') for i in list_participants])
                            try:
                                send_mail("LIDcode event status", f"Ваша заявка регистрации на соревнование '{event}' "
                                                                  f"{text}",
                                          settings.EMAIL_HOST_USER, [i['emailAdress'].decode('utf-8') for i in list_participants])
                            except SMTPDataError as e:
                                print('There was an error sending an email: ', e)

                except:
                    pass
                return Response({"TeamData": list_team_data, "TeamListParticipantsData": list_participants})

class UserLoginAPIView(ObjAPIView):
    model = Users

    def get(self, request):
        if "HTTP_AUTHORIZATION" in request.META:
            token_auth = request.META['HTTP_AUTHORIZATION'].split(' ')[-1]
            try:
                token_auth = token_check(token_auth)
                return Response({'token': token_auth})
            except:
                return Response({"status": 'user is not authorized'})
        return Response({"status": 'user is not authorized'})
    def post(self, request):
        login = request.data['login']
        password = request.data['password']
        where_login = WhereConstructor()
        where_login.append(parameter='login', operator='==', meaning=login)
        req = self.loop.run_until_complete(wrapper_select(self.model, request, 'password', "access", where_settings=where_login))
        for i in req[0].rows:
            print('pass', password, i['password'])
            if password != i['password'].decode('utf-8'):
                return Response({"status": 'password is incorrect'})
            else:
                vr = int(time.mktime(datetime.datetime.now().timetuple())) + 3 * 60 * 60
                token_auth = jwt.encode({"login": login, "exp": vr, "access": i["access"].decode('utf-8')}, os.environ.get("TOKEN_WORD"), algorithm="HS256")
                return Response({'token': token_auth})
        return Response({'status': "login is incorrect"})