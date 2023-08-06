from pydantic import BaseModel
from typing import Optional


class AnnoationLocation(BaseModel):
    start: int
    end: int

    def __eq__(self, other):
        return self.start == other.start and self.end == other.end

    def __hash__(self):
        return hash("{}-{}".format(self.start, self.end))

    def __repr__(self):
        return "AnnotationLocation(start={}, end={})".format(self.start, self.end)

    def __str__(self):
        return "AnnotationLocation(start={}, end={})".format(self.start, self.end)

    def __lt__(self, other):
        return self.start < other.start and self.end < other.end


class Entity(BaseModel):
    entity_type: str
    text: str
    location: AnnoationLocation
    subtype: str = "NONE"
    score: Optional[float]


class Relation(BaseModel):
    relation_type: str
    sentence: str
    score: float
    head: Entity
    tail: Entity
