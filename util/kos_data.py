import time
import datetime
import traceback
import shelve
import settings
from typing import TypedDict


class UserData(TypedDict):
    reason: str
    adder: str
    expire: int
    cancelled: bool


async def add_kos(user: str, adder: int, reason: str = settings.LANGUAGE.NO_REASON_PROVIDED, expire: int = None) -> str:
    result: str = ""
    try:
        with shelve.open('kos_data') as data:
            user_data: UserData = data.get(user)

            # Checks did the user got KOS record before
            if user_data:
                # Put the original reason into a variable
                original_reason = user_data["reason"]
                original_adder = user_data["adder"]
                original_expire = user_data["expire"]
                cancelled = user_data["cancelled"]

                # Checks is the KOS expired
                expire_is_none = user_data["expire"] is None
                if not expire_is_none:
                    expired = time.time() > original_expire
                    date = datetime.datetime.fromtimestamp(original_expire)
                else:
                    expired = False

                # Get the expired message
                if expired:
                    expired_message: str = settings.LANGUAGE.ALREADY_EXPIRED_MSG.format(
                        date.strftime(settings.LANGUAGE.TIME_FORMAT))
                elif cancelled:
                    expired_message: str = settings.LANGUAGE.CANCELLED
                elif expire_is_none:
                    expired_message: str = settings.LANGUAGE.NEVER_EXPIRE
                else:
                    expired_message: str = settings.LANGUAGE.ORIGINAL_EXPIRE_MSG.format(
                        date=date.strftime(settings.LANGUAGE.TIME_FORMAT)
                    )

                # Check is the original adder the same adder
                if user_data["adder"] == adder:
                    result = settings.LANGUAGE.ADDED_TO_KOS_BEFORE_BY_SAME_USER_MSG.format(
                        original_reason=original_reason,
                        expired_message=expired_message
                    )
                else:
                    result = settings.LANGUAGE.ADDED_TO_KOS_BEFORE_BY_ANOTHER_USER_MSG.format(
                        original_adder=original_adder,
                        original_reason=original_reason,
                        expired_message=expired_message
                    )

            # Save the user data
            data[user]: UserData = {
                "adder": adder,
                "reason": reason,
                "expire": expire,
                "cancelled": False
            }

            if not result:
                result = settings.LANGUAGE.ADDED_TO_KOS_MSG

    except Exception as ex: # NO
        result = settings.LANGUAGE.ERROR_MSG
        print(traceback.format_exc())
    return result


async def cancel_kos(user: str):
    result: str = ""
    try:
        with shelve.open('kos_data') as data:
            user_data = data.get(user)
            if user_data is None:
                result = settings.LANGUAGE.KOS_NOT_FOUND_MSG
            elif user_data["cancelled"]:
                result = settings.LANGUAGE.KOS_WAS_CANCELLED_MSG
            else:
                user_data["cancelled"] = True
                data[user] = user_data
                result = settings.LANGUAGE.KOS_CANCELLED_MSG

    except BaseException as e:
        result = settings.LANGUAGE.ERROR_MSG
        print(traceback.format_exc())

    return result


async def get_all_ids() -> list[str]:
    with shelve.open('kos_data') as data:
        dict_data = dict(data)

    return dict_data
