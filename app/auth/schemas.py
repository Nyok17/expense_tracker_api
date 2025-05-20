from marshmallow import Schema, fields

class RegisterSchema(Schema):
    id = fields.Int(dump_only=True)
    username= fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True)

class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)
    