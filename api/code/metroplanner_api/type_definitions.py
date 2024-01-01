import pydantic
from datetime import datetime
import pydantic_extra_types.color
from typing import List, Dict, Set, Tuple, Union, Optional, Annotated, get_args
from abc import ABC
from humps import camelize
from bson.objectid import ObjectId as BsonObjectId


class BaseModel(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(alias_generator=camelize, populate_by_name=True)


def check_object_id(oid: str) -> str:
    if not BsonObjectId.is_valid(oid):
        raise ValueError("Invalid ObjectId")
    return oid


ObjectId = Annotated[str, pydantic.AfterValidator(check_object_id)]


"""
Basic Types
"""


class MissingValueBaseClass(BaseModel):
    pass


Missing = MissingValueBaseClass()
NonNegativeInt = Annotated[int, pydantic.Field(ge=0)]
IntOrFloat = Union[int, float]
PositiveIntOrFloat = Annotated[Union[int, float], pydantic.Field(gt=0)]
NonNegativeIntOrFloat = Annotated[Union[int, float], pydantic.Field(ge=0)]
ShortText = pydantic.constr(max_length=100)
LongText = pydantic.constr(max_length=500)
LocalizedShortText = Dict[str, ShortText]
LocalizedLongText = Dict[str, LongText]
MaybeLocalizedShortText = Union[LocalizedShortText, ShortText]
MaybeLocalizedLongText = Union[LocalizedLongText, LongText]
Identifier = pydantic.constr(min_length=36, max_length=36)
ColorCSS = pydantic_extra_types.color.Color
ColorReference = pydantic.constr(
    pattern=(
        r"(^(fore|back)ground$)"
        r"|(^landscape::(((deep|shallow)?water)|border)$)"
        r"|(^lines::\d{1,3}$)"
    )
)
Color = Union[ColorReference, ColorCSS]


Point = Tuple[IntOrFloat, IntOrFloat]


def MaybeMissing(t):
    return Union[MissingValueBaseClass, t]


class ModelMayMissFields(BaseModel):
    def get_existing_fields(self):
        """
        Iterates over the Model's fields and returns a dict containing only values that are not Missing.
        If field of type ModelMayMissFields is encountered, get_existing_fields is called recursively.
        """
        return {
            field_name: (
                field_value.get_existing_fields()
                if isinstance(field_value, ModelMayMissFields)
                else field_value
            )
            for field_name, field_spec in self.model_fields.items()
            if MissingValueBaseClass in get_args(field_spec.annotation)
            and (field_value := self.__getattribute__(field_name)) != Missing
        }


"""
Submodels
"""


class Anchor(BaseModel):
    ## node: Union[Point, Identifier]
    node: Union[Point, str]
    x_shift: IntOrFloat = 0
    y_shift: IntOrFloat = 0


class Styling(BaseModel):
    font_size: pydantic.confloat(gt=0.1, lt=10)


class Span(BaseModel):
    coords: Point
    width: NonNegativeIntOrFloat
    height: NonNegativeIntOrFloat


class Label(BaseModel):
    label_class: Annotated[
        pydantic.constr(
            pattern=(
                "centered"
                "|left_ascending"
                "|right_ascending"
                "|left_descending"
                "|right_descending"
                "|left"
                "|right"
                "|span"
            )
        ),
        pydantic.Field(
            alias="class",
            alias_priority=2,
        ),
    ] = "right"
    text: str
    ## anchor: Anchor
    anchor: Union[Span, Anchor]
    styling: Optional[Styling] = None


class Marker(BaseModel):
    width: IntOrFloat = 1
    height: IntOrFloat = 1
    size_factor: Union[IntOrFloat, str] = 1  # TODO: Add constrain
    rotation: IntOrFloat = 0


class Node(BaseModel):
    location: Point
    marker: Marker
    ## label: Label
    label: Union[str, Label]


class Connection(BaseModel):
    nodes: List[Anchor]


class Line(BaseModel):
    name: str
    color: Color
    border_width: Optional[NonNegativeIntOrFloat] = None
    border_style: Optional[str] = None  # TODO: constrain
    border_color: Optional[Color] = None
    width: NonNegativeIntOrFloat
    connections: List[Connection]


class IndependentLabel(BaseModel):
    ## anchor: Anchor
    anchor: Union[Span, Anchor]
    text: str
    width: NonNegativeIntOrFloat
    height: NonNegativeIntOrFloat


"""
Planstate
"""


class PlanstateStats(BaseModel):
    created_at: datetime
    number_of_labels: NonNegativeInt
    number_of_nodes: NonNegativeInt
    number_of_lines: NonNegativeInt
    number_of_edges: NonNegativeInt


class PlanstateDimensions(BaseModel):
    global_offset_x: Union[float, int]
    global_offset_y: Union[float, int]
    plan_width: Union[float, int]
    plan_height: Union[float, int]


class PlanstateComponentOderings(BaseModel):
    nodes_ordering: List[Identifier] = []
    lines_ordering: List[Identifier] = []
    labels_ordering: List[Identifier] = []


class PlanstateComponents(BaseModel):
    nodes: Union[Dict[str, Node], Dict[Identifier, Node]] = {}
    lines: Union[List[Line], Dict[Identifier, Line]] = []
    labels: Union[
        Dict[str, Label], Dict[Identifier, Union[Label, IndependentLabel]]
    ] = {}


class CreatePlanstate(
    PlanstateDimensions, PlanstateComponents, PlanstateComponentOderings
):
    color_theme: Optional[Union[str, ObjectId]] = None


class PlanstateHistoryItem(PlanstateStats):
    pass


class PlanstateHistoryItemWithID(PlanstateHistoryItem):
    planstateid: ObjectId


class Planstate(CreatePlanstate, PlanstateHistoryItem):
    pass


class PlanstateInDB(Planstate):
    _id: ObjectId


# class LineSegment(BaseModel):
#     pass


class PlanstateViewerResponse:
    css: Optional[str] = None
    hash: Optional[str] = None
    nodes: Union[Dict[str, Node], Dict[Identifier, Node]] = {}
    nodes_ordering: List[Identifier] = []
    lines: Union[List[Line], Dict[Identifier, Line]] = []
    # line_segments: Dict[Identifier, LineSegment] = []


"""
Plan
"""


class PlanProfile(BaseModel):
    plan_name: ShortText
    plan_description: LongText


class PlanPrivateView(PlanProfile):
    plan_id: ObjectId
    plan_shortlink: ShortText


class Stats(BaseModel):
    total_count: NonNegativeInt
    views: Dict[str, NonNegativeInt]


class ShortlinkWithStats(BaseModel):
    _id: str
    stats: Stats


class PlanTimings(BaseModel):
    last_modified_at: datetime
    created_at: datetime


class PlanStats(BaseModel):
    like_count: NonNegativeInt = 0
    current_number_of_labels: NonNegativeInt
    current_number_of_nodes: NonNegativeInt
    current_number_of_lines: NonNegativeInt
    current_number_of_edges: NonNegativeInt


class Plan(PlanProfile):
    forked_from: Optional[ObjectId]
    owned_by: ObjectId
    created_at: datetime
    last_modified_at: datetime
    like_count: NonNegativeInt
    # likes_received: List[str]

    current_number_of_labels: NonNegativeInt
    current_number_of_nodes: NonNegativeInt
    current_number_of_lines: NonNegativeInt
    current_number_of_edges: NonNegativeInt
    # current_color_theme: ObjectId


class PlanID(BaseModel):
    plan_id: ObjectId


class PlanInDB(Plan):
    _id: ObjectId
    current_state: ObjectId
    history: List[ObjectId]
    deleted: Optional[datetime]


class PlanPrivateGetResponse(PlanProfile, PlanStats):
    history: List[PlanstateHistoryItemWithID]
    shortlinks: List[ShortlinkWithStats]
    color_theme: Optional[str] = None
    current_state: ObjectId
    forked_from: ObjectId
    owned_by: str
    primary_shortlink: Optional[str] = None


class PlanPrivatePatchRequest(PlanProfile):
    current_state: ObjectId


class PlanPublicGetResponse(Plan):
    total_view_count: NonNegativeInt


class PlanPostRequest(PlanProfile):
    class ForkFromShortlink(BaseModel):
        shortlink: ShortText

    class ForkFromPrivatePlan(BaseModel):
        plan_id: ObjectId
        planstate_id: Optional[ObjectId] = None

    forkFrom: Optional[Union[ForkFromPrivatePlan, ForkFromShortlink]] = None


"""
User
"""


class UserCommons(BaseModel):
    bio: LongText
    display_name: ShortText
    profile_picture: Optional[str] = None
    public: bool = True


class UpdateUser(UserCommons, ModelMayMissFields):
    bio: MaybeMissing(LongText) = Missing
    display_name: MaybeMissing(ShortText) = Missing
    profile_picture: MaybeMissing(Optional[str]) = Missing
    public: MaybeMissing(bool) = Missing


class User(UserCommons):
    profile_views: NonNegativeInt = 0
    likes_given: List[ObjectId] = []
    plans_created: Optional[List[PlanPrivateView]] = None


class UserInDB(User):
    _id: str  # User ID from OAuth


"""
Link
"""


# class CreateLink(BaseModel):
#     _id: Optional[ShortText]
#     plan: ObjectId
#     active: bool = True
#
#
# class UpdateLink(BaseModel):
#     """Set an existing link to active or inactive"""
#     _id: ShortText
#     active: bool


class Link(BaseModel):
    _id: ShortText
    plan: ObjectId
    auto_generated: bool
    active: bool


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
