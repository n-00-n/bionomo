# encoding: utf-8

class Constants:
    no_img_id = '-1'
    no_img_full_name = 'no_image.png'
    img_default = 'default.jpg'

    CODE_IMG_THUMBNAIL = 1    # bigger version of the image for collection item
    CODE_IMG_MEDIUM = 2    # bigger version of the image for collection item
    CODE_IMG_BIG = 3    # bigger version of the image for collection item
    CODE_IMG_LOGO = 4
    CODE_IMG_FLAG = 5   # images for the little flags

    IMG_CODES = [CODE_IMG_THUMBNAIL,
                 CODE_IMG_MEDIUM,
                 CODE_IMG_BIG,
                 CODE_IMG_LOGO,
                 CODE_IMG_FLAG,
                 ]

    form_flags = {
        'simple_search': 'ss',
        'advanced_search': 'as',
        'side_filter': 'sf',
    }

    collections_per_page = 15
    page_name = '_p'
    date_format = '%d/%m/%Y'
    general_date_format = '%Y/%m/%d'
    file_date_format = '%Y%m%d%H%M%S'
    gmaps_markers_limit = 500

    DEFAULT_LOCALE = 'pt'
    LOCALE_DICT = {'en': 'English', 'pt': 'Português', 'fr': 'Français', 'it': 'Italiano'}
