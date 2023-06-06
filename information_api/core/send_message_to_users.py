from background_task import background
import requests
from time import sleep
@background(schedule=0)  # Specify the scheduling interval for the job
def send_message_to_users(user_ids, message_text):
    # print("reached")
    bot_token = '6141215482:AAHXl1LNtFuuKbY0fml-vX3Uyk3cqfq5VoE'
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    print(user_ids)
    for user_id in user_ids:
        params = {
            'chat_id': user_id,
            'text': message_text
        }
        response = requests.post(url, json=params)
        print(response)
        if response.status_code == 200:
            print(f'Message sent to {user_id} successfully.')
        else:
            print(f'Failed to send the message to {user_id}.')
        sleep(0.1)
    print('Message sending process completed.')
