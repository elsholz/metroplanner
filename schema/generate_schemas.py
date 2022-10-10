#!/usr/bin/python3
from json import dumps


def schema_color_themes():
    schema = {
        "$jsonSchema": {
            "bsonType": "object",
            "description": "Document describing a metro plan",
            "properties": {
                "themeName": {
                    "type": "string",
                    "description": "Display name of the color theme.",
                },
                "public": {
                    "type": "boolean",
                    "description": "Whether this color theme is public and can be forked.",
                },
                "forkedFrom": {
                    "type": "objectId",
                    "description": "ID of the color theme this one has been forked from",
                },
                "ownedBy": {
                    "type": "string",
                    "description": "User who owns this colortheme. Empty if available by default",
                },
                "themeData": {
                    "type": "object",
                    "properties": {
                        "backgroundColor": {"type": "string"},
                        "fontColor": {"type": "string"},
                        "lineColors": {
                            "type": "array",
                            "items": {
                                "type": "string",
                            },
                        },
                        "landscape": {
                            "type": "object",
                            "properties": {
                                "river": {"type": "string"},
                                "border": {"type": "string"},
                            },
                        },
                    },
                },
            },
            "required": ["themeName", "public", "ownedBy", "themeData"],
        }
    }

    with open("colorThemes.schema.jsonc", "w") as fout:
        fout.write(dumps(schema, indent=4, ensure_ascii=False))


def schema_plans():
    schema = {
        "$jsonSchema": {
            "bsonType": "object",
            "description": "Document describing a metro plan",
            "properties": {
                "forkedFrom": {
                    "type": "string",
                    "description": "Public link of the plan this one has been forked from.",
                },
                "ownedBy": {
                    "type": "string",
                    "description": "User who owns this plan.",
                },
                "planName": {
                    "type": "string",
                    "description": "Display name of this plan.",
                },
                "colorTheme": {
                    "type": "string",
                    "description": "ID of the plans color theme.",
                },
                "history": {
                    "type": "array",
                    "items": {
                        "type": "objectId",
                        "description": "The states of this plan in history. First item is the latest state.",
                    },
                },
            },
            "required": ["planName", "colorTheme", "history"],
        }
    }

    with open("plans.schema.jsonc", "w") as fout:
        fout.write(dumps(schema, indent=4, ensure_ascii=False))


def schema_plan_history_state():
    styling = {"type": "object", "properties": {"fontSize": {"type": "number"}}}

    point = {
        "type": "array",
        "items": {"type": "number"},
        "minItems": 2,
        "maxItems": 2,
    }

    anchor = {
        "type": "object",
        "properties": {
            "node": {"oneOf": [point, {"type": "string"}]},
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

    schema = {
        "$jsonSchema": {
            "bsonType": "object",
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
                                    "width": {"type": "number"},
                                    "height": {"type": "number"},
                                    "sizeFactor": {
                                        "oneOf": [
                                            {"type": "number"},
                                            {"type": "string", "enum": ["sqrt2"]},
                                        ]
                                    },
                                    "rotation": {"type": "number"},
                                },
                            },
                            "label": label_basics,
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
                "additionalLabels": {
                    # label objects mapped by a unique id that is randomly generated at creation
                    "type": "object",
                    "additionalProperties": label_basics,
                },
            },
            "required": ["nodes", "lines", "additionalLabels"],
        }
    }

    with open("plan_states.schema.jsonc", "w") as fout:
        fout.write(dumps(schema, indent=4, ensure_ascii=False))


def schema_links():
    """
    For each plan, a publicly sharable shortlink ist created
    that consists of 12 random characters. This shortlink
    is inactive by default. When activated, a shortlink allows
    any user to view a plan, it is thereby publicly shared.

    Plans cannot be accessed directly, only via a share-link.
    Only the edit URL includes the plan OID, but this page
    includes user-authorization.
    """
    schema = {
        "$jsonSchema": {
            "bsonType": "object",
            "description": "Document describing a metro plan",
            "properties": {
                "_id": {
                    "type": "string",
                    "description": "Shortlink",
                },
                "plan": {
                    "type": "objectId",
                    "description": "OID of the plan the link is for",
                },
                "active": {
                    "type": "boolean",
                    "description": "Whether link is active or inactive",
                },
            },
            "required": ["_id", "plan", "active"],
        }
    }
    with open("links.schema.jsonc", "w") as fout:
        fout.write(dumps(schema, indent=4, ensure_ascii=False))


def schema_stats():
    schema = {
        "$jsonSchema": {
            "bsonType": "object",
            "description": "Document describing a metro plan",
            "properties": {
                "_id": {
                    "type": "object",
                    "properties": {
                        "plan": {
                            "type": "objectId",
                            "description": "OID of the plan accessed",
                        },
                        "link": {
                            "type": "string",
                            "description": "Link that's been used to access the plan",
                        },
                    },
                    "required": ["plan", "link"],
                },
                "views": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "description": "Datetime when plan was accessed, in ISO format",
                    },
                    "required": ["at"],
                },
            },
        },
        "required": [
            "_id",
            "views",
        ],
    }
    with open("stats.schema.jsonc", "w") as fout:
        fout.write(dumps(schema, indent=4, ensure_ascii=False))


schema_color_themes()
schema_plans()
schema_plan_history_state()
schema_links()
schema_stats()
