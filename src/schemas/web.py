from webargs import fields

login_post = {
    'email': fields.Str(required=True),
    'password': fields.Str(required=True)
}

teacher_create_post = {
    'email': fields.Str(),
    'name': fields.Str(required=True)
}

subects_create_post = {
    'name': fields.Str(required=True),
    'desc': fields.Str(),
    'teacher_id': fields.Str(required=True)
}

