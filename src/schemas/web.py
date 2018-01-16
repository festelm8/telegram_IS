from webargs import fields

login_post = {
    'email': fields.Str(required=True),
    'password': fields.Str(required=True)
}
