import enum
from dataclasses import dataclass

from traktor.models.model import VanillaModel


class ConfigKey(str, enum.Enum):
    format = "format"
    db_path = "db_path"
    timezone = "timezone"


@dataclass
class ConfigEntry(VanillaModel):

    Key = ConfigKey

    HEADERS = VanillaModel.HEADERS + [
        ("Key", "key.value"),
        ("Value", "value"),
    ]

    key: ConfigKey
    value: str

    def to_dict(self) -> dict:
        return {
            "key": self.key,
            "value": self.value,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "ConfigEntry":
        return cls(key=d["key"], value=d["value"])
