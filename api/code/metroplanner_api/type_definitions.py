import pydantic

# from datetime import datetime
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
ShortText = Annotated[str, pydantic.StringConstraints(max_length=50)]
LongText = Annotated[str, pydantic.StringConstraints(max_length=500)]
LocalizedShortText = Dict[str, ShortText]
LocalizedLongText = Dict[str, LongText]
MaybeLocalizedShortText = Union[LocalizedShortText, ShortText]
MaybeLocalizedLongText = Union[LocalizedLongText, LongText]
Point = pydantic.conlist(IntOrFloat, min_length=2, max_length=2)
Identifier = Annotated[str, pydantic.StringConstraints(max_length=36, min_length=36)]
ColorCSS = Annotated[str, pydantic_extra_types.color.Color]
ColorReference = Annotated[
    str,
    pydantic.StringConstraints(
        pattern=(
            r"(^(fore|back)ground$)"
            r"|(^landscape::(((deep|shallow)?water)|border)$)"
            r"|(^lines::\d{1,3}$)"
        )
    ),
]


def check_color(v: str) -> str:
    ColorCSS = Annotated[str, pydantic_extra_types.color.Color]
    ColorReference = Annotated[
        str,
        pydantic.StringConstraints(
            pattern=(
                r"(^(fore|back)ground$)"
                r"|(^landscape::(((deep|shallow)?water)|border)$)"
                r"|(^lines::\d{1,3}$)"
            )
        ),
    ]

    class ModelCheck(BaseModel):
        color: Union[ColorCSS, ColorReference]

    try:
        m = ModelCheck(color=v)
        return v
    except Exception as e:
        raise ValueError()


Color = Annotated[str, pydantic.AfterValidator(check_color)]


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
            if (
                MissingValueBaseClass in get_args(field_spec.annotation)
                and (field_value := self.__getattribute__(field_name)) != Missing
            )
            or (MissingValueBaseClass not in get_args(field_spec.annotation))
        }


"""
Submodels
"""


class AnchorAtNode(BaseModel):
    node: Identifier
    x_shift: IntOrFloat = 0
    y_shift: IntOrFloat = 0


class AnchorAtInferredNode(BaseModel):
    x_shift: IntOrFloat = 0
    y_shift: IntOrFloat = 0


class AnchorAtPoint(BaseModel):
    coords: Point


Anchor = Union[AnchorAtNode, AnchorAtPoint, AnchorAtInferredNode]


class Styling(BaseModel):
    font_size: pydantic.confloat(gt=0.1, lt=10)


