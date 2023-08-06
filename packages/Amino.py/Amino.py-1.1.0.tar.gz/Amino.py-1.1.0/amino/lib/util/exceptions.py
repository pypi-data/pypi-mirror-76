# AMINO ERROR 100
# Unknown Message
# Unknown Code
class UnsupportedService(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

# AMINO ERROR 102
# Unknown Message
# API_STD_ERR_ENTITY_TOO_LARGE_RAW
class FileTooLarge(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

# AMINO ERROR 103, 104
# Unknown Message
# Unknown Code
class InvalidRequest(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

# AMINO ERROR 105
# Unknown Message
# Unknown Code
class InvalidSession(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

# AMINO ERROR 106
# Unknown Message
# Unknown Code
class AccessDenied(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

# AMINO ERROR 107
# Unknown Message
# Unknown Code
class UnexistentData(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

# AMINO ERROR 113
# Be more specific, please.
# Unknown Code
class MessageNeeded(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

# AMINO ERROR 200
# Unknown Message
# Unknown Code
class InvalidAccountOrPassword(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

# AMINO ERROR 200
# Unknown Message
# Unknown Code
class EmailAlreadyRegistered(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

# AMINO ERROR 210
# Unknown Message
# AUTH_DISABLED_ACCOUNT
class AccountDisabled(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

# AMINO ERROR 213
# Unknown Message
# API_ERR_EMAIL
class InvalidEmail(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

# AMINO ERROR 214
# Unknown Message
# API_ERR_PASSWORD
class InvalidPassword(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

# AMINO ERROR 215
# This email address is not supported
# EMAIL_TAKEN
class UnsupportedEmail(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

# AMINO ERROR 216
# Unknown Message
# AUTH_ACCOUNT_NOT_EXISTS
class AccountDoesntExist(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

# AMINO ERROR 219
# Unknown Message
# Unknown Code
class AccountLimitReached(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

# AMINO ERROR 219
# Unknown Message
# Unknown Code
class TooManyRequests(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

# AMINO ERROR 221
# Unknown Message
# Unknown Code
class CantFollowYourself(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

# AMINO ERROR 225
# Unknown Message
# Unknown Code
class UserUnavailable(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

# AMINO ERROR 229
# Unknown Message
# Unknown Code
class YouAreBanned(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

# AMINO ERROR 230
# Unknown Message
# Unknown Code
class UserNotMemberOfCommunity(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

# AMINO ERROR 239
# Sorry, you can not do this before transferring your Agent status to another member.
# Unknown Code
class CantLeaveCommunity(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

# AMINO ERROR 240
# Unknown Message
# Unknown Code
class ReachedTitleLength(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

# AMINO ERROR 246
# Unknown Message
# AUTH_RECOVERABLE_DELETED_ACCOUNT
class AccountDeleted(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

# AMINO ERROR 249
# Unknown Message
# PHONE_NUMBER
class PHONE_NUMBER(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

# AMINO ERROR 251
# Unknown Message
# EMAIL_NO_PASSWORD
class EMAIL_NO_PASSWORD(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

# AMINO ERROR 262
# Unknown Message
# Unknown Code
class ReachedMaxTitles(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

# AMINO ERROR 270
# Unknown Message
# Unknown NEED_TWO_FACTOR_AUTHENTICATION
class VerificationRequired(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

# AMINO ERROR 271
# Unknown Message
# API_ERR_INVALID_AUTH_NEW_DEVICE_LINK
class API_ERR_INVALID_AUTH_NEW_DEVICE_LINK(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

# AMINO ERROR 291
# Whoa there! You've done too much too quickly. Take a break and try again later.
# Unknown Code
class CommandCooldown(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

# AMINO ERROR 300
# Unknown Message
# Unknown Code
class BadImage(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

# AMINO ERROR 313
# Unknown Message
# Unknown Code
class InvalidThemepack(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

# AMINO ERROR 314
# Unknown Message
# Unknown Code
class InvalidVoiceNote(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

# AMINO ERROR 500
# Sorry, the requested data no longer exists. Try refreshing the view
# Unknown Code
class RequestedNoLongerExists(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

# AMINO ERROR 503
# Sorry, you have reported this page too recently
# Unknown Code
class PageRepostedTooRecently(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

# AMINO ERROR 551
# This post type is restricted to members with a level X ranking and above.
# Unknown Code
class InsufficientLevel(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

# AMINO ERROR 702
# Unknown Message
# Unknown Code
class WallCommentingDisabled(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

# AMINO ERROR 805
# Unknown Message
# Unknown Code
class CommunityNameAlreadyTaken(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

# AMINO ERROR 801
# This Community no longer exists.
# Unknown Code
class CommunityNoLongerExists(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

# AMINO ERROR 802
# Sorry, this code or link is invalid.
# Unknown Code
class InvalidCodeOrLink(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

# AMINO ERROR 833
# This Community has been deleted.
# Unknown Code
class CommunityDeleted(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

# AMINO ERROR 1605
# Unknown Message
# Unknown Code
class ChatFull(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

# AMINO ERROR 1661
# Unknown Message
# Unknown Code
class LevelFiveRequiredToEnableProps(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

# AMINO ERROR 1663
# Unknown Message
# Unknown Code
class ChatViewOnly(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

# AMINO ERROR 2601
# Unknown Message
# Unknown Code
class AlreadyCheckedIn(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

# AMINO ERROR 2001
# Sorry, you have already submitted a membership request.
# Unknown Code
class AlreadyRequested(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

# AMINO ERROR 2611
# Unknown Message
# Unknown Code
class AlreadyUsedMonthlyRepair(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

# AMINO ERROR 2800
# Unknown Message
# Unknown Code
class AccountAlreadyRestored(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

# AMINO ERROR 3102
# Incorrect verification code
# Unknown Code
class IncorrectVerificationCode(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

# AMINO ERROR 4300
# Unknown Message
# Unknown Code
class NotEnoughCoins(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

# AMINO ERROR 4400
# Unknown Message
# Unknown Code
class AlreadyPlayedLottery(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

# AMINO ERROR 4500, 4501
# Unknown Message
# Unknown Code
class CannotSendCoins(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class SpecifyType(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class UnknownResponse(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class UnsupportedFileExtension(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class NotLoggedIn(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class NoCommunity(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class NoChatThread(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class ChatRequestsBlocked(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class NoImageSource(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class CannotFetchImage(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class FailedLogin(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)


class LibraryUpdateAvailable(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class InvalidDeveloperKey(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class DeveloperKeyRequired(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)
