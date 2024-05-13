class MdmaError(Exception):
    pass


class MdmaMissingConfigError(MdmaError):

    def __init__(self, key_path: str):
        self.key_path = key_path

    def __str__(self) -> str:
        return f'No key "{self.key_path}" in configuration file.'