class Label(BaseModel):
    label_class: Annotated[
        str, 
        pydantic.StringConstraints(
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
    text: str = ""
    anchor: Anchor = None
    styling: Optional[Styling] = None


class Marker(BaseModel):
    width: IntOrFloat = 1
    height: IntOrFloat = 1
    size_factor: Union[IntOrFloat, str] = 1  # TODO: Add constrain
    rotation: IntOrFloat = 0


class Node(BaseModel):
    location: Point
    marker: Marker
    label: Label = Label()


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
    anchor: Anchor
    text: ShortText
    width: NonNegativeIntOrFloat
    height: NonNegativeIntOrFloat
    styling: Optional[Styling] = None


"""
Planstate
"""


class PlanstateStats(BaseModel):
    created_at: str  # datetime
    number_of_labels: NonNegativeInt
    number_of_nodes: NonNegativeInt
    number_of_lines: NonNegativeInt
    number_of_edges: NonNegativeInt


class PlanstateDimensions(BaseModel):
    global_offset_x: IntOrFloat = 0
    global_offset_y: IntOrFloat = 0
    plan_width: IntOrFloat = 10
    plan_height: IntOrFloat = 10


class PlanstateComponentOderings(BaseModel):
    nodes_ordering: List[Identifier] = []
    lines_ordering: List[Identifier] = []
    labels_ordering: List[Identifier] = []


class PlanstateComponents(BaseModel):
    nodes: Dict[Identifier, Node] = {}
    lines: Dict[Identifier, Line] = {}
    independent_labels: Dict[Identifier, IndependentLabel] = {}


class CreatePlanstate(
    PlanstateDimensions,
    PlanstateComponents,
    # PlanstateComponentOderings
    ModelMayMissFields,
):
    color_theme: MaybeMissing(Optional[Union[str, ObjectId]]) = Missing
    make_current: bool = False


class PlanstateHistoryItem(PlanstateStats):
    pass


class PlanstateHistoryItemWithID(PlanstateHistoryItem):
    planstate_id: ObjectId


class Planstate(CreatePlanstate, PlanstateHistoryItem):
    pass


class PlanstateID(BaseModel):
    _id: ObjectId


class PlanstateInDB(Planstate, PlanstateID):
    pass


class PlanstatePublicGetResponse(
    PlanstateDimensions,
    PlanstateComponents,
    PlanstateStats,
):
    pass


class PlanstatePublicGetResponseV2:
    class LineSegment(BaseModel):
        pass

    css: Optional[str] = None
    hash: Optional[str] = None
    nodes: Union[Dict[str, Node], Dict[Identifier, Node]] = {}
    lines: Union[List[Line], Dict[Identifier, Line]] = []
    line_segments: Dict[Identifier, LineSegment] = []


class PlanstatePrivateGetResponse(
    PlanstateStats,
    PlanstateDimensions,
    PlanstateComponents,
    PlanstateComponentOderings,
):
    color_theme: Optional[Union[str, ObjectId]] = None


class PlanstatePrivatePostResponse(PlanstateID):
    pass


"""
Plan
"""


class PlanProfile(BaseModel):
    plan_name: ShortText
    plan_description: LongText


class PlanPrivateView(PlanProfile):
    plan_id: ObjectId
    primary_shortlink: Optional[str] = None
    shortlinks: List[Dict[str, str]] = {}


class PlanTimestamps(BaseModel):
    last_modified_at: str  # datetime
    created_at: str  # datetime


class PlanStats(BaseModel):
    like_count: NonNegativeInt = 0
    current_number_of_labels: NonNegativeInt
    current_number_of_nodes: NonNegativeInt
    current_number_of_lines: NonNegativeInt
    current_number_of_edges: NonNegativeInt


class Plan(PlanProfile, PlanStats):
    forked_from: Optional[ObjectId]
    owned_by: str
    created_at: str  # datetime
    last_modified_at: str  # datetime
    like_count: NonNegativeInt
    # likes_received: List[str]
    # current_color_theme: ObjectId


class PlanID(BaseModel):
    plan_id: ObjectId


class PlanInDB(Plan):
    _id: ObjectId
    current_state: ObjectId
    history: List[ObjectId]
    deleted: Optional[str] = None  # datetime]


class PlanPublicGetResponse(Plan):
    total_view_count: NonNegativeInt


class PlanPrivateGetResponse(PlanProfile, PlanStats, PlanTimestamps):
    class ShortlinkWithStats(BaseModel):
        class Stats(BaseModel):
            total_count: NonNegativeInt
            per_hour: List[Tuple[int, NonNegativeInt]]
            per_day: List[Tuple[int, NonNegativeInt]]
            per_month: List[Tuple[int, NonNegativeInt]]

        shortlink: str
        stats: Stats
        auto_generated: bool = False

    history: List[PlanstateHistoryItemWithID]
    shortlinks: List[ShortlinkWithStats]
    color_theme: Optional[str] = None
    current_state: ObjectId
    forked_from: Optional[ObjectId] = None
    owned_by: str
    primary_shortlink: Optional[str] = None


class PlanPrivatePostRequest(PlanProfile):
    class ForkFromShortlink(BaseModel):
        shortlink: ShortText

    class ForkFromPrivatePlan(BaseModel):
        plan_id: ObjectId
        planstate_id: Optional[ObjectId] = None

    forkFrom: Optional[Union[ForkFromPrivatePlan, ForkFromShortlink]] = None


class PlanPrivatePostResponse(PlanID):
    pass


class PlanPrivatePatchRequest(ModelMayMissFields):
    current_state: MaybeMissing(ObjectId) = Missing
    plan_name: MaybeMissing(ShortText) = Missing
    plan_description: MaybeMissing(LongText) = Missing
    # TODO: Add color theme


class PlanPrivatePatchResponse(ModelMayMissFields):
    current_state: MaybeMissing(ObjectId) = Missing
    plan_name: MaybeMissing(ShortText) = Missing
    plan_description: MaybeMissing(LongText) = Missing
    last_modified_at: str


"""
User
"""


class UserCommons(BaseModel):
    bio: LongText
    display_name: ShortText
    profile_picture: Optional[str] = None
    public: bool = True


class User(UserCommons):
    profile_views: NonNegativeInt = 0
    likes_given: List[ObjectId] = []
    plans_created: List[PlanPrivateView]


class UserInDB(User):
    _id: str


class UserPrivatePatchRequest(UserCommons, ModelMayMissFields):
    bio: MaybeMissing(LongText) = Missing
    display_name: MaybeMissing(ShortText) = Missing
    profile_picture: MaybeMissing(Optional[str]) = Missing
    public: MaybeMissing(bool) = Missing
    plans_created: List = []  # TODO: Change to PlanPrivateView


class UserPrivatePatchResponse(UserCommons):
    pass


class UserPrivateGetResponse(UserInDB):
    pass


class UserPublicDetailedGetResponse(User):
    plans_created: List[PlanPublicGetResponse] = []


class UserPublicGetResponse(UserCommons):
    pass


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
