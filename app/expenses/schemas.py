from marshmallow import Schema, fields

class ExpenseSchema(Schema):
    id = fields.Int(dump_only=True)
    expense = fields.Str(required=True)
    amount = fields.Int(required=True)
    category = fields.Str(required=True)
    created_at = fields.Date(dump_only=True)
    updated_at = fields.Date(dump_only=True)