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
                    "type": "string",
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

    schema = {
        "$jsonSchema": {
            "bsonType": "object",
            "description": "Document describing a metro plan",
            "properties": {
                "public": {},
                "forkedFrom": {},
                "ownedBy": {},
                "planName": {"type": "string"},
                "colorTheme": {"type": "string", "enum": ["dark", "bright"]},
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
                        },
                        "required": ["location"],
                    },
                },
                "lines": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "symbol": {"type": "string"},
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
                    "type": "array",
                    "items": {
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
                    },
                },
            },
            "required": ["planName", "colorTheme", "nodes", "lines", "labels"],
        }
    }

    with open("plans.schema.jsonc", "w") as fout:
        fout.write(dumps(schema, indent=4, ensure_ascii=False))


def schema_links():
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
                    "type": "string",
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
                    "properies": {
                        "plan": {
                            "type": "string",
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
                        "type": "object",
                        "properties": {
                            "user": {
                                "type": "string",
                                "description": "ID of the user who viewed the plan, if logged in.",
                            },
                            "at": {
                                "type": "string",
                                "description": "Datetime when plan was accessed, in ISO format",
                            },
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
    }
    with open("stats.schema.jsonc", "w") as fout:
        fout.write(dumps(schema, indent=4, ensure_ascii=False))


schema_color_themes()
schema_plans()
schema_links()
schema_stats()
