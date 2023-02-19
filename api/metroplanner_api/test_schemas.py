import schemas
from jsonschema import validate, ValidationError

valid_hours = [{
    "from": 10000,
    "to": 10000,
    "description": ""
}]

valid = [
    {
        "year": 2020,
        "month": 1,
        "day": 1,
        "hours": valid_hours
    },
    {
        "year": 2023,
        "month": 10,
        "day": 31,
        "hours": valid_hours
    },
]

invalid = [
    {
        "year": 2020,
        "month": 1,
        "hours": valid_hours
    },
    {
        "year": 2020,
        "month": "1",
        "day": 1,
        "hours": valid_hours
    },
    {
        "year": 2020,
        "month": 1,
        "day": 1,
        "hours": {}
    },
    {
        "year": 2019,
        "month": 1,
        "day": 1,
        "hours": valid_hours
    },
    {
        "year": 2020,
        "month": 0,
        "day": 1,
        "hours": valid_hours
    },
    {
        "year": 2020,
        "month": 1,
        "day": 1,
        "hours": valid_hours,
        "blabliblu": 123
    },
    {
        "year": 2020,
        "month": 0,
        "day": 1,
    },
    {},
]

for x in valid:
    # print(x)
    validate(schema=schemas.patch_request_schema, instance=x)

for x in invalid:
    # print(x)
    try:
        validate(schema=schemas.patch_request_schema, instance=x)
        assert False, x
    except ValidationError as e:
        # print("X:", x, e)
        pass  # print(x, e)

print("Schemas work!")
