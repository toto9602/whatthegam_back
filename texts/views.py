from django.shortcuts import get_object_or_404
from users.models import CustomUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Text
from .serializers import *
from whatthegam.models import Place
import random

class TextCountAPIView(APIView):

    def get(self, request, map_id):
        place = Place.objects.get(map_id=map_id)
        text_count = Text.objects.filter(written_place=place).count()
        context = {}
        if text_count == 0:
            context['msg'] = '낙서가 없는 장소입니다!'
        else:
            context['msg'] = f'낙서가 {text_count}개 있는 장소입니다!'
        context['text_count'] = text_count
        context['map_id'] = map_id
        context['place'] = place.name
        
        return Response(context, status=status.HTTP_200_OK)


class TextListAPIView(APIView):

    def get(self, request, map_id):
        try:                
            place = Place.objects.get(map_id=map_id)
        except:
            context = {'msg':'첫 번째 낙서를 남겨보세요!!'}
            return Response(context, status=status.HTTP_204_NO_CONTENT)
        texts = Text.objects.filter(written_place=place)
        context = {}
        if texts:
            serializer = TextSerializer(texts, many=True)
            context['data'] = serializer.data
            context['text_count'] = texts.count()
            return Response(context, status=status.HTTP_200_OK)
        else:
            context['text_count'] = texts.count()
            context['data'] = []
            return Response(context, status=status.HTTP_204_NO_CONTENT)

    def post(self, request, map_id):
        place = Place.objects.get(map_id=map_id)
        if place:
            serializer = TextCreateSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(author=request.user,
                                written_place=place,
                                spin_rate=round(random.uniform(0, 360), 2),
                                x_axis=round(random.uniform(0,100), 2),
                                y_axis=round(random.uniform(0,100), 2))

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    

class TextDetailAPIView(APIView):


    def put(self, request, map_id, text_pk):
        place = Place.objects.get(map_id=map_id)
        text = get_object_or_404(Text, id=text_pk)

        serializer = TextCreateSerializer(text, data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def delete(self, request, map_id, text_pk):
        text = Text.objects.get(id=text_pk)
        text.delete()
        msg = {'msg':"낙서가 지워졌습니다!"}
        return Response(msg, status=status.HTTP_204_NO_CONTENT)





# def put(self, request, map_id, text_pk):
#         print(request.user)
#         place = Place.objects.get(map_id=map_id)
#         text = get_object_or_404(Text, id=text_pk)
#         if (request.data['is_private'] and request.data['users_opened']):
#             print("debug#0")
#             users = []
#             print(request.data['users_opened'])
#             for user in request.data['users_opened']:
#                 print(CustomUser.objects.get(username=user))
#                 users.append(CustomUser.objects.get(username=user).id)
#             print(users)
#         print("debug#1")
#         # request.data.pop('users_opened')
#         # request.data['users_opened'] = users
#         request.data['author'] = request.user
#         print(request.data)
#         request.data['users_opened'] = users
#         serializer = TextCreateSerializer(text, data=request.data)
#         print(serializer.is_valid())
#         print(serializer.errors)
#         if serializer.is_valid():
#             serializer.save()
#             print(serializer.data)
#             serializer.data['author_year'] = request.user.year
#             print(serializer.data)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)