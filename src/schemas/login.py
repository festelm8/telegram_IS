from webargs import fields

login_post = {
    'email': fields.Email(required=True),
    'password': fields.Str(required=True)
}
