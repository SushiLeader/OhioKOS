import settings

NO_REASON_PROVIDED = "沒有提供原因"
TIME_FORMAT = '%Y年%m月%d日 %H時%M分%S秒'
ERROR_MSG = f"報錯了 <@{settings.AUTHOR}>"
CANCELLED = "已取消"
NEVER_EXPIRE = "永不過期"

ALREADY_EXPIRED_MSG = "已在{date}過期"
ORIGINAL_EXPIRE_MSG = "原來的過期時間：{date}"
ADDED_TO_KOS_BEFORE_BY_SAME_USER_MSG = "你之前新增過這個用戶進KOS，原因和過期時間已經更新\n原本的原因：{original_reason}\n{expired_message}"
ADDED_TO_KOS_BEFORE_BY_ANOTHER_USER_MSG = "之前<@{original_adder}>新增過這個用戶進KOS\n" \
                                          "原本的原因：「{original_reason}" \
                                          "{expired_message}"
ADDED_TO_KOS_MSG = "成功新增了KOS"


KOS_NOT_FOUND_MSG = "沒有這個用戶的KOS記錄"
KOS_WAS_CANCELLED_MSG = "KOS之前被取消了"
KOS_CANCELLED_MSG = "成功取消這個KOS"

START_SCANNING_SERVER_MSG = "開始掃描服務器 (未必可靠)"
FOUND_TARGET_MSG = ":warning: 發現KOS :warning:\n用戶名: {username}\n顯示名: {display_name}\n服務器: {serverid}\n" \
                   "用戶連結: https://www.roblox.com/users/{userid}/profile"
SCAN_FINISHED_MSG = "掃描結束"


ALREADY_HAVE_ROLE_MSG = "你已經有這個角色了"
ROLE_ADDED_MSG = "成功給你這個角色"
