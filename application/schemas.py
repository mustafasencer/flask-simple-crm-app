"""
    Created by Mustafa Sencer Özcan on 12.05.2020.
"""

from marshmallow import Schema, fields, ValidationError, validates_schema


class RegisterSchema(Schema):
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    email = fields.Email(required=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True)


class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)


class ResetPasswordSchema(Schema):
    new_password = fields.Str(required=True)
    new_password_repeat = fields.Str(required=True)

    @validates_schema
    def validate_passwords(self, data, **kwargs):
        if not data["new_password"] == data["new_password_repeat"]:
            raise ValidationError("new_password must be must be equal to new_password_repeat")
