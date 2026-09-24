class SearchState:
    'Класс - состояние поиска одного пользователя'

    def __init__(self):
        self.candidates = []
        self.current_index = 0


# Состояния всех пользователей бота: {user_id: SearchState()}
search_states = {}
