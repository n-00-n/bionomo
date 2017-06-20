# encoding: utf-8
import urllib

from flask import g
from flask import request
from flask import url_for
from wtforms import Form, HiddenField, DecimalField, SelectField, DateField
from wtforms import validators

from bionomo_pilot.service.bionomo_service import BioNoMoService
from hack import gettext, StringField, LessThan, GreaterThan

from constants import Constants as c
from biocase.constants import Constants as b_c

service = BioNoMoService()


def get_locale():
    return g.get('lang_code', c.DEFAULT_LOCALE)


def page_url(page=None):
    _args = []
    for _arg in request.args.keys():
        for value in request.args.getlist(_arg):
            if _arg != c.page_name:
                _args.append((_arg, value))
    # request.args
    # return url_for('view_results', **_args)
    _args.append((c.page_name, page if page else 1))
    return '/view_results?' + urllib.urlencode(_args)


def csv_url():
    return url_for('download_csv', **request.args)


def redirect_url():
    return request.args.get('next') or \
           request.referrer or \
           url_for('index')


class SearchForm(Form):
    flag = HiddenField('flag', validators=[validators.any_of(message="invalid search option/form",
                                                             values=c.form_flags.values(), values_formatter=str), ]
                       )


class MainSearch(SearchForm):
    # _attributes = {
    #     "placeholder": gettext('Entre o nome cientifico de seguida <ENTER>'),
    # }
    name_field = StringField(label=gettext('Nome Científico'),
                             name=b_c.name_full_scientific_name_string,
                             validators=[
                                 validators.DataRequired(message=gettext("Por favor submeta um nome científico"))],
                             render_kw=None)

    flag = HiddenField('flag', validators=[validators.any_of(message="invalid search option/form",
                                                             values=c.form_flags.values(), values_formatter=str), ]
                       , render_kw={'value': c.form_flags['simple_search']})

    def __init__(self, *args, **kwargs):
        # creates an attribute for the form with the name.
        # now have to delete the previous name_attr

        setattr(self, b_c.name_full_scientific_name_string, self.name_field)
        self._to_remove_from = ['name_field']
        _new_unbound_fields = []

        for unbound_field in self._unbound_fields:
            if unbound_field[0][0] not in self._to_remove_from:
                _new_unbound_fields.append(unbound_field)

        _new_unbound_fields.append((b_c.name_full_scientific_name_string, self.name_field))

        self._unbound_fields = _new_unbound_fields
        # self._unbound_fields = self._unbound_fields + [[b_c.name_full_scientific_name_string, self.name_field]]
        super(SearchForm, self).__init__(*args, **kwargs)

    def field_name(self):
        return self.name_field

    def get_errors(self):
        if self.errors:
            # the most anti-pythonic line of code ever!
            return {self._fields.get(key).label.text: error_list for key, error_list in self.errors.items() if
                    key not in self._to_remove_from}


class AdvancedSearch(MainSearch):
    flag = HiddenField('flag', validators=[validators.any_of(message="invalid search option/form",
                                                             values=c.form_flags.values(), values_formatter=str), ]
                       , render_kw={'value': c.form_flags['advanced_search']})

    # validators.Optional()

    province_field = SelectField(label=gettext("Província"),
                                 choices=[(province, province) for province in service.get_provinces()],
                                 render_kw={'multiple': '', 'size': len(service.get_provinces())},
                                 validators=[validators.Optional(),])

    start_date_field = DateField(label=(gettext("Data") + ' ' + gettext("(inicio)")),
                                 format=c.date_format,
                                 render_kw={'data-language': gettext("lang"),},
                                 validators=[LessThan(b_c.name_last_date_end),
                                            validators.Optional(),])

    end_date_field = DateField(label=(gettext("Data") + ' ' + gettext("(fim)")),
                               format=c.date_format,
                               validators=[GreaterThan(b_c.name_last_date_start),
                                           validators.Optional(),])

    start_latitude_field = DecimalField(label=(gettext("Latitude") + ' (' + gettext("início") + ')'),
                                        validators=[LessThan(b_c.name_latitude_decimal_end),
                                                    validators.NumberRange(min=-180, max=180, message=gettext("permitido valores no intervalo de -180 a 180")),
                                                    validators.Optional(),])

    end_latitude_field = DecimalField(label=(gettext("Latitude") + ' (' + gettext("fim") + ')'),
                                      validators=[GreaterThan(b_c.name_latitude_decimal_start),
                                                  validators.NumberRange(min=-180, max=180, message=gettext("permitido valores no intervalo de -180 a 180")),
                                                  validators.Optional(),])

    start_longitude_field = DecimalField(label=(gettext("Longitude") + ' (' + gettext("início") + ')'),
                                         validators=[LessThan(b_c.name_longitude_decimal_end),
                                                     validators.Optional(),
                                                     validators.NumberRange(min=-180, max=180, message=gettext("permitido valores no intervalo de -180 a 180")),
                                                     validators.Optional(),])

    end_longitude_field = DecimalField(label=(gettext("Longitude") + ' (' + gettext("fim") + ')'),
                                       validators=[GreaterThan(b_c.name_longitude_decimal_start),
                                                   validators.Optional(),
                                                   validators.NumberRange(min=-180, max=180, message=gettext("permitido valores no intervalo de -180 a 180")),
                                                   validators.Optional(),])

    def __init__(self, *args, **kwargs):

        setattr(self, b_c.name_full_scientific_name_string, self.name_field)
        setattr(self, b_c.name_province, self.province_field)
        setattr(self, b_c.name_last_date_start, self.start_date_field)
        setattr(self, b_c.name_last_date_end, self.end_date_field)
        setattr(self, b_c.name_latitude_decimal_start, self.start_latitude_field)
        setattr(self, b_c.name_latitude_decimal_end, self.end_latitude_field)
        setattr(self, b_c.name_longitude_decimal_start, self.start_longitude_field)
        setattr(self, b_c.name_longitude_decimal_end, self.end_longitude_field)

        # add here to remove original, keep mines... HAH!
        self._to_remove_from = ['name_field', 'province_field', 'start_date_field', 'end_date_field',
                                'start_latitude_field', 'start_longitude_field', 'end_latitude_field',
                                'end_longitude_field']
        _new_unbound_fields = []

        for unbound_field in self._unbound_fields:
            if unbound_field[0] not in self._to_remove_from:
                _new_unbound_fields.append(unbound_field)

        # add here. to the new unbound_fields
        _new_unbound_fields.append((b_c.name_full_scientific_name_string, self.name_field))
        _new_unbound_fields.append((b_c.name_province, self.province_field))
        _new_unbound_fields.append((b_c.name_last_date_start, self.start_date_field))
        _new_unbound_fields.append((b_c.name_last_date_end, self.end_date_field))
        _new_unbound_fields.append((b_c.name_latitude_decimal_start, self.start_latitude_field))
        _new_unbound_fields.append((b_c.name_latitude_decimal_end, self.end_latitude_field))
        _new_unbound_fields.append((b_c.name_longitude_decimal_start, self.start_longitude_field))
        _new_unbound_fields.append((b_c.name_longitude_decimal_end, self.end_longitude_field))

        self._unbound_fields = _new_unbound_fields
        super(MainSearch, self).__init__(*args, **kwargs)


