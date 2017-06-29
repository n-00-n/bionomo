# encoding: utf8
import base64
import os
# ok this is gonna be bat-shit crazy move.
# but i'm gonna try to override get_translation from flask-babel
# I feel this is causing my code to fail to parse uft-8 text on .py files.
# let's see
import urllib
from urlparse import urlparse
from datetime import datetime

import traceback
from flask import Response
from flask import flash, jsonify
from flask import g
from flask import redirect
from flask import request, abort, send_from_directory

from bionomo_pilot.models import Collection
from hack import render_template
from forms import *

from constants import Constants as c
from biocase.constants import Constants as b_c
from bionomo_pilot.service.bionomo_service import BioNoMoService
from . import Components

app = Components.app
babel = Components.babel

_multimedia_dir = app.config['MULTIMEDIA_DIR']
_multimedia_endpoint = app.config['MULTIMEDIA_ENDPOINT']


@app.route('/')
@app.route('/<lang_code>')
@app.route('/<lang_code>/')
def index():
    # raise Exception()
    form = MainSearch(request.form)
    return render_template('landing_page.html', _fields=b_c, form=form)


@app.route('/async/scientific_name')
@app.route('/async/scientific_name/')
@app.route('/async/scientific_name/<scientific_name>/<lang>')
def get_scientific_name(scientific_name=None, lang=None):
    if not scientific_name:
        return jsonify([])

    _locale = None
    if not lang:
        _locale = c.DEFAULT_LOCALE
    else:
        _locale = lang if lang in c.LOCALE_DICT.keys() else c.DEFAULT_LOCALE

    service = BioNoMoService()
    collection_list = service.get_collections_by_scientific_name_with_limit(scientific_name, limit=5)

    _collection_dict_list = [
            {'scientific_name': collection.full_scientific_name,
             'url': '/' + _locale + url_for('view_results', **{'flag': c.form_flags["simple_search"],
                                               b_c.name_full_scientific_name_string: collection.full_scientific_name}
                            )
             }
            for collection in collection_list
        ]

    return jsonify(_collection_dict_list)


