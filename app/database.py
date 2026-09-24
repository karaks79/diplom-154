import psycopg2

from app.config import (
    DB_HOST,
    DB_PORT,
    DB_NAME,
    DB_USER,
    DB_PASSWORD,
)


def get_connection():
    ''' Создаёт подключение к PostgreSQL. '''

    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        client_encoding="UTF8",
    )


def save_user_in_db(user: dict) -> int:
    '''
        Сохраняет пользователя VK в таблицу users.
    '''
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO netology_2026_diplom.users (
            vk_id,
            first_name,
            last_name
        )
        VALUES (%s, %s, %s)
        ON CONFLICT (vk_id)
        DO UPDATE SET
            first_name = EXCLUDED.first_name,
            last_name = EXCLUDED.last_name
        RETURNING id
        """,
        (
            user["id"],
            user["first_name"],
            user["last_name"],
        ),
    )

    user_id = cursor.fetchone()[0]

    connection.commit()
    cursor.close()
    connection.close()

    return user_id


def save_candidate_in_db(candidate: dict) -> int:
    '''
    Сохраняет найденного кандидата в таблицу candidates.
    '''
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO netology_2026_diplom.candidates (
            vk_id,
            first_name,
            last_name,
            age,
            sex,
            city_id,
            city_name
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (vk_id)
        DO UPDATE SET
            first_name = EXCLUDED.first_name,
            last_name = EXCLUDED.last_name,
            age = EXCLUDED.age,
            sex = EXCLUDED.sex,
            city_id = EXCLUDED.city_id,
            city_name = EXCLUDED.city_name
        RETURNING id
        """,
        (
            candidate["id"],
            candidate["first_name"],
            candidate["last_name"],
            candidate["age"],
            candidate["sex"],
            candidate["city_id"],
            candidate["city_name"],
        ),
    )

    candidate_id = cursor.fetchone()[0]

    connection.commit()
    cursor.close()
    connection.close()

    return candidate_id


def save_favorite_in_db(user_id: int, candidate_id: int) -> None:
    '''
    Сохраняет кандидата в избранное пользователя.
    '''
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO netology_2026_diplom.favorites (
            user_id,
            candidate_id
        )
        VALUES (%s, %s)
        ON CONFLICT (user_id, candidate_id) DO NOTHING
        """,
        (user_id, candidate_id),
    )

    connection.commit()
    cursor.close()
    connection.close()


def get_user_db_id(vk_id: int) -> int:
    '''
    Возвращает id пользователя из таблицы users.
    '''
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id
        FROM netology_2026_diplom.users
        WHERE vk_id = %s
        """,
        (vk_id,),
    )

    user_id = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    return user_id


def get_favorites_from_db(user_db_id: int) -> list:
    '''
    Возвращает избранных кандидатов пользователя.
    '''
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            candidates.vk_id,
            candidates.first_name,
            candidates.last_name
        FROM netology_2026_diplom.favorites
        JOIN netology_2026_diplom.candidates
            ON favorites.candidate_id = candidates.id
        WHERE favorites.user_id = %s
        ORDER BY favorites.id
        """,
        (user_db_id,),
    )

    favorites = cursor.fetchall()

    cursor.close()
    connection.close()

    return favorites


if __name__ == "__main__":
    connection = get_connection()

    print("Подключение к PostgreSQL успешно!")

    connection.close()
