import const


def create_stat_info():
    # 'Hey %s, there is a 0x%x error!' % (name, errno)
    all_count = len(const.user_set)
    active_count = all_count - const.BLOCK_COUNT
    active_today = get_active_users()

    stat_info = "Всего пользователей в боте %d \n" \
                "Активных пользователей в боте %d \n" \
                "Активных пользователей за сегодня %d \n" \
                "Бота заблокировали %d \n"\
                % (all_count, active_count, active_today, const.BLOCK_COUNT)
    return stat_info


def get_active_users():
    return len(const.active_users_set)


def check_date(day, id_user):
    if const.LAST_DAY == day:
        const.active_users_set.add(id_user)
    else:
        const.LAST_DAY = day
        const.active_users_set.clear()
