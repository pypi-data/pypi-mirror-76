def get_event_type(number):
    if number == 1:
        return 'REPLACE_MESSAGE_FLAGS' # Замена флагов сообщения
    if number == 2:
        return 'SET_MESSAGE_FLAGS' # Установка флагов сообщения
    if number == 3:
        return 'RESET_MESSAGE_FLAGS' # Сброс флагов сообщения
    if number == 4:
        return 'ADD_NEW_MESSAGE' #  Добавление нового сообщения
    if number == 5:
        return 'EDIT_MESSAGE' # Редактирование сообщения
    if number == 6:
        return 'INCOMING_MESSAGE_READ' # Прочтение входящего вообщения
    if number == 7:
        return 'OUTCOMING_MESSAGE_READ' # Прочтение исходящего сообщения
    if number == 8:
        return 'FRIEND_ONLINE' # Друг стал онлайн
    if number == 9:
        return 'FRIEND_OFFLINE' # Друг стал оффлайн
    if number == 10:
        return 'RESET_DIALOG_FLAGS' # Сброс флагов диалога
    if number == 11:
        return 'REPLACE_DIALOG_FLAGS' # Замена флагов диалога
    if number == 12:
        return 'SET_DIALOG_FLAGS' # Установка флагов диалога
    if number == 13:
        return 'DELETE_MESSAGE' # Удаление сообщения
    if number == 14:
        return 'UNDO_DELETE_MESSAGE' # Отмена удаления сообщения
    if number == 20:
        return 'MAJOR_ID_CHANGED' # Изменился major id
    if number == 21:
        return 'MINOR_ID_CHANGED' # Изменился minor id
    if number == 51:
        return 'CONTENT_OR_TOPIC_CHANGED' # Состав или тема изменены
    if number == 52:
        return 'CHANGE_CHAT_INFO' # Изменена информация чата
    if number == 61:
        return 'USER_TYPING_IN_DIALOG' # Пользователь печатает в диалоге
    if number == 62:
        return 'USER_TYPING_IN_CONVERSATION' # Пользователь печатает в беседа
    if number == 63:
        return 'USERS_TYPING_IN_CONVERSATION' # Пользователи печатают в беседе
    if number == 64:
        return 'USERS_AUDIO_RECORDING_IN_CONVERSTION' # Пользователи записывают аудиосообщение в беседе
    if number == 70:
        return 'USER_CALLED' # Пользователь совершил аудиозвонок
    if number == 80:
        return 'COUNTER_CHANGE' # Счетчик изменен
    if number == 114:
        return 'NOTIFY_SETTINGS_CHANGED' # Изменены настройки уведомлений
    return 'NONE_VK_EVENT' # Не явяется событием
