class CantDeleteDevGroupError(Exception):
    def __init__(self, message=None, errors=None):
        super().__init__(message)
        self.message = (
            message
            if message
            else "Tried to delete developer-created groups."
            " If you must delete it, please use force_delete"
        )
        self.errors = errors if not errors else []
