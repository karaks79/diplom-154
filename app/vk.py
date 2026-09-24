import json
import vk_api

from app.config import VK_APP_TOKEN, VK_GROUP_TOKEN
from vk_api.longpoll import VkLongPoll
from datetime import date, datetime


vk_session = vk_api.VkApi(token=VK_GROUP_TOKEN)
vk = vk_session.get_api()

# longpoll - механизм библиотеки vk_api, который постоянно ждёт новые события сообщества.
longpoll = VkLongPoll(vk_session)

app_session = vk_api.VkApi(token=VK_APP_TOKEN)
app_vk = app_session.get_api()


def get_keyboard():
    '''Создаёт клавиатуру для бота.'''
    keyboard = {
        "one_time": False,
        "buttons": [
            [
                {
                    "action": {
                        "type": "text",
                        "label": "Начать",
                    },
                    "color": "primary",
                },
                {
                    "action": {
                        "type": "text",
                        "label": "Следующий",
                    },
                    "color": "secondary",
                },
            ],
            [
                {
                    "action": {
                        "type": "text",
                        "label": "В избранное",
                    },
                    "color": "positive",
                },
                {
                    "action": {
                        "type": "text",
                        "label": "Избранное",
                    },
                    "color": "secondary",
                },
            ],
        ],
    }

    return json.dumps(
        keyboard,
        ensure_ascii=False,
    )


def write_msg(
    user_id,
    message,
    attachment=None,
    keyboard=None,
):
    vk.messages.send(
        user_id=user_id,
        message=message,
        random_id=0,
        attachment=attachment,
        keyboard=keyboard,
    )


def get_user(user_id: int) -> dict:
    'Получить данные о пользователе'
    users = vk.users.get(
        user_ids=user_id,
        fields="sex,bdate,city",
    )

    return users[0]


def get_user_info(user_id: int) -> dict:
    'Инфо о пользователе'
    user = get_user(user_id)

    bdate = user.get("bdate")
    age = None

    if bdate:
        try:
            birth_date = datetime.strptime(bdate, "%d.%m.%Y").date()

            today = date.today()
            age = today.year - birth_date.year

            if (today.month, today.day) < (
                birth_date.month,
                birth_date.day,
            ):
                age -= 1

        except ValueError:
            pass

    city = user.get("city")
    city_id = city["id"] if city else None
    city_name = city["title"] if city else None

    return {
        "id": user["id"],
        "first_name": user["first_name"],
        "last_name": user["last_name"],
        "age": age,
        "sex": user.get("sex"),
        "city_id": city_id,
        "city_name": city_name,
    }

