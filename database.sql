CREATE SCHEMA netology_2026_diplom;
;

-- Пользователи бота
CREATE TABLE netology_2026_diplom.users (
    id SERIAL PRIMARY KEY,
    vk_id BIGINT NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL
)
;

-- Пользователь должен быть уникальным
ALTER TABLE netology_2026_diplom.users
ADD CONSTRAINT users_vk_id_unique UNIQUE (vk_id)
;

-- Кандидаты
CREATE TABLE netology_2026_diplom.candidates(
	id SERIAL PRIMARY KEY,
	vk_id BIGINT NOT NULL,
	first_name VARCHAR(100) NOT NULL,
	last_name VARCHAR(100) NOT NULL,
	age INTEGER NOT NULL,
	sex INTEGER NOT NULL, 
	city_id BIGINT NOT NULL,
	city_name VARCHAR(100) NOT NULL
)
;

-- Уникальность кандидата
ALTER TABLE netology_2026_diplom.candidates
ADD CONSTRAINT candidates_vk_id_unique UNIQUE (vk_id)
;

-- Избранные кандидаты
CREATE TABLE netology_2026_diplom.favorites(
	id SERIAL PRIMARY KEY,
	user_id INTEGER NOT NULL REFERENCES netology_2026_diplom.users(id),
	candidate_id INTEGER NOT NULL REFERENCES netology_2026_diplom.candidates(id)
)
;

-- В избранное можно добавить пользователя только один раз
ALTER TABLE netology_2026_diplom.favorites
ADD CONSTRAINT favorites_user_candidate_unique
UNIQUE (user_id, candidate_id)
;