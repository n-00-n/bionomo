# from flask import render_template
from flask_babel import _, gettext as gt
from werkzeug.utils import escape
from wtforms import ValidationError, SelectMultipleField, SelectField
from wtforms.widgets import HTMLString, Select
from wtforms.widgets import html_params
from six import string_types
# from wtforms.widgets import escape


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


class Select2MultipleField(SelectMultipleField):

    def pre_validate(self, form):
        # Prevent "not a valid choice" error
        pass

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = ",".join(valuelist)
        else:
            self.data = ""


class SelectWidget(Select):
    """
    Add support of choices with ``optgroup`` to the ``Select`` widget.
    """
    @classmethod
    def render_option(cls, value, label, mixed):
        """
        Render option as HTML tag, but not forget to wrap options into
        ``optgroup`` tag if ``label`` var is ``list`` or ``tuple``.
        """
        if isinstance(label, (list, tuple)):
            children = []

            for item_value, item_label in label:
                item_html = cls.render_option(item_value, item_label, mixed)
                children.append(item_html)

            html = u'<optgroup label="%s">%s</optgroup>'
            data = (escape(unicode(value)), u'\n'.join(children))
        else:
            coerce_func, data = mixed
            # value = value.decode('utf-8')
            func_result = str(value) if isinstance(value, string_types) else coerce_func(value)
            selected = func_result == data

            options = {'value': value}

            if selected:
                options['selected'] = u'selected'
            options['selected'] = u'selected'

            html = u'<option %s>%s</option>'
            data = (html_params(**options), escape(str(label)))

        return HTMLString(html % data)


class ThisSelectField(SelectField):
    widget = SelectWidget()

    def iter_choices(self):
        """
        We should update how choices are iter to make sure that value from
        internal list or tuple should be selected.
        """
        for value, label in self.choices:
            yield (value, label, (self.coerce, self.data))