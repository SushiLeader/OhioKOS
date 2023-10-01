import settings

NO_REASON_PROVIDED = "No reason was provided"
TIME_FORMAT = '%m-%d-%Y %H:%M:%S'
ERROR_MSG = f"ERROR <@{settings.AUTHOR}>"
CANCELLED = "Cancelled"
NEVER_EXPIRE = "Never expires"

ALREADY_EXPIRED_MSG = "Already expired at {date}"
ORIGINAL_EXPIRE_MSG = "Original expire: {date}"
ADDED_TO_KOS_BEFORE_BY_SAME_USER_MSG = "You have added this user to KOS in the pass, The information have been updated" \
                                       "\nOriginal reason：{original_reason}\n" \
                                       "{expired_message}"
ADDED_TO_KOS_BEFORE_BY_ANOTHER_USER_MSG = "This person was added to KOS by <@{original_adder}> before\n" \
                                          "Original reason: {original_reason}" \
                                          "{expired_message}"
ADDED_TO_KOS_MSG = "Successfully added the user to KOS"

KOS_NOT_FOUND_MSG = "User was not found in KOS"
KOS_WAS_CANCELLED_MSG = "The KOS was cancelled before"
KOS_CANCELLED_MSG = "Successfully cancelled the KOS"

START_SCANNING_SERVER_MSG = "Started scanning the servers (can be inaccurate)"
FOUND_TARGET_MSG = ":warning: KOS was found :warning:\n" \
                   "Username: {username}\n" \
                   "Display name: {display_name}\n" \
                   "Server ID: {serverid}\n" \
                   "User Link: https://www.roblox.com/users/{userid}/profile"
SCAN_FINISHED_MSG = "Scan is finished"

ALREADY_HAVE_ROLE_MSG = "You already have the role"
ROLE_ADDED_MSG = "Role is given to you"
