from dataclasses import dataclass
from commons.core.model import CoreModel


@dataclass(repr=True, frozen=True, kw_only=True, eq=True)
class NoteModel(CoreModel):
    id: int
    title: str
    content: str
    user_id: int
