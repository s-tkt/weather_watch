def get_description(code):
    code = int(code)
    if code in wmo_description:
        return wmo_description[code]
    elif 0 <= code <= 9:
        return '*晴れ/曇り'
    elif 4 <= code <= 9:
        return '*霞'
    elif 10 <= code <= 19:
        return '*霧'
    elif 20 <= code <= 29:
        return '*荒天'
    elif 30 <= code <= 39:
        return '*砂嵐'
    elif 40 <= code <= 49:
        return '*霧雨'
    elif 50 <= code <= 59:
        return '*霧雨'
    elif 60 <= code <= 69:
        return '*雨'
    elif 70 <= code <= 79:
        return '*雪'
    elif 80 <= code <= 99:
        return '*にわか雨'
    else:
        return '-'

wmo_description = {
    0: '快晴',
    1: 'だいたい晴れ',
    2: '曇り',
    3: 'たっぷり曇り',
    60: 'ぱらぱら',
    61: 'ず～っと小雨',
    62: '時々雨',
    63: 'ず～っと雨',
    64: '雨、時々大雨',
    65: 'ず～っと大雨',
    80: '軽くにわか雨',
    81: 'にわか雨',
    82: 'ゲリラ豪雨',
}
