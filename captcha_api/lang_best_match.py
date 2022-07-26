
def best_locale(accept_languages) -> dict:
    locale = 'en'

    # https://en.wikipedia.org/wiki/IETF_language_tag
    ietf_language_tag = ['af', 'am', 'ar', 'arn', 'as', 'az', 'ba', 'be', 'bg', 'bn', 'bo', 'br', 'bs', 'ca', 'co', 'cs', 'cy', 'da', 'de', 'dsb', 'dv', 'el', 'en', 'es', 'et', 'eu', 'fa', 'fi', 'fil', 'fo', 'fr', 'fy', 'ga', 'gd', 'gl', 'gsw', 'gu', 'ha', 'he', 'hi', 'hr', 'hsb', 'hu', 'hy', 'id', 'ig', 'ii', 'is', 'it', 'iu', 'ja', 'ka', 'kk', 'kl', 'km', 'kn', 'ko', 'kok', 'ky', 'lb',
                        'lo', 'lt', 'lv', 'mi', 'mk', 'ml', 'mn', 'moh', 'mr', 'ms', 'mt', 'my', 'nb', 'ne', 'nl', 'nn', 'no', 'nso', 'oc', 'or', 'pa', 'pl', 'prs', 'ps', 'pt', 'quc', 'quz', 'rm', 'ro', 'ru', 'rw', 'sa', 'sah', 'se', 'si', 'sk', 'sl', 'sma', 'sq', 'sr', 'sv', 'sw', 'syr', 'ta', 'te', 'tg', 'th', 'tk', 'tn', 'tr', 'tt', 'tzm', 'ug', 'uk', 'ur', 'uz', 'vi', 'wo', 'xh', 'yo', 'zh', 'zu']

    for lang in str(accept_languages).split(','):
        if lang[:2] in ietf_language_tag:
            locale = lang[:2]
            break
    return locale
