from json import dumps

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
    "required": ["node"],
}

schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "description": "Document describing a mountain peak",
        "properties": {
            "planName": {"type": "string"},
            "colorTheme": {"type": "string"},
            "nodes": {
                "type": "object",
                "additionalProperties": {
                    "type": "object",
                    "properties": {
                        "location": point,
                        "marker": {
                            "type": "object",
                            "properties": {
                                "class": {"type": "string"},
                                "width": {"type": "number"},
                                "height": {"type": "number"},
                                "sizeFactor": {"type": "number"},
                                "rotation": {"type": "number"},
                            },
                            "required": ["class"],
                        },
                        "label": {
                            "type": "object",
                            "properties": {
                                "class": {
                                    "type": "string",
                                    "enum": [
                                        "center",
                                        "left_ascending",
                                        "right_ascending",
                                        "bottom_ascending",
                                        "top_ascending",
                                        "left_descending",
                                        "right_descending",
                                        "bottom_descending",
                                        "top_descending",
                                    ],
                                },
                                "text": {"type": "string"},
                                "anchor": anchor,
                                "styling": styling,
                            },
                            "required": ["class", "text"],
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
            "labels": {"type": "array", "items": {"type": "object", "properties": {}}},
        },
        "required": ["planName", "colorTheme", "nodes", "lines", "labels"],
    }
}

with open("metroplanner.schema.jsonc", "w") as fout:
    fout.write(dumps(schema, indent=4, ensure_ascii=False))
