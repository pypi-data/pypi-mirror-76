class Error(Exception):
    pass


class LoginError(Error):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class UserOrPassError(LoginError):
    def __init__(self, value=None):
        super().__init__(value or "用户名或密码错误!")


class UserNotFoundError(LoginError):
    def __init__(self, value=None):
        super().__init__(value or "用户不存在!")


class UserDefunctError(LoginError):
    def __init__(self, value=None):
        super().__init__(value or "用户已失效!")

class RoleError(Error):
    def __init__(self, value=None):
        self.value = value or "账号是未知用户"

    def __str__(self):
        return str(self.value)


class ArgError(Error):
    def __init__(self, value=None):
        self.value = value or "请输入正确的参数!"

    def __str__(self):
        return str(self.value)
