import sys
from unicodedata import category

ID_START = ''.join([
    c for c in map(chr, range(sys.maxunicode))
    if category(c) in ['Lu', 'Ll', 'Lt', 'Lm', 'Lo', 'Nl']]) + '_’'

ID_CONTINUE = (ID_START + ''.join([
    c for c in map(chr, range(sys.maxunicode))
    if category(c) in ['Mn', 'Mc', 'Nd',
                       # 'Pc'
                       ]]) + '·')


class நிரல்மொழி(object):
    def __init__(தன், பெயர், நீட்சி, மொழி):
        தன்.பெயர் = பெயர்
        தன்.நீட்சி = [நீட்சி] if isinstance(நீட்சி, str) else நீட்சி
        தன்.மொழி = மொழி

    def இலக்கணம்(தன், மொழி, புதிப்பு=None):
        if மொழி == தன்.மொழி:
            return  # Donner grammaire de base
        # lire traductions
        # avertir si pas 100% approuvée
        # générer texte grammaire

    def பெயர்_குறிப்பு(தன், புதிப்பு=None):
        id_strt = ''
        id_cont = ''
        pass