@app.route('/view_results', methods=['GET', 'POST'])
@app.route('/<lang_code>/view_results', methods=['GET', 'POST'])
@app.route('/<lang_code>/view_results/', methods=['GET', 'POST'])
def view_results():
    """An endpoint that processes form submissions"""
    # if its post
    # else if its get
    # ----------- prevent sql-injection: prevented by default by flask-sqlalchemy
    # put values back on the form

    service = BioNoMoService()
    form = SearchForm(request.args)
    if request.method == 'GET':
        if form.flag.data:
            if not form.validate():
                print 'flag attribute has invalid values. check it out.'
                print form.flag.errors
                abort(404)
            else:
                if form.flag.data == c.form_flags['simple_search']:
                    form = MainSearch(request.args)
                    # filter_form = FilterForm(request.args)
                    if form.validate():

                        _page = request.args.get(c.page_name, None)
                        if _page and not _page.isdigit():
                            abort(404)

                        _page = int(_page) if _page and _page.isdigit() else None

                        _scientific_name = form.data.get(b_c.name_full_scientific_name_string, None)

                        _result_dict = service.get_collections_by_scientific_name(_scientific_name, page=_page)
                        if not _result_dict or (_result_dict and _result_dict['collections'].total == 0):
                            flash(gettext('não foram encontradas coleções para a procurar: \'%(search_input)s\'',
                                          search_input=_scientific_name), 'info')
                            return redirect(redirect_url())

                        _result_dict['csv_url'] = csv_url()
                        _result_dict['page_url'] = page_url

                        _filter_form = FilterSearch(request.args, _results_dict=_result_dict)
                        return render_template('search_results.html', result=_result_dict, form=form,
                                               filter_form=_filter_form)
                    else:
                        for field_errors in form.get_errors().values():
                            for field_error in field_errors:
                                flash(gettext(field_error), 'error-main')
                        return redirect(redirect_url())

                elif form.flag.data == c.form_flags['advanced_search']:
                    form = AdvancedSearch(request.args)
                    # filter_form = FilterForm(request.args)
                    if form.validate():

                        _page = request.args.get(c.page_name, None)
                        if _page and not _page.isdigit():
                            abort(404)

                        _page = int(_page) if _page and _page.isdigit() else None

                        _scientific_name = form.data.get(b_c.name_full_scientific_name_string, None)
                        _province_list = request.args.getlist(b_c.name_province)
                        _start_date = form.data.get(b_c.name_last_date_start, None)
                        _end_date = form.data.get(b_c.name_last_date_end, None)

                        _start_latitude = form.data.get(b_c.name_latitude_decimal_start, None)
                        _end_latitude = form.data.get(b_c.name_latitude_decimal_end, None)

                        _start_longitude = form.data.get(b_c.name_longitude_decimal_start, None)
                        _end_longitude = form.data.get(b_c.name_longitude_decimal_end, None)

                        _result_dict = service.get_collections_by_fields(scientific_name=_scientific_name,
                                                                         province_list=_province_list,
                                                                         start_latitude=_start_latitude,
                                                                         end_latitude=_end_latitude,
                                                                         start_longitude=_start_longitude,
                                                                         end_longitude=_end_longitude,
                                                                         start_date=_start_date,
                                                                         end_date=_end_date,
                                                                         page=_page
                                                                         )

                        if not _result_dict or (_result_dict and _result_dict['collections'].total == 0):
                            flash(gettext('nao foram encontradas coleçoes para o seu criterio de procura!'),
                                  'info-advanced')
                            return redirect(redirect_url())

                        _result_dict['csv_url'] = csv_url()
                        _result_dict['page_url'] = page_url

                        _filter_form = FilterSearch(request.args, _results_dict=_result_dict)
                        return render_template('search_results.html', result=_result_dict, form=form,
                                               filter_form=_filter_form)
                    else:
                        for label, field_errors in form.get_errors().items():
                            for field_error in field_errors:
                                flash((gettext(label) + ': ' + gettext(field_error)), 'error-advanced')
                        return redirect(redirect_url())

                elif form.flag.data == c.form_flags['side_filter']:
                    form = FilterSearch(request.args)
                    if form.validate():
                        _page = request.args.get(c.page_name, None)
                        if _page and not _page.isdigit():
                            abort(404)

                        _page = int(_page) if _page and _page.isdigit() else None

                        _scientific_name = form.data.get(b_c.name_full_scientific_name_string, None)
                        _start_date = form.data.get(b_c.name_last_date_start, None)
                        _end_date = form.data.get(b_c.name_last_date_end, None)

                        _start_latitude = form.data.get(b_c.name_latitude_decimal_start, None)
                        _end_latitude = form.data.get(b_c.name_latitude_decimal_end, None)

                        _start_longitude = form.data.get(b_c.name_longitude_decimal_start, None)
                        _end_longitude = form.data.get(b_c.name_longitude_decimal_end, None)

                        _provider_list = request.args.getlist(b_c.name_provider)
                        _province_list = request.args.getlist(b_c.name_province)

                        if service.is_valid_provider_id_list(_provider_list) and service.is_valid_province_list(
                                _province_list):
                            _result_dict = service.get_collections_by_fields(scientific_name=_scientific_name,
                                                                             provider_id_list=_provider_list,
                                                                             province_list=_province_list,
                                                                             start_latitude=_start_latitude,
                                                                             end_latitude=_end_latitude,
                                                                             start_longitude=_start_longitude,
                                                                             end_longitude=_end_longitude,
                                                                             start_date=_start_date,
                                                                             end_date=_end_date,
                                                                             page=_page
                                                                             )

                            if not _result_dict or (_result_dict and _result_dict['collections'].total == 0):
                                flash(gettext('nao foram encontradas coleçoes para o seu criterio de procura!'),
                                      'info-filter')
                                return redirect(redirect_url())

                            _result_dict['csv_url'] = csv_url()
                            _result_dict['page_url'] = page_url

                            _filter_form = FilterSearch(request.args, _results_dict=_result_dict)
                            return render_template('search_results.html', result=_result_dict, form=form,
                                                   filter_form=_filter_form)

                        else:
                            flash(gettext('Parâmetros inválidos.'), 'error-filter')
                            return redirect(redirect_url())
                    else:
                        for label, field_errors in form.get_errors().items():
                            for field_error in field_errors:
                                flash((gettext(label) + ': ' + gettext(field_error)), 'error-filter')
                        return redirect(redirect_url())
                else:
                    abort(404)
                    # print 'invalid flag!'
        else:
            abort(404)
            # print 'attribute flag not found.'

    return render_template('landing_page.html')


