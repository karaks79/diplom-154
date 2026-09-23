from vk_api.longpoll import VkEventType

from app.database import (
    get_favorites_from_db,
    get_user_db_id, 
    save_candidate_in_db, 
    save_favorite_in_db, 
    save_user_in_db
)
from app.search import create_search_params, search_users, show_candidate
from app.state import SearchState, search_states
from app.vk import get_user_info, longpoll, write_msg


if __name__ == "__main__":
    print("Бот запущен. Жду сообщения...")

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                #print(f"Новое сообщение: {event.text}")
                user = get_user_info(event.user_id)

                print(user)

                save_user_in_db(user)

                state = search_states.get(event.user_id)

                if state is None:
                    state = SearchState()
                    search_states[event.user_id] = state

                if event.text.lower() == "начать":
                    print("Начинаем поиск...")

                    params = create_search_params(user)

                    state.candidates = search_users(
                        params,
                        user["id"],
                    )

                    for candidate in state.candidates:
                        try:
                            candidate_info = get_user_info(candidate["id"])
                            candidate["db_id"] = save_candidate_in_db(candidate_info)
                        except Exception:
                            continue

                    state.current_index = 0

                    print("Найдено кандидатов:", len(state.candidates))

                    if state.candidates:
                        show_candidate(
                            state.candidates[state.current_index],
                            event.user_id,
                        )

                elif event.text.lower() == "следующий":
                    state.current_index += 1

                    while state.current_index < len(state.candidates):
                        shown = show_candidate(
                            state.candidates[state.current_index],
                            event.user_id,
                        )

                        # Если фото найдены, прекратить поиск
                        if shown:
                            break

                        state.current_index += 1
                    else:
                        write_msg(
                            event.user_id,
                            "Кандидаты закончились.",
                        )

                elif event.text.lower() == "в избранное":
                    if not state.candidates:
                        write_msg(
                            event.user_id,
                            "Сначала начните поиск.",
                        )
                        continue

                    candidate = state.candidates[state.current_index]

                    if "db_id" not in candidate:
                        write_msg(
                            event.user_id,
                            "Не удалось сохранить этого кандидата.",
                        )
                        continue

                    user_db_id = get_user_db_id(user["id"])

                    save_favorite_in_db(
                        user_db_id,
                        candidate["db_id"],
                    )

                    write_msg(
                        event.user_id,
                        "Кандидат добавлен в избранное.",
                    )

                elif event.text.lower() == "избранное":
                    user_db_id = get_user_db_id(user["id"])

                    favorites = get_favorites_from_db(user_db_id)

                    if not favorites:
                        write_msg(
                            event.user_id,
                            "В избранном пока ничего нет.",
                        )
                        continue

                    message = "Избранные кандидаты:\n\n"

                    for favorite in favorites:
                        vk_id = favorite[0]
                        first_name = favorite[1]
                        last_name = favorite[2]

                        message += (
                            f"{first_name} {last_name}\n"
                            f"https://vk.com/id{vk_id}\n\n"
                        )

                    write_msg(
                        event.user_id,
                        message,
                    )

                print("Кандидаты:", state.candidates) 
                print("Текущий индекс:", state.current_index)

                write_msg(
                    event.user_id,
                    "Я получил информацию о твоём профиле!",
                )

