class UserNotFoundException(Exception):

    def __init__(self, username: str):
        self.message = f"User {username} not found"
        super().__init__(self.message)


class DuplicateUserException(Exception):

    def __init__(self, username: str):
        self.message = f"User {username} already exists"
        super().__init__(self.message)


class UserAlreadyAdminException(Exception):

    def __init__(self, username: str):
        self.message = f"User {username} is already an administrator"
        super().__init__(self.message)


class UserAlreadyBannedException(Exception):

    def __init__(self, username: str):
        self.message = f"User {username} is already banned"
        super().__init__(self.message)


class UserNotAdminException(Exception):

    def __init__(self, username: str):
        self.message = f"User {username} is not an administrator"
        super().__init__(self.message)


class UserNotBannedException(Exception):

    def __init__(self, username: str):
        self.message = f"User {username} is not banned"
        super().__init__(self.message)