@app.route('/download_csv', methods=['GET'])
@app.route('/<lang_code>/download_csv', methods=['GET'])
@app.route('/<lang_code>/download_csv/', methods=['GET'])
def download_csv():
    """An endpoint that processes form submissions"""
    # if its post
    # else if its get
    # ----------- prevent sql-injection: prevented by default by flask-sqlalchemy
    # put values back on the form

    service = BioNoMoService()
    form = SearchForm(request.args)
    if request.method == 'GET':
        if form.flag.data:
            if not form.validate():
                abort(404)
            else:
                if form.flag.data == c.form_flags['simple_search']:
                    form = MainSearch(request.args)
                    # filter_form = FilterForm(request.args)
                    if form.validate():

                        _page = request.args.get(c.page_name, None)
                        if _page and not _page.isdigit():
                            abort(404)

                        _scientific_name = form.data.get(b_c.name_full_scientific_name_string, None)

                        _csv_content = service.get_csv_for_fields(scientific_name=_scientific_name)

                        _file_name = '_'.join(
                            [gettext('dados_bionomo'), datetime.utcnow().strftime(c.file_date_format)])
                        response = Response(_csv_content.getvalue(),
                                            mimetype="text/csv",
                                            headers={
                                                "Content-disposition": "attachment; filename={}.csv".format(_file_name)}
                                            )

                        return response
                    else:
                        abort(404)

                elif form.flag.data == c.form_flags['advanced_search']:
                    form = AdvancedSearch(request.args)
                    # filter_form = FilterForm(request.args)
                    if form.validate():

                        _page = request.args.get(c.page_name, None)
                        if _page and not _page.isdigit():
                            abort(404)

                        _page = int(_page) if _page and _page.isdigit() else None

                        _scientific_name = form.data.get(b_c.name_full_scientific_name_string, None)
                        _province_list = request.args.getlist(b_c.name_province)
                        _start_date = form.data.get(b_c.name_last_date_start, None)
                        _end_date = form.data.get(b_c.name_last_date_end, None)

                        _start_latitude = form.data.get(b_c.name_latitude_decimal_start, None)
                        _end_latitude = form.data.get(b_c.name_latitude_decimal_end, None)

                        _start_longitude = form.data.get(b_c.name_longitude_decimal_start, None)
                        _end_longitude = form.data.get(b_c.name_longitude_decimal_end, None)

                        _csv_content = service.get_csv_for_fields(scientific_name=_scientific_name,
                                                                  province_list=_province_list,
                                                                  start_latitude=_start_latitude,
                                                                  end_latitude=_end_latitude,
                                                                  start_longitude=_start_longitude,
                                                                  end_longitude=_end_longitude,
                                                                  start_date=_start_date,
                                                                  end_date=_end_date
                                                                  )

                        _file_name = '_'.join(
                            [gettext('dados_bionomo'), datetime.utcnow().strftime(c.file_date_format)])
                        response = Response(_csv_content.getvalue(),
                                            mimetype="text/csv",
                                            headers={
                                                "Content-disposition": "attachment; filename={}.csv".format(_file_name)}
                                            )

                        return response
                    else:
                        abort(404)

                elif form.flag.data == c.form_flags['side_filter']:
                    form = FilterSearch(request.args)
                    if form.validate():
                        _page = request.args.get(c.page_name, None)
                        if _page and not _page.isdigit():
                            abort(404)

                        _page = int(_page) if _page and _page.isdigit() else None

                        _scientific_name = form.data.get(b_c.name_full_scientific_name_string, None)
                        _province_list = request.args.getlist(b_c.name_province)
                        _start_date = form.data.get(b_c.name_last_date_start, None)
                        _end_date = form.data.get(b_c.name_last_date_end, None)

                        _start_latitude = form.data.get(b_c.name_latitude_decimal_start, None)
                        _end_latitude = form.data.get(b_c.name_latitude_decimal_end, None)

                        _start_longitude = form.data.get(b_c.name_longitude_decimal_start, None)
                        _end_longitude = form.data.get(b_c.name_longitude_decimal_end, None)

                        _provider_list = request.args.getlist(b_c.name_provider)
                        _province_list = request.args.getlist(b_c.name_province)

                        if service.is_valid_provider_id_list(_provider_list) and service.is_valid_province_list(
                                _province_list):

                            _csv_content = service.get_csv_for_fields(scientific_name=_scientific_name,
                                                                      provider_id_list=_provider_list,
                                                                      province_list=_province_list,
                                                                      start_latitude=_start_latitude,
                                                                      end_latitude=_end_latitude,
                                                                      start_longitude=_start_longitude,
                                                                      end_longitude=_end_longitude,
                                                                      start_date=_start_date,
                                                                      end_date=_end_date,
                                                                      )

                            if not _csv_content:
                                abort(404)

                            _file_name = '_'.join(
                                [gettext('dados_bionomo'), datetime.utcnow().strftime(c.file_date_format)])
                            response = Response(_csv_content.getvalue(),
                                                mimetype="text/csv",
                                                headers={
                                                    "Content-disposition": "attachment; filename={}.csv".format(
                                                        _file_name)}
                                                )

                            return response

                        else:
                            abort(404)

                    else:
                        abort(404)
                else:
                    abort(404)
        else:
            abort(404)

    return abort(404)


