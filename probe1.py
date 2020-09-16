# import os
#
# from dotenv import load_dotenv
# load_dotenv()
#
# token = os.getenv('token')
# print(token) # 123
# import os
#
# from dotenv import load_dotenv
# load_dotenv()
#
# account_sid = os.getenv("account_sid")
# auth_token = os.getenv("token")
# print(auth_token)
# import requests
# import datetime as dt
# import time
#
# def get_friends(user_id):
#     data = {
#         'access_token': '27bbced3ed453c827a08b9b1005c5d6eec564ee7c9df9d1fbd1da4a4fcf3c43dec648456b9ff5745431a0',
#         'user_id': user_id,
#         'v': '5.92',
#         'fields': 'nickname, domain, sex, bdate, city, country, timezone, photo_50'
#                   ', photo_100, photo_200_orig, has_mobile, contacts, education,'
#                   ' online, relation, last_seen, status, '
#                   'can_write_private_message, '
#                   'can_see_all_posts, can_post, universities'
#     }
#     url = 'https://api.vk.com/method/friends.get'
#     friends_list = requests.post(url, data)
#     return friends_list.json()
# print(get_friends(5159171))
# final_list = get_friends(47127327)['response']
# # print(final_list)
# count = 0
# deleted_list = []
# delete_count = 0
# for friend in final_list['items']:
#     if friend['first_name'] != 'DELETED':
#         if friend['status']:
#             with open('statuses.txt', mode='a') as f:
#                 f.write(f"id={friend['id']} {friend['first_name']} {friend['last_name']}\n"
#                         f"----------------------------------------------------\n"
#                         f"https://vk.com/id{friend['id']}\n"
#                         f"{friend['status']}\n"
#                         f"++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
#             print(friend['id'], friend['first_name'], friend['last_name'])
#             print('='*50)
#             print(friend['status'])
#             # ts = friend['last_seen']['time']
#             # print(f"Последнее посещение: {dt.datetime.fromtimestamp(ts).strftime('%d-%B-%Y %H:%M:%S')}")
#             print('-' * 50)
#             print('+'*50)
#             count += 1
#     # else:
#     #     delete_count += 1
# # print(f'Всего неудаленных страниц: {count}')
# # print(f'Всего удаленных страниц: {delete_count} ')
# print(f'Всего людей со статусом: {count}')
from django.shortcuts import  get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET', 'POST'])
def api_posts(request):
    if request.method == 'GET':
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return JsonResponse(serializer.data)
    elif request.method == 'POST':
        serializer = PostSerializer(request.date, many=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return Response(data={'1': 1}, status=status.HTTP_400_BAD_REQUEST)
