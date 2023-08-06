from dataclasses import dataclass

from traktor.timestamp import humanize
from traktor.models.model import VanillaModel


@dataclass
class Report(VanillaModel):
    HEADERS = VanillaModel.HEADERS + [
        ("Project", "project"),
        ("Task", "task"),
        ("Time", "humanized_time"),
    ]

    project: str
    task: str
    time: int

    @property
    def key(self):
        return f"{self.project}-{self.task}"

    @property
    def humanized_time(self):
        return humanize(self.time)

    def to_dict(self) -> dict:
        return {
            "project": self.project,
            "task": self.task,
            "time": self.time,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Report":
        return cls(project=d["project"], task=d["task"], time=d["time"])