@app.route('/favicon')
@app.route('/favicon/')
@app.route('/favicon.ico')
@app.route('/favicon.ico/')
def server_favicon():
    return send_from_directory(_multimedia_dir, 'favicon.ico')


@app.route(_multimedia_endpoint + '/<base64_multimedia_id>')
@app.route(_multimedia_endpoint + '/<base64_multimedia_id>/<base64_multimedia_type>')
def serve_multimedia(base64_multimedia_id, base64_multimedia_type=None):
    """An endpoint for serving multimedia files.

    :param base64_multimedia_id: the base64 encoded multimedia_id: -1 - for no media, multimedia_id - fro the id on DB
    :param base64_multimedia_type: the base64 encoded image_type code: 1 - thumbnail, 2 - medium, 3 - big
                                                                        4 - logo, 5 - flag
                                                                     None - for all other types of multimedia
    :return:
    """
    # img_type
    _serve_image = True
    multimedia_id = None
    multimedia_type = None
    service = BioNoMoService()

    try:
        multimedia_id = base64.b64decode(base64_multimedia_id)
        if base64_multimedia_type:
            multimedia_type = base64.b64decode(base64_multimedia_type)
    except TypeError:
        _serve_image = False
        print 'failed to decode input. will assume no multimedia. will return no_image.jpg'

    # if there's no problems with the parameter
    if _serve_image:
        try:
            multimedia_id = int(multimedia_id)
            if multimedia_type:
                multimedia_type = int(multimedia_type)
        except ValueError:
            _serve_image = False
            print 'failed to decode input. will assume no multimedia. will return no_image.jpg'

    if not _serve_image or (multimedia_type and multimedia_type not in c.IMG_CODES):
        # return the default no-img image
        return send_from_directory(_multimedia_dir, c.no_img_full_name)
    else:
        # multimedia_id = -1 is an indication that should load the
        # default image (bionomo_logo) on the right size (multimedia_type)
        if multimedia_id == -1:
            img_name = '_'.join([str(multimedia_type), c.img_default])
            return send_from_directory(_multimedia_dir, img_name)
        else:
            # load the multimedia from the database;
            # should contain (name, collection_id, provider_id, order)
            multimedia = service.load_multimedia_by_id(multimedia_id)

            if not multimedia:
                return send_from_directory(_multimedia_dir, c.no_img_full_name)

            _image_name = '_'.join([str(multimedia_type), str(multimedia_id), multimedia.full_name])
            _image_path = os.path.sep.join([_multimedia_dir, _image_name])

            if not os.path.exists(_image_path):
                print 'image not found: ' + _image_path
                return send_from_directory(_multimedia_dir, c.no_img_full_name)

            return send_from_directory(_multimedia_dir, _image_name)


