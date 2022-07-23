from main import BOT_DATA, USER_DATA


def get_bot_data(query: str):
    # sourcery skip: assign-if-exp, reintroduce-else
    if BOT_DATA.find_one() is None:
        return None
    if query not in dict(BOT_DATA.find_one()).keys():  # type: ignore[arg-type]
        return None

    return dict(BOT_DATA.find_one())[query]  # type: ignore[arg-type]


def set_bot_data(query: str, value):
    if query not in dict(BOT_DATA.find_one()).keys():  # type: ignore[arg-type]
        return None

    BOT_DATA.find_one_and_update({}, {"$set": {query: value}})
    return True


def get_user_data(user_id: int, query: str = None):
    if not USER_DATA.find_one({"_id": user_id}):
        return None
    return (
        dict(USER_DATA.find_one({"_id": user_id})).get(query, None) if query else True
    )


def set_user_data(user_id: int, query: str, value):
    if not get_user_data(user_id):
        return None

    USER_DATA.find_one_and_update({"_id": user_id}, {"$set": {query: value}})
    return True


def unset_user_data(user_id: int, query: str):
    if not get_user_data(user_id, query):
        return None

    USER_DATA.find_one_and_update({"_id": user_id}, {"$unset": {query: ""}})
    return True
