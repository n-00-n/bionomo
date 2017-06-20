# from flask import render_template
from flask_babel import _, gettext as gt
from wtforms import ValidationError


def this_gettext(string, **variables):
    try:
        return gt(string, **variables)
    except:
        # print 'failed to get text for "{}"'.format(string)
        s = unicode(string, encoding='utf-8')
        return gt(s, **variables)
        # return s if not variables else s % variables

_ = gettext = this_gettext

from wtforms import StringField


class StringField(StringField):

    def __init__(self, *args, **kwargs):
        name = kwargs.pop('name', None)
        super(StringField, self).__init__(*args, **kwargs)
        if name:
            self.id = name
            self.name = name
            self.short_name = name

    def _value(self):
        return super(StringField, self)._value()


from flask import g, render_template


class LessThan(object):
    """
    Compares the values of two fields.

    :param fieldname:
        The name of the other field to compare to.
    :param message:
        Error message to raise in case of a validation error. Can be
        interpolated with `%(other_label)s` and `%(other_name)s` to provide a
        more helpful error.
    """
    def __init__(self, fieldname, message=None):
        self.fieldname = fieldname
        self.message = message

    def __call__(self, form, field):
        try:
            other = form[self.fieldname]
        except KeyError:
            raise ValidationError(field.gettext("Invalid field name '%s'.") % self.fieldname)
        if field.data and other.data and field.data >= other.data:
            d = {
                'other_label': hasattr(other, 'label') and other.label.text or self.fieldname,
                'other_name': self.fieldname
            }
            message = self.message
            if message is None:
                message = field.gettext('O campo dever ter valor inferior ao %(other_label)s.')

            raise ValidationError(message % d)


class GreaterThan(object):
    """
    Compares the values of two fields.

    :param fieldname:
        The name of the other field to compare to.
    :param message:
        Error message to raise in case of a validation error. Can be
        interpolated with `%(other_label)s` and `%(other_name)s` to provide a
        more helpful error.
    """
    def __init__(self, fieldname, message=None):
        self.fieldname = fieldname
        self.message = message

    def __call__(self, form, field):
        try:
            other = form[self.fieldname]
        except KeyError:
            raise ValidationError(field.gettext("Invalid field name '%s'.") % self.fieldname)
        if field.data and other.data and field.data < other.data:
            d = {
                'other_label': hasattr(other, 'label') and other.label.text or self.fieldname,
                'other_name': self.fieldname
            }
            message = self.message
            if message is None:
                message = field.gettext('O campo dever ter valor superior ao %(other_label)s.')

            raise ValidationError(message % d)

