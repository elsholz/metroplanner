hours_schema = {
    "type": "object",
    "properties": {
        "from": {
            "type": "integer",
            "description": "Timestamp in seconds when time slot starts",
            "minimum": 0,
            "maximum": 86399,
        },
        "to": {
            "type": "integer",
            "description": "Timestamp in seconds when time slot ends",
            "minimum": 1,
            "maximum": 86400,
        },
        "description": {
            "type": "string",
            "description": "Description for this time slow",
            "maxLength": 255,
            "pattern": "^[a-zA-Z0-9 -_.;]{0,255}$"
        }
    },
    "additionalProperties": False,
    "required": [
        "from",
        "to",
        "description"
    ]
}


# // Schema for Mongo DB collection `userdata` in database `just-in-time`.
db_schema = {
    "type": "object",
    "description": "Collection to save work hours for a user",
    "properties": {
            "_id": {
                "type": "string",
                "description": "ID of the user whose work hours are saved in this document"
            },
        "hours": {
                "description": "First Layer: Year",
                "type": "object",
                "additionalProperties": {
                    "description": "Second Layer: Month",
                    "type": "object",
                    "additionalProperties": {
                        "description": "Third Layer: Day",
                        "type": "object",
                        "additionalProperties": {
                            "type": "array",
                            "description": "List of time slots for this day",
                            "items": hours_schema
                        }
                    }
                }
        },
        "layout": {
                "type": "object",
                "properties": {
                    "integererval": {
                        "type": "integer",
                        "description": "integererval in minutes in which start and end times can be moved",
                        "enum": [
                            15  # // currently only 15 minute integerervals are allowed
                        ]
                    },
                    "theme": {
                        "type": "string",
                        "description": "Color Theme"
                    },
                    "from": {
                        "type": "integer",
                        "description": ""
                    },
                    "to": {
                        "type": "integer",
                        "description": ""
                    }
                },
                "additionalProperties": False
        }
    },
    "required": [
        "hours"
    ],
    "additionalProperties": False
}

patch_request_schema = {
    "type": "object",
    "properties": {
        "year": {
            "type": "integer",
            "minimum": 2020,
            "maximum": 2030,
        },
        "month": {
            "type": "integer",
            "minimum": 1,
            "maximum": 12,
        },
        "day": {
            "type": "integer",
            "minimum": 1,
            "maximum": 31,
        },
        "hours": {
            "type": "array",
            "description": "List of time slots for this day",
            "items": hours_schema
        }
    },
    "required": [
        "year",
        "month",
        "day",
        "hours",
    ],
    "additionalProperties": False
}
