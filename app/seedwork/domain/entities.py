from abc import ABC
from dataclasses import dataclass
from pydantic import BaseModel


@dataclass
class Entity(BaseModel, ABC):
    ...
