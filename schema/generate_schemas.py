#!/usr/bin/python3
from json import dumps


def schema_color_themes():
    schema = {
        "$jsonSchema": {
            "bsonType": "object",
            "description": "Document describing a color theme for a metro map.",
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
                    "bsonType": "objectId",
                    "description": "ID of the color theme this one has been forked from",
                },
                "ownedBy": {
                    "bsonType": "objectId",
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
            "description": "Document containing a metro plans basic information, excluding state info.",
            "properties": {
                "forkedFrom": {
                    "type": "string",
                    "description": "Public link of the plan this one has been forked from.",
                },
                "ownedBy": {
                    "bsonType": "objectId",
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
                "createdAt": {
                    "type": "string",
                    "description": "Datetime when this plan was first created.",
                },
                "lastModified": {
                    "type": "string",
                    "description": "Datetime when this plan was last modified",
                },
                "currentState": {
                    "bsonType": "objectId",
                    "description": "The current state that is to be displayed for this plan",
                },
                "numberOfNodes": {
                    "type": "number",
                    "description": "The number of nodes in the current state.",
                },
                "numberOfLines": {
                    "type": "number",
                    "description": "The number of lines in the current state.",
                },
                "numberOfEdges": {
                    "type": "number",
                    "description": "The number of edges between nodes in the current state.",
                },
                "likeCount": {
                    "type": "number",
                    "description": "The number of users who've liked this plan.",
                },
                "history": {
                    "type": "array",
                    "items": {
                        "bsonType": "objectId",
                        "description": "The states of this plan in history. First item is the latest state.",
                    },
                },
                "deleted": {
                    "description": "Wheter this plan has been marked for deletion. If so, the date of deletion is saved.",
                    "oneOf": [
                        {
                            "type": "bool",
                            "const": False,
                        },
                        {
                            "type": "string",
                            "description": "Datetime of the deletion.",
                        },
                    ],
                },
            },
            "required": ["planName", "colorTheme", "history", "currentState"],
        }
    }

    with open("plans.schema.jsonc", "w") as fout:
        fout.write(dumps(schema, indent=4, ensure_ascii=False))


def schema_users():
    schema = {
        "$jsonSchema": {
            "bsonType": "object",
            "description": "Document containing some user settings.",
            "properties": {
                "_id": {
                    "bsonType": "objectId",
                    "description": "ID by which this user is publicly identified. Differs from the username.",
                },
                "username": {
                    "type": "string",
                    "description": "User this profile is for. Not publicly accessible.",
                },
                "public": {
                    "type": "boolean",
                    "description": "Whether this profile will be publicly visible or hidden.",
                },
                "displayName": {
                    "type": "string",
                    "description": "If profile is public, this is the user's display name.",
                },
                "mailto": {
                    "type": "string",
                    "description": "If profile is public, email address that users can view. May be empty.",
                },
                "profileViews": {
                    "type": "number",
                    "description": "Number of views on this profile, while it was publicly accessible.",
                },
                "likesGiven": {
                    "type": "array",
                    "description": "Number of views on this profile, while it was publicly accessible.",
                    "items": {
                        "bsonType": "objectId",
                        "description": "ID of a plan that has been liked by the user.",
                    },
                },
            },
            "required": [
                "username",
            ],
        }
    }
    with open("users.schema.jsonc", "w") as fout:
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
                "createdAt": {
                    "type": "string",
                    "description": "Datetime when this plan state was created.",
                },
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
                            "label": {
                                "bsonType": "string",
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
            },
            "required": ["nodes", "lines", "labels"],
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
            "description": "Document mapping shortlinks to plan ids. Used to access plan-related data publicly (read-only).",
            "properties": {
                "_id": {
                    "type": "string",
                    "description": "Shortlink",
                },
                "plan": {
                    "bsonType": "objectId",
                    "description": "OID of the plan the link is for",
                },
                "active": {
                    "type": "boolean",
                    "description": "Whether link is active (publicly) or inactive",
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
            "description": "Document for counting map views via a specified shortlink.",
            "properties": {
                "_id": {
                    "type": "object",
                    "properties": {
                        "plan": {
                            "bsonType": "objectId",
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
                    "type": "object",
                    "additionalProperties": {
                        "type": "number",
                        "description": "View counts mapped to datetime when plan was accessed up to hour, in ISO format",
                    },
                },
            },
            "required": [
                "_id",
                "views",
            ],
        },
    }
    with open("stats.schema.jsonc", "w") as fout:
        fout.write(dumps(schema, indent=4, ensure_ascii=False))


schema_color_themes()
schema_plans()
schema_plan_history_state()
schema_links()
schema_stats()
schema_users()
