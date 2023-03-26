definite_color_patterns = [
    {
        "type": "string",
        "pattern": "^#([0-9a-fA-F]{3,4}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})$",
    },
    {
        "type": "string",
        "pattern": "^hsl\(\d{1,3},\s?\d{1,3}%,\s?\d{1,3}%\)$",
    },
    {
        "type": "string",
        "pattern": "^hsla\(\d{1,3},\s?\d{1,3}%,\s?\d{1,3}%,\s?(1|(0\.\d{1,10}))\)$",
    },
]

theme_color_patterns = [
    {
        "type": "string",
        "pattern": "^(fore|back)ground$",
    },
    {
        "type": "string",
        "pattern": "^landscape::(((deep|shallow)?water)|border)$",
    },
    {
        "type": "string",
        "pattern": "^lines::\d{1,3}$",
    },
]

colors = {
    "oneOf": [
        *definite_color_patterns,
        *theme_color_patterns,
    ]
}

styling = {
    "type": "object",
    "properties": {
        "fontSize": {
            "type": "number",
            "description": "Font size as multiple of coordinate scalar",
            "minimum": 0.1,
            "maximum": 10,
        }
    },
}

point = {
    "type": "array",
    "items": {
        "type": "number",
        "description": "Coordinates of the point in multiples of coordinate scalar",
    },
    "minItems": 2,
    "maxItems": 2,
}

anchor = {
    "type": "object",
    "properties": {
        "node": {
            "oneOf": [
                point,
                {
                    "type": "string",
                    "description": "unique node identifier",
                    "maxLength": 50,
                },
            ]
        },
        "xShift": {"type": "number"},
        "yShift": {"type": "number"},
        "width": {"type": "number"},
        "height": {"type": "number"},
    },
}

label_basics = {
    "type": "object",
    "properties": {
        "class": {
            "type": "string",
            "enum": [
                "centered",
                "left_ascending",
                "right_ascending",
                "left_descending",
                "right_descending",
                "left",
                "right",
            ],
        },
        "text": {
            "type": "string",
            "minLength": 0,
            "maxLength": 100,
        },
        "anchor": anchor,
        "styling": styling,
    },
    "required": ["class", "text", "anchor"],
}

patch_user_schema = {
    "type": "object",
    "properties": {
        "bio": {
            "type": "string",
            "minLength": 0,
            "maxLength": 250,
        },
        "displayName": {
            "type": "string",
            "pattern": r"^.*$",
            "minLength": 3,
            "maxLength": 20,
        },
    },
    "additionalProperties": False,
    "required": [
        "bio",
        "displayName",
    ],
}

plan_basics = {
    "planName": {
        "type": "string",
        "description": "Display name of this plan.",
        "minLength": 0,
        "maxLength": 30,
    },
    "planDescription": {
        "type": "string",
        "description": "Description of this plan.",
        "minLength": 0,
        "maxLength": 250,
    },
}

post_plan_schema = {
    "type": "object",
    "description": "Request content for creating a new plan, either from scratch or forked from a public shortlink or private planstate.",
    "properties": {
        **plan_basics,
        "forkFrom": {
            "oneOf": [
                {
                    "type": "object",
                    "description":"For forking a plan from a public plan, given its shortlink.",
                    "properties": {
                        "shortlink": {
                            "type": "string",
                        }
                    },
                    "required": ["shortlink"],
                    "additionalProperties": False,
                },
                {
                    "type": "object",
                    "description":"For forking a plan from one's own plan's planstate.",
                    "properties": {
                        "planID": {
                            "type": "string"
                        },
                        "planstateID": {
                            "type": "string",
                        },
                    },
                    "required": ["planstateID", "planID"],
                    "additionalProperties": False,
                },
            ]
        },
    },
    "additionalProperties": False,
    "required": ["planName", "planDescription"],
}


patch_plan_schema = {
    "type": "object",
    "description": "Document containing a metro plans basic information, excluding state info.",
    "properties": {
        **plan_basics,
        "currentState": {
            "type": "objectId",
            "description": "ID of the current planstate.",
        },
        "currentColorTheme": {
            "oneOf": [
                {
                    "type": "string",
                    "enum": [
                        "colorful-dl",
                        "colorful-ld",
                        "glow",
                        "shine",
                        "pastels-dl",
                        "pastels-ld",
                        "dark-pastels",
                        "light-pastels",
                        "monochrome-dl",
                        "monochrome-ld",
                        "black-white",
                        "white-black",
                    ],
                },
                # {
                #     "type": "objectId",
                #     "description": "ID of the plan's color theme.",
                # },
            ]
        },
    },
    "additionalProperties": False,
    "required": [],
}

post_planstate_schema = {
    "type": "object",
    "description": "Document describing the state of a metro plan in its history",
    "properties": {
        "nodes": {
            "type": "object",
            "additionalProperties": {
                "type": "object",
                "properties": {
                    "location": point,
                    "marker": {
                        "type": "object",
                        "properties": {
                            "width": {
                                "type": "integer",
                                "minimum": 1,
                            },
                            "height": {
                                "type": "integer",
                                "minimum": 1,
                            },
                            "diagonalStretch": {
                                "type": "boolean",
                                "description": "Whether this marker should be stretched for diagonal use."
                                " Setting this to True has the same effect as setting sizeFactor to sqrt2.",
                            },
                            "sizeFactor": {
                                "oneOf": [
                                    {
                                        "type": "integer",
                                        "minimum": 1,
                                        "maximum": 1,
                                    },
                                    {
                                        "type": "string",
                                        "enum": ["sqrt2"],
                                    },
                                ]
                            },
                            "rotation": {
                                "type": "integer",
                                "description": "marker rotation in degrees",
                                "minium": 0,
                                "exclusiveMaximum": 360,
                            },
                        },
                    },
                    "label": {
                        "type": "string",
                        "description": "UUID of the node's label.",
                        "maxLength": 36,
                    },
                },
                "required": ["location"],
            },
        },
        "lines": {
            "type": "object",
            "additionalProperties": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "maxLength": 50,
                    },
                    "color": colors,
                    "borderWidth": {"type": "number"},
                    "borderStyle": {
                        "type": "string",
                        "enum": [
                            "dotted",
                            "p.dashed",
                            "p.solid",
                            "p.double",
                            "p.groove",
                            "p.ridge",
                            "p.inset",
                            "p.outset",
                            "p.none",
                            "p.hidden",
                            "p.mix",
                        ],
                    },
                    "borderColor": colors,
                    "width": {"type": "number"},
                    "connections": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "nodes": {
                                    "type": "array",
                                    "items": anchor,
                                }
                            },
                        },
                    },
                },
                "required": ["symbol", "name", "color", "connections"],
            },
        },
        "labels": {
            # label objects mapped by a unique id that is randomly generated at creation
            "type": "object",
            "additionalProperties": label_basics,
        },
        "globalOffsetX": {
            "type": "number",
            "description": "Global offset for coordinates in X direction (added to x coord)",
        },
        "globalOffsetY": {
            "type": "number",
            "description": "Global offset for coordinates in Y direction (added to y coord)",
        },
        "planWidth": {
            "type": "number",
            "description": "Width of the plan (in units)",
            "minimum": 10,
        },
        "planHeight": {
            "type": "number",
            "description": "Height of the plan (in units)",
            "minimum": 10,
        },
    },
    "required": [
        "nodes",
        "lines",
        "labels",
        "planWidth",
        "planHeight",
        "globalOffsetX",
        "globalOffsetY",
    ],
    "additionalProperties": False,
}
