import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from settings import token, group_id
from message_handler import create_message_chat, create_message, load_modules


def main():

    vk_session = vk_api.VkApi(token=token)

    longpoll = VkBotLongPoll(vk_session, group_id)

    while True:
        try:
            for event in longpoll.listen():
                prefix = event.obj.message['text'][0]
                if event.type == VkBotEventType.MESSAGE_NEW and len(event.obj.message['text']) > 0 and prefix in ('/', '!'):
                    if event.from_chat:
                        print(event.obj.message['text'], flush=True)
                        create_message_chat(token=token, u=event.obj.message['from_id'], chat=event.obj.message['peer_id']-2000000000, command=event.obj.message['text'], prefix=prefix)
                    elif event.from_user:
                        create_message(token=token, u=event.obj.message['from_id'], command=event.obj.message['text'], prefix=prefix)
        except Exception as e:
            print(e, flush=True)


print('task_test1', flush=True)
load_modules()
main()
