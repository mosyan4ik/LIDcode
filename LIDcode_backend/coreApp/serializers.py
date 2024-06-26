import io

from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

# import businessLogic
# import models
from .models import *
# from .businessLogic import get_max_table_id, create_table_item, get_data_table, update_table_item


class ParticipantsSerializers(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=200)
    emailAdress = serializers.EmailField()
    phoneNumbers = serializers.CharField(max_length=11)  # Номер с "8" - "89998887766"
    organization = serializers.CharField(max_length=300)
    universityFaculty = serializers.CharField(max_length=200)
    universityCourse = serializers.CharField(max_length=200)

def encode(model):
    # model = Participants()
    model_sr = ParticipantsSerializers(model)
    # print(model_sr.data, type(model_sr.data), sep='\n')
    json = JSONRenderer().render(model_sr.data)
    return (json)


# encode()

def decode():
    stream = io.BytesIO(b'{"name":"Angelina Jolie","organization":"Content: Angelina Jolie"}')
    data = JSONParser().parse(stream)
    serializer = ParticipantsSerializers(data=data)
    serializer.is_valid()
    print(serializer.validated_data)

    # url = serializers.HyperlinkedIdentityField(
    #     view_name='participant',
    #     lookup_field='slug'
    # )

    # def create(self, validated_data):
    #     return create_table_item(participant, **validated_data)
    #
    # def get(self):
    #     return get_data_table(participant)
    #
    # def update(self, instance, validated_data):
    #     upd_t_i = update_table_item(participant, **validated_data)
    #     return upd_t_i

        # instance.name = validated_data.get('name', instance.name)
        # instance.emailAdress = validated_data.get('emailAdress', instance.emailAdress)
        # instance.phoneNumbers = validated_data.get('phoneNumbers', instance.phoneNumbers)
        # instance.organization = validated_data.get('organization', instance.organization)
        # instance.universityFaculty = validated_data.get('universityFaculty', instance.universityFaculty)
        # instance.universityCourse = validated_data.get('universityCourse', instance.universityCourse)


# ParticipantSerializer = ParticipantSerializers(models.participant_Oleg)
# print(ParticipantSerializer.data)
# print(ParticipantSerializer.get())
# businessLogic.delete_table_item(table=models.participant, id=4)
# ParticipantSerializers.create({'emailAdress': 'testperson@test.ru', 'name': 'TestCreatePerson',
#                                'organization': 'Create', 'phoneNumbers': '89998887766', 'universityCourse': '4',
#                                'universityFaculty': 'IVT'})
