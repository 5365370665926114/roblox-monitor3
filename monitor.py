import requests
from datetime import datetime

# C ONFIGURAÇÕES
roblox_user_id = 1095627406  # Substitua pelo ID do jogador
webhook_url = 'https://discord.com/api/webhooks/1393626937070456842/eRm7z8Rucy_YBDeIbE0SpGf6jY8TdNjEuTlUbbyBREW0K0wtvM5X4KHLARdZfLEL3GtE'  # Cole aqui seu webhook
state_file = 'last_status.txt'

def is_user_online(user_id):
    url = f"https://api.roblox.com/users/{user_id}/onlinestatus/"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('IsOnline', False)
    return False

def get_username(user_id):
    response = requests.get(f"https://users.roblox.com/v1/users/{user_id}")
    if response.status_code == 200:
        return response.json().get("name", "Desconhecido")
    return "Desconhecido"

def send_webhook(username, time_str):
    data = {
        "content": None,
        "embeds": [
            {
                "title": f"{username} entrou no Roblox!",
                "description": f"🟢 O jogador **{username}** ficou online às `{time_str}`.",
                "color": 65280
            }
        ]
    }
    requests.post(webhook_url, json=data)

def main():
    username = get_username(roblox_user_id)
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    online = is_user_online(roblox_user_id)

    try:
        with open(state_file, 'r') as f:
            last_status = f.read().strip()
    except FileNotFoundError:
        last_status = 'offline'

    if online and last_status == 'offline':
        send_webhook(username, now)
        with open(state_file, 'w') as f:
            f.write('online')
    elif not online:
        with open(state_file, 'w') as f:
            f.write('offline')

if __name__ == "__main__":
    main()
