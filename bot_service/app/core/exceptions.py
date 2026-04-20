# базовая ошибка сервиса
class BotServiceError(Exception):
    pass

# ошибки токена
class TokenExpiredError(BotServiceError):
    pass

class TokenInvalidError(BotServiceError):
    pass

# ошибки openrouter
class OpenRouterError(BotServiceError):
    pass
