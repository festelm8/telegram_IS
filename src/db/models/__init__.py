"""models init."""
import inspect
from flask_sqlalchemy import Model

from .user import User
from .teacher import Teacher
from .subject import Subject
from .event_log import EventLog
from .course_theme import CourseTheme
from .course_number import CourseNumber
from .course_group import CourseGroup
from .class_schedule import ClassSchedule
from .m2m import (
    course_number_subjects,
)


ALL_MODELS = {x.__name__: x for x in locals().values()
              if inspect.isclass(x) and
              issubclass(x, Model) and
              x != Model}