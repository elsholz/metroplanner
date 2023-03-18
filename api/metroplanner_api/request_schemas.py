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
                {"type": "string", "description": "unique node identifier"},
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
        "text": {"type": "string"},
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

post_plan_schema = {
    "additionalProperties": False,
    "required": [],
}

patch_plan_schema = {
    "type": "object",
    "description": "Document containing a metro plans basic information, excluding state info.",
    "properties": {
        "planName": {
            "type": "string",
            "description": "Display name of this plan.",
            "minLength": 3,
            "maxLength": 30,
        },
        "planDescription": {
            "type": "string",
            "description": "Description of this plan.",
            "minLength": 0,
            "maxLength": 250,
        },
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
                    "name": {"type": "string"},
                    "color": {"type": "string"},
                    "borderWidth": {"type": "number"},
                    "borderStyle": {"type": "string"},
                    "borderColor": {"type": "string"},
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