@babel.localeselector
def get_locale():
    # _default_locale = app.config['BABEL_DEFAULT_LOCALE']
    _default_locale = request.accept_languages.best_match(app.config['SUPPORTED_LANGUAGES'].keys())
    # get from request_path
    if len(request.path) > 3:
        lang_block = request.path[:4]
        if lang_block in app.config['SUPPORTED_LANGUAGES_PATH']:
            _default_locale = lang_block[1:3]

    _lang_code = g.get('lang_code', _default_locale)
    _lang_code = _lang_code if _lang_code in app.config['SUPPORTED_LANGUAGES'].keys() else _default_locale
    return _lang_code
    # return request.accept_languages.best_match(app.config['SUPPORTED_LANGUAGES'].keys())


@babel.timezoneselector
def get_timezone():
    user = g.get('user', None)
    if user is not None:
        return user.timezone


@app.url_defaults
def set_language_code(endpoint, values):
    if 'lang_code' in values or not g.get('lang_code', None):
        return
    if app.url_map.is_endpoint_expecting(endpoint, 'lang_code'):
        values['lang_code'] = g.lang_code


@app.url_value_preprocessor
def get_lang_code(endpoint, values):
    if values is not None:
        g.lang_code = values.pop('lang_code', None)


@app.before_request
def ensure_lang_support():
    lang_code = g.get('lang_code', None)
    if lang_code and lang_code not in app.config['SUPPORTED_LANGUAGES'].keys():
        abort(404)


@app.context_processor
def inject_form_names():
    return dict(_form_names=b_c)


@app.context_processor
def inject_portal_data():
    service = BioNoMoService()
    _data = service.get_portal_data(),
    return dict(_data=_data)


@app.context_processor
def inject_updated_locale_urls():
    # todo: implement this properly.
    _request_url = ''

    if len(request.full_path) > 6:
        _args = []
        for arg, arg_v in request.args.items():
            # _args.append((arg, arg_v))
            _args.append((unicode(arg).encode('utf-8'), unicode(arg_v).encode('utf-8')))
        _request_url = urllib.urlencode(_args)
        if request.path[:4] in app.config['SUPPORTED_LANGUAGES_PATH']:
            _request_url = request.path[3:] + '?' + _request_url
        else:
            _request_url = request.path + '?' + _request_url

    langs = {
        'pt': '/pt' + _request_url,
        'en': '/en' + _request_url,
        'it': '/it' + _request_url,
        'fr': '/fr' + _request_url,
    }
    return dict(_langs=langs)


@app.context_processor
def inject_selected_locale():
    _default_locale = request.accept_languages.best_match(app.config['SUPPORTED_LANGUAGES'].keys())
    # get from request_path
    if len(request.path) > 3:
        lang_block = request.path[:4]
        if lang_block in app.config['SUPPORTED_LANGUAGES_PATH']:
            _default_locale = lang_block[1:3]

    lang_code = g.get('lang_code', _default_locale)
    lang_code = lang_code if lang_code else _default_locale
    #validate one more time the lang_code... ufff

    lang_code = lang_code if lang_code in app.config['SUPPORTED_LANGUAGES'].keys() else _default_locale

    return dict(selected_locale=lang_code)


@app.context_processor
def inject_forms():
    simple_search_form = MainSearch(request.form)
    advanced_search_form = AdvancedSearch(request.form)

    forms = {
        'simple': simple_search_form,
        'advanced': advanced_search_form,
    }

    lang_code = g.get('lang_code', app.config['BABEL_DEFAULT_LOCALE'])
    lang_code = lang_code if lang_code else app.config['BABEL_DEFAULT_LOCALE']
    return dict(forms=forms)


@app.errorhandler(404)
def page_not_found(e):
    lang_code = g.get('lang_code', app.config['BABEL_DEFAULT_LOCALE'])
    return render_template('404.html'), 404


@app.errorhandler(503)
def service_not_found(e):
    return render_template('503.html'), 503


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('503.html'), 500


@app.errorhandler(Exception)
def all_exception_handler(e):
    app.logger.exception(e)
    return render_template('503.html')
