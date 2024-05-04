class CantDeleteDevGroupError(Exception):
    def __init__(self, message=None, errors=None):
        self.message = (
            message
            if message
            else "Tried to delete developer-created groups."
            " If you must delete it, please use force_delete"
        )
        self.errors = errors if not errors else []
        super().__init__(
            self.message + (f"Caused by: {self.errors}" if self.errors else "")
        )


class GroupExcludesCreatorInMembersError(Exception):
    def __init__(self, message=None, errors=None):
        self.message = (
            message
            if message
            else "Can't create Group without creator included in members"
        )
        self.errors = errors if not errors else []
        super().__init__(
            self.message + (f"Caused by: {self.errors}" if self.errors else "")
        )


class GroupDoesntHaveCreatorError(Exception):
    def __init__(self, message=None, errors=None):
        self.message = message if message else "Can't create Group without creator"
        self.errors = errors if not errors else []
        super().__init__(
            self.message + (f"Caused by: {self.errors}" if self.errors else "")
        )
