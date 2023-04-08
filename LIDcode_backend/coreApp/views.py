from rest_framework.response import Response
from rest_framework.views import APIView
from .businessLogic import get_data_table, create_table_item, update_table_item, delete_table_item
from .models import participant, event, team, material, organizer, sponsor


class ParticipantAPIView(APIView):

    def get(self, request):
        return Response({'get': get_data_table(participant)})

    def post(self, request):
        post_new = create_table_item(participant,
                                     name=request.data['name'],
                                     emailAdress=request.data['emailAdress'],
                                     phoneNumbers=request.data['phoneNumbers'],
                                     organization=request.data['organization'],
                                     universityFaculty=request.data['universityFaculty'],
                                     universityCourse=request.data['universityCourse']
                                     )
        return Response({'post': post_new})

    def put(self, request):
        put_new = update_table_item(participant,
                                    id=request.data['id'],
                                    name=request.data['name'],
                                    emailAdress=request.data['emailAdress'],
                                    phoneNumbers=request.data['phoneNumbers'],
                                    organization=request.data['organization'],
                                    universityFaculty=request.data['universityFaculty'],
                                    universityCourse=request.data['universityCourse']
                                    )
        return Response({'put': put_new})

    def delete(self, request):
        delete_new = delete_table_item(participant, request.data['id'])
        return Response({'delete': delete_new})


class EventAPIView(APIView):

    def get(self, request):
        return Response({'get': get_data_table(event)})

    def post(self, request):
        post_new = create_table_item(event,
                                     datEnd=request.data['datEnd'],
                                     dateCloseRegister=request.data['dateCloseRegister'],
                                     dateRegister=request.data['dateRegister'],
                                     dateStart=request.data['dateStart'],
                                     description=request.data['description'],
                                     image=request.data['image'],
                                     isHidden=request.data['isHidden'],
                                     name=request.data['name'],
                                     numberOfParticipants=request.data['numberOfParticipants'],
                                     regulations=request.data['regulations'],
                                     results=request.data['results'],
                                     timePublicationAdditionalMaterial=request.data['timePublicationAdditionalMaterial']
                                     )
        return Response({'post': post_new})

    def put(self, request):
        put_new = update_table_item(event,
                                    id=request.data['id'],
                                    datEnd=request.data['datEnd'],
                                    dateCloseRegister=request.data['dateCloseRegister'],
                                    dateRegister=request.data['dateRegister'],
                                    dateStart=request.data['dateStart'],
                                    description=request.data['description'],
                                    image=request.data['image'],
                                    isHidden=request.data['isHidden'],
                                    name=request.data['name'],
                                    numberOfParticipants=request.data['numberOfParticipants'],
                                    regulations=request.data['regulations'],
                                    results=request.data['results'],
                                    timePublicationAdditionalMaterial=request.data['timePublicationAdditionalMaterial']
                                    )
        return Response({'put': put_new})

    def delete(self, request):
        delete_new = delete_table_item(event, request.data['id'])
        return Response({'delete': delete_new})


class TeamAPIView(APIView):

    def get(self, request):
        return Response({'get': get_data_table(team)})

    def post(self, request):
        post_new = create_table_item(team,
                                     CoachFaceId=request.data['CoachFaceId'],
                                     ContactFaceId=request.data['ContactFaceId'],
                                     approvement=request.data['approvement'],
                                     name=request.data['name']
                                    )
        return Response({'post': post_new})

    def put(self, request):
        put_new = update_table_item(team,
                                    id=request.data['id'],
                                    CoachFaceId=request.data['CoachFaceId'],
                                    ContactFaceId=request.data['ContactFaceId'],
                                    approvement=request.data['approvement'],
                                    name=request.data['name'])
        return Response({'put': put_new})

    def delete(self, request):
        delete_new = delete_table_item(team, request.data['id'])
        return Response({'delete': delete_new})

class MaterialAPIView(APIView):

    def get(self, request):
        return Response({'get': get_data_table(material)})

    def post(self, request):
        post_new = create_table_item(material,
                                     link=request.data['link'],
                                     name=request.data['name']
                                    )
        return Response({'post': post_new})

    def put(self, request):
        put_new = update_table_item(material,
                                    id=request.data['id'],
                                    link=request.data['link'],
                                    name=request.data['name']
                                    )
        return Response({'put': put_new})

    def delete(self, request):
        delete_new = delete_table_item(material, request.data['id'])
        return Response({'delete': delete_new})


class OrganizerAPIView(APIView):

    def get(self, request):
        return Response({'get': get_data_table(organizer)})

    def post(self, request):
        post_new = create_table_item(organizer,
                                     link=request.data['link'],
                                     image=request.data['image'],
                                     name=request.data['name']
                                    )
        return Response({'post': post_new})

    def put(self, request):
        put_new = update_table_item(organizer,
                                    id=request.data['id'],
                                    link=request.data['link'],
                                    image=request.data['image'],
                                    name=request.data['name']
                                    )
        return Response({'put': put_new})

    def delete(self, request):
        delete_new = delete_table_item(organizer, request.data['id'])
        return Response({'delete': delete_new})


class SponsorAPIView(APIView):

    def get(self, request):
        return Response({'get': get_data_table(sponsor)})

    def post(self, request):
        post_new = create_table_item(sponsor,
                                     link=request.data['link'],
                                     image=request.data['image'],
                                     name=request.data['name']
                                    )
        return Response({'post': post_new})

    def put(self, request):
        put_new = update_table_item(sponsor,
                                    id=request.data['id'],
                                    link=request.data['link'],
                                    image=request.data['image'],
                                    name=request.data['name']
                                    )
        return Response({'put': put_new})

    def delete(self, request):
        delete_new = delete_table_item(sponsor, request.data['id'])
        return Response({'delete': delete_new})


# class UserViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows users to be viewed or edited.
#     """
#     queryset = User.objects.all().order_by('-date_joined')
#     serializer_class = ParticipantSerializers
#     permission_classes = [permissions.IsAuthenticated]


# class GroupViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows groups to be viewed or edited.
#     """
#     queryset = Group.objects.all()
#     serializer_class = GroupSerializer
#     permission_classes = [permissions.IsAuthenticated]
