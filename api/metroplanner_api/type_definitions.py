from pydantic import BaseModel, Field, constr, conint, confloat
from datetime import datetime
import pydantic_extra_types.color
from typing import List, Dict, Set, Tuple, Union, Optional, Annotated, BeforeValidator
from abc import ABC


ObjectId = Annotated[str, BeforeValidator(str)]
NonNegativeInt = Annotated[int, Field(ge=0)]
IntOrFloat = Union[int, float]
PositiveIntOrFloat = Annotated[Union[int, float], Field(gt=0)]
NonNegativeIntOrFloat = Annotated[Union[int, float], Field(ge=0)]
Point = Tuple[IntOrFloat, IntOrFloat]
ColorCSS = pydantic_extra_types.color.Color
ShortText = constr(max_length=100)
LongText = constr(max_length=500)
Identifier = constr(min_length=36, max_length=36)

ColorReference = constr(
    pattern=(
        r"(^(fore|back)ground$)"
        r"|(^landscape::(((deep|shallow)?water)|border)$)"
        r"|(^lines::\d{1,3}$)"
    )
)

Color = Union[ColorReference, ColorCSS]


class Anchor(BaseModel):
    node: Union[Point, Identifier]
    xShift: IntOrFloat
    yShift: IntOrFloat


class Styling(BaseModel):
    fontSize: confloat(gt=0.1, lt=10)


class Label(BaseModel):
    labelClass: constr(
        pattern=(
            "centered"
            "|left_ascending"
            "|right_ascending"
            "|left_descending"
            "|right_descending"
            "|left"
            "|right"
        )
    )
    text: str
    anchor: Anchor
    styling: Optional[Styling]


class Marker(BaseModel):
    width: IntOrFloat
    height: IntOrFloat
    sizeFactor: Union[IntOrFloat, str]  # TODO: Add constrain
    rotation: IntOrFloat


class Node(BaseModel):
    location: Point
    marker: Marker
    label: Label


class Connection(BaseModel):
    nodes: List[Anchor]


class Line(BaseModel):
    name: str
    color: Color
    borderWidth: PositiveIntOrFloat
    borderStyle: str  # TODO: constrain
    borderColor: Color
    width: PositiveIntOrFloat
    connections: List[Connection]


class IndependentLabel(BaseModel):
    anchor: Anchor
    text: str
    width: NonNegativeIntOrFloat
    height: NonNegativeIntOrFloat 


class User(BaseModel):
    _id: ObjectId
    username: str
    displayName: str
    public: bool
    mailto: Optional[str] = None
    profileViews: NonNegativeInt = 0
    likesGiven: List[ObjectId] = []
    profilePicture: Optional[str] = None


class Planstate(BaseModel):
    createdAt: datetime
    colorTheme: ObjectId
    numberOfLabels: NonNegativeInt
    numberOfNodes: NonNegativeInt
    numberOfLines: NonNegativeInt
    numberOfEdges: NonNegativeInt

    nodes: Dict[Identifier, Node]
    nodesOrdering: List[Identifier]
    lines: Dict[Identifier, Line]
    linesOrdering: List[Identifier]
    independentLabels: Dict[Identifier, IndependentLabel]
    labelsOrdering: List[Identifier]

    globalOffsetX: Union[float, int]
    globalOffsetY: Union[float, int]
    planWidth: Union[float, int]
    planHeight: Union[float, int]


class Plan(BaseModel):
    forkedFrom: Optional[ObjectId]
    ownedBy: ObjectId
    planName: ShortText
    planDescription: LongText
    createdAt: datetime
    lastModifiedAt: datetime
    history: List[ObjectId]
    # likeCount: PositiveIntOrZero
    deleted: Optional(datetime)

    currentState: ObjectId
    currentNumberOfLabels: NonNegativeInt
    currentNumberOfNodes: NonNegativeInt
    currentNumberOfLines: NonNegativeInt
    currentNumberOfEdges: NonNegativeInt
    currentColorTheme: ObjectId


# class LandscapeColors(BaseModel):
#     river: ColorCSS
#     border: ColorCSS
#
# class ThemeData(BaseModel):
#     backgroundColor: ColorCSS
#     foregroundColor: ColorCSS
#     lineColors: ColorCSS
#     landscape: LandscapeColors
#
# class ColorTheme(BaseModel):
#     themeName: str
#     builtin: bool
#     public: bool
#     forkedFrom: Optional[ObjectId]
#     ownedBy: Optional[ObjectId]
#     themeData: ThemeData
