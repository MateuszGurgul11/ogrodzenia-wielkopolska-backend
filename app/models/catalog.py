from typing import Literal

from pydantic import BaseModel, Field, field_validator
import re

COLLECTION_NAMES = ("posts", "panels", "spacerOptions", "heights", "colors")
CollectionName = Literal["posts", "panels", "spacerOptions", "heights", "colors"]

HEX_RE = re.compile(r"^#[0-9A-Fa-f]{6}$")
PATTERN_IDS = ("pattern-solid", "pattern-lines", "pattern-grid", "pattern-brick")


class BaseEntity(BaseModel):
    name: str = Field(min_length=1)
    sortOrder: int = Field(ge=0, default=0)
    active: bool = True
    description: str | None = None
    previewAsset: str | None = None


class PostCreate(BaseEntity):
    slug: str = Field(min_length=1, pattern=r"^[a-z0-9-]+$")
    widthCm: float = Field(ge=10, le=50)


class PostOut(PostCreate):
    id: str


class PanelCreate(BaseEntity):
    patternId: Literal[
        "pattern-solid", "pattern-lines", "pattern-grid", "pattern-brick"
    ]


class PanelOut(PanelCreate):
    id: str


class SpacerCreate(BaseEntity):
    hasSpacer: bool
    openness: float = Field(ge=0, le=1)


class SpacerOut(SpacerCreate):
    id: str


class HeightCreate(BaseModel):
    label: str = Field(min_length=1)
    valueM: float = Field(ge=1.0, le=2.25)
    sortOrder: int = Field(ge=0, default=0)
    active: bool = True
    description: str | None = None


class HeightOut(HeightCreate):
    id: str


class ColorCreate(BaseEntity):
    hex: str

    @field_validator("hex")
    @classmethod
    def validate_hex(cls, v: str) -> str:
        if not HEX_RE.match(v):
            raise ValueError("Kolor musi być w formacie #RRGGBB")
        return v


class ColorOut(ColorCreate):
    id: str


class CatalogCollections(BaseModel):
    posts: list[PostOut]
    panels: list[PanelOut]
    spacerOptions: list[SpacerOut]
    heights: list[HeightOut]
    colors: list[ColorOut]


CREATE_MODELS = {
    "posts": PostCreate,
    "panels": PanelCreate,
    "spacerOptions": SpacerCreate,
    "heights": HeightCreate,
    "colors": ColorCreate,
}

OUT_MODELS = {
    "posts": PostOut,
    "panels": PanelOut,
    "spacerOptions": SpacerOut,
    "heights": HeightOut,
    "colors": ColorOut,
}
