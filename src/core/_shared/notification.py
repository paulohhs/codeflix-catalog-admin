from dataclasses import dataclass, field


@dataclass
class Notification:
    def __init__(self) -> None:
        self.errors: list[str] = []

    @property
    def has_errors(self) -> bool:
        return bool(self.errors)

    @property
    def messages(self) -> str:
        return ", ".join(self.errors)

    def add_error(self, message: str) -> None:
        self.errors.append(message)
