from app.config import MIN_AGE_DELTA, MAX_AGE_DELTA

from app.vk import app_vk, write_msg


def create_search_params(user: dict) -> dict:
    '''
    Параметры поиска пользователей:
        Диапазон возраста: 
            От (ВозрастОбратившегося - MIN_AGE_DELTA) 
            До (ВозрастОбратившегося - MAX_AGE_DELTA).
        Противоположный пол: 1 - Ж, 2 - М
        Тот же город
    '''
    return {
        "age_from": user["age"] - MIN_AGE_DELTA,
        "age_to": user["age"] - MAX_AGE_DELTA,
        "sex": 3 - user["sex"], 
        "city_id": user["city_id"],           
        "city_name": user["city_name"],
    }


def search_users(params: dict, user_exception_id: int) -> list:
    '''
    Ищет пользователей VK по заданным параметрам.
    '''
    result = app_vk.users.search(
        age_from=params["age_from"],
        age_to=params["age_to"],
        sex=params["sex"],
        city=params["city_id"],
        has_photo=1,
        count=20,
    )

    return [
        person  
        for person in result["items"] 
        if person["id"] != user_exception_id       # Исключая самого ищущего
    ]


def get_top_photos(user_id: int) -> list:
    '''
    Возвращает 3 самые популярные фотографии пользователя.
    '''
    try:
        result = app_vk.photos.get(
            owner_id=user_id,
            album_id="profile",
            extended=1,
            count=100,
        )
    except Exception:
        return []

    photos = result["items"]

    # print("Всего фотографий:", len(photos))

    photos.sort(
        key=lambda photo: photo["likes"]["count"],
        reverse=True,
    )

    return photos[:3]


def create_photo_attachment(photo: dict) -> str:
    '''
    Создаёт attachment для фотографии VK.
    '''
    return f'photo{photo["owner_id"]}_{photo["id"]}'


def show_candidate(candidate: dict, user_id: int) -> None:
    '''
    Показывает кандидата пользователю бота.
    '''
    message = (
        f'{candidate["first_name"]} {candidate["last_name"]}\n'
        f'https://vk.com/id{candidate["id"]}'
    )

    photos = get_top_photos(candidate["id"])

    # Если нет фото (закрытый профиль)
    if not photos:
        return False

    attachments = [
        create_photo_attachment(photo)
        for photo in photos
    ]

    attachment = ",".join(attachments)

    write_msg(
        user_id,
        message,
        attachment,
    )

    return True


if __name__ == "__main__":
    from app.vk import get_user_info

    user = get_user_info(871061919)

    print("Данные пользователя:")
    print(user)

    params = create_search_params(user)

    # print("\nПараметры поиска:")
    # print(params)

    results = search_users(params, user["id"])

    print("\nНайдено пользователей:", len(results))

    if results:
        show_candidate(
            results[0],
            user["id"],
        )

    # for person in results:
    #     print(
    #         person["id"],
    #         person["first_name"],
    #         person["last_name"],
    #     )

    # if results:
    #     first_person = results[2]

    #     photos = get_top_photos(first_person["id"])

    #     print("\nТоп-3 фотографии:")
        
    #     for photo in photos:
    #         attachment = create_photo_attachment(photo)

    #         print(
    #             "ID:",
    #             photo["id"],
    #             "Лайков:",
    #             photo["likes"]["count"],
    #             "Attachment:",
    #             attachment,
    #         )

    #         write_msg(
    #             user["id"],
    #             "Проверяем отправку фотографии:",
    #             attachment,
    #         )

    #         break