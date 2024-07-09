NEWS_TABLE_SCHEMA = {
    'author': {'type' : str, 'required': False, 'default': None},
    'title': {'type' : str, 'required': True, 'default': 'No title'},
    'description': {'type': str, 'required':True, 'default': 'No description'},
    'url' : {'type': str, 'required': True, 'default': 'No url'},
    'source': {'type': str, 'required': True, 'default': 'No Source'},
    'category': {'type':str, 'required':False, 'default': None},
    'published_at': {'type':str, 'required':True, 'default': None},
    'country': {'type':str, 'required': False, 'default': None}
}