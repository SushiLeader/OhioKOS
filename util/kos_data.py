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


async def add_kos(user: str, adder: int, reason: str = "沒有提供原因", expire: int = None) -> str:
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
                print(f"Cancelled: {cancelled}")
                # Checks is the KOS expired
                expire_is_none = user_data["expire"] is None
                if not expire_is_none:
                    expired = time.time() > original_expire
                    date = datetime.datetime.fromtimestamp(original_expire)
                else:
                    expired = False

                # Get the expired message
                if expired:
                    expired_message: str = f"已在{date.strftime('%Y年%m月%d日 %H時%M分%S秒')}過期"
                elif cancelled:
                    expired_message: str = "已取消"
                elif expire_is_none:
                    expired_message: str = "永不過期"
                else:
                    expired_message: str = f"原來的過期時間：{date.strftime('%Y年%m月%d日 %H時%M分%S秒')}"

                # Check is the original adder the same adder
                if user_data["adder"] == adder:
                    result = f"你之前新增過這個用戶進KOS，原因和過期時間已經更新\n原本的原因：{original_reason}\n{expired_message}"
                else:
                    result = f"之前<@{original_adder}>新增過這個用戶進KOS\n原本的原因：「{original_reason}」\n{expired_message}"

            # Save the user data
            data[user]: UserData = {
                "adder": adder,
                "reason": reason,
                "expire": expire,
                "cancelled": False
            }

            if not result:
                result = "成功新增了KOS"''

    except BaseException as e:
        result = f"報錯了 <@{settings.AUTHOR}>"
        print(traceback.format_exc())
    return result


async def cancel_kos(user: str):
    result: str = ""
    try:
        with shelve.open('kos_data') as data:
            user_data = data.get(user)
            if user_data is None:
                result = "沒有這個用戶的KOS記錄"
            elif user_data["cancelled"]:
                result = "這個用戶的KOS之前已被取消"
            else:
                user_data["cancelled"] = True
                data[user] = user_data
                result = "成功取消這個KOS"

    except BaseException as e:
        result = f"報錯了 <@{settings.AUTHOR}>"
        print(traceback.format_exc())

    return result


async def get_all_ids() -> list[str]:
    with shelve.open('kos_data') as data:
        dict_data = dict(data)

    return dict_data