class FilterSearch(AdvancedSearch):
    flag = HiddenField('flag', validators=[validators.any_of(message="invalid search option/form",
                                                             values=c.form_flags.values(), values_formatter=str), ]
                       , render_kw={'value': c.form_flags['side_filter']})

    provider_field = None
    province_field = None
    if False:
        province_field = SelectField(label=gettext("Província"),
                                     # choices=[(province, province) for province in service.get_provinces()],
                                     # render_kw={'multiple': '', 'size': len(service.get_provinces())},
                                     validators=[validators.Optional(),])


    start_latitude_field = None
    end_latitude_field = None
    start_longitude_field = None
    end_longitude_field = None

    start_date_field = None
    end_date_field = None

    def __init__(self, *args, **kwargs):
        # setattr(self, b_c.name_province, self.province_field)

        _provider_choices = []
        _province_choices = []

        _latitude_start = None
        _latitude_end = None
        _longitude_start = None
        _longitude_end = None

        _date_start = None
        _date_end = None

        _results_dict = kwargs.pop('_results_dict', None)
        if _results_dict:
            _provider_choices = [(provider.id, provider.full_name) for provider in _results_dict['data_providers']]

            _province_choices = [(province, province) for province in _results_dict['provinces']]

            if _results_dict.get('filter_form_values', None):

                if _results_dict['filter_form_values'].get(b_c.name_latitude_decimal_start, None):
                    _latitude_start = _results_dict['filter_form_values'][b_c.name_latitude_decimal_start]

                if _results_dict['filter_form_values'].get(b_c.name_latitude_decimal_end, None):
                    _latitude_end = _results_dict['filter_form_values'][b_c.name_latitude_decimal_end]

                if _results_dict['filter_form_values'].get(b_c.name_latitude_decimal_start, None):
                    _longitude_start = _results_dict['filter_form_values'][b_c.name_longitude_decimal_start]

                if _results_dict['filter_form_values'].get(b_c.name_latitude_decimal_start, None):
                    _longitude_end = _results_dict['filter_form_values'][b_c.name_longitude_decimal_end]

                if _results_dict['filter_form_values'].get(b_c.name_last_date_start, None):
                    _date_start = _results_dict['filter_form_values'][b_c.name_last_date_start]

                if _results_dict['filter_form_values'].get(b_c.name_last_date_end, None):
                    _date_end = _results_dict['filter_form_values'][b_c.name_last_date_end]
        else:
            if args and args[0]:
                if args[0].getlist(b_c.name_province):
                    _province_choices = [(province, province) for province in args[0].getlist(b_c.name_province)]

                if args[0].getlist(b_c.name_provider):
                    provider_id_list = args[0].getlist(b_c.name_provider)
                    providers = service.get_providers_with_ids(provider_id_list)
                    _provider_choices = [(provider.id, provider.full_name) for provider in providers]
                else:
                    providers = service.get_providers()
                    _provider_choices = [(provider.id, provider.full_name) for provider in providers]

        self.provider_field = SelectField(label=gettext("Instituição"),
                                          choices=_provider_choices,
                                          render_kw={'multiple': '', 'size': len(_provider_choices)},
                                          default=_provider_choices, coerce=int, validators=[validators.Optional(), ])  #validators.DataRequired()

        self.province_field = SelectField(label=gettext("Província"),
                                          choices=_province_choices,
                                          render_kw={'multiple': '', 'size': len(_province_choices)},
                                          default=_province_choices, coerce=str, validators=[validators.Optional(), ])

        self.start_latitude_field = DecimalField(label=(gettext("Latitude") + ' (' + gettext("início") + ')'),
                                                 render_kw={"value": _latitude_start if _latitude_start else ''},
                                                 validators=[LessThan(b_c.name_latitude_decimal_end),
                                                             validators.NumberRange(min=-180, max=180, message=gettext(
                                                                "permitido valores no intervalo de -180 a 180")),
                                                             validators.Optional(), ])

        self.end_latitude_field = DecimalField(label=(gettext("Latitude") + ' (' + gettext("fim") + ')'),
                                               render_kw={"value": _latitude_end if _latitude_end else ''},
                                               validators=[GreaterThan(b_c.name_latitude_decimal_start),
                                                           validators.NumberRange(min=-180, max=180, message=gettext(
                                                           "permitido valores no intervalo de -180 a 180")),
                                                           validators.Optional(), ])

        self.start_longitude_field = DecimalField(label=(gettext("Longitude") + ' (' + gettext("início") + ')'),
                                                  render_kw={"value": _longitude_start if _longitude_start else ''},
                                                  validators=[LessThan(b_c.name_longitude_decimal_end),
                                                              validators.Optional(),
                                                              validators.NumberRange(min=-180, max=180, message=gettext(
                                                                  "permitido valores no intervalo de -180 a 180")),
                                                              validators.Optional(), ])

        self.end_longitude_field = DecimalField(label=(gettext("Longitude") + ' (' + gettext("fim") + ')'),
                                                render_kw={"value": _longitude_end if _longitude_end else ''},
                                                validators=[GreaterThan(b_c.name_longitude_decimal_start),
                                                       validators.Optional(),
                                                       validators.NumberRange(min=-180, max=180, message=gettext(
                                                           "permitido valores no intervalo de -180 a 180")),
                                                       validators.Optional(), ])

        self.start_date_field = DateField(label=(gettext("Data") + ' ' + gettext("(inicio)")),
                                          render_kw={"value": _date_start if _date_start else ''},
                                          format=c.date_format,
                                          validators=[LessThan(b_c.name_last_date_end),
                                                      validators.Optional(), ])

        self.end_date_field = DateField(label=(gettext("Data") + ' ' + gettext("(fim)")),
                                        render_kw={"value": _date_end if _date_end else ''},
                                        format=c.date_format,
                                        validators=[GreaterThan(b_c.name_last_date_start),
                                                    validators.Optional(), ])

        setattr(self, b_c.name_full_scientific_name_string, self.name_field)
        setattr(self, b_c.name_provider, self.provider_field)
        setattr(self, b_c.name_province, self.province_field)
        setattr(self, b_c.name_last_date_start, self.start_date_field)
        setattr(self, b_c.name_last_date_end, self.end_date_field)
        setattr(self, b_c.name_latitude_decimal_start, self.start_latitude_field)
        setattr(self, b_c.name_latitude_decimal_end, self.end_latitude_field)
        setattr(self, b_c.name_longitude_decimal_start, self.start_longitude_field)
        setattr(self, b_c.name_longitude_decimal_end, self.end_longitude_field)

        self._to_remove_from = ['name_field', 'province_field', 'provider_field', 'start_date_field', 'end_date_field',
                                'start_latitude_field', 'start_longitude_field', 'end_latitude_field',
                                'end_longitude_field']
        _new_unbound_fields = []

        for unbound_field in self._unbound_fields:
            if unbound_field[0] not in self._to_remove_from:
                _new_unbound_fields.append(unbound_field)

        # add here. to the new unbound_fields
        _new_unbound_fields.append((b_c.name_full_scientific_name_string, self.name_field))
        _new_unbound_fields.append((b_c.name_province, self.province_field))
        _new_unbound_fields.append((b_c.name_provider, self.provider_field))
        _new_unbound_fields.append((b_c.name_last_date_start, self.start_date_field))
        _new_unbound_fields.append((b_c.name_last_date_end, self.end_date_field))
        _new_unbound_fields.append((b_c.name_latitude_decimal_start, self.start_latitude_field))
        _new_unbound_fields.append((b_c.name_latitude_decimal_end, self.end_latitude_field))
        _new_unbound_fields.append((b_c.name_longitude_decimal_start, self.start_longitude_field))
        _new_unbound_fields.append((b_c.name_longitude_decimal_end, self.end_longitude_field))

        self._unbound_fields = _new_unbound_fields
        super(AdvancedSearch, self).__init__(*args, **kwargs)
