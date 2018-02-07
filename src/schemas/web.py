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

course_theme_create_post = {
    'name': fields.Str(required=True),
}

course_number_create_post = {
    'number': fields.Integer(required=True),
    'subjects[]': fields.List(fields.Str(required=True), required=True)
}

course_group_create_post = {
    'gid': fields.Str(required=True),
}

class_schedule_show_post = {
    'gid': fields.Str(required=True),
}

class_schedule_edit_post = {
    'mon[1]': fields.List(
        fields.Nested({
            'class': fields.Str(),
            'asd': fields.Str()
        }),
    ),
}

alert_post = {
    'gid': fields.Str(),
    'msg': fields.Str(required=True)
}
