# coding: utf8
from functools import cmp_to_key


class TibetanSort:
    def __init__(self):
        self.trie = None

    def sort_list(self, list):
        """
        A comparison method that sorts a list using "self.compare()"
        """
        return sorted(list, key=cmp_to_key(self.compare))

    def compare(self, a, b):
        """
        A comparison function is any callable that accept two arguments, compares them,
        and returns a negative number for less-than, zero for equality, or a positive number for greater-than.
        """
        if self.trie == None:
            self._build_trie()

        a_offset = 0
        b_offset = 0
        while True:
            alm_i, alm_p, alm_s = self._get_longest_match(a, a_offset)
            blm_i, blm_p, blm_s = self._get_longest_match(b, b_offset)

            if alm_i < 1 and blm_i < 1:
                return 0

            if alm_i < 1:
                return -1

            if blm_i < 1:
                return 1

            if alm_p < blm_p:
                return -1

            if alm_p > blm_p:
                return 1

            if alm_s < blm_s:
                return -1

            if alm_s > blm_s:
                return 1

            a_offset = a_offset + alm_i
            b_offset = b_offset + blm_i

        else:
            return 0

    def _build_trie(self):
        self.trie = {}
        batches = [
            ['ཀ', 'ྈྐ', 'ཫ', 'དཀ', 'བཀ', 'རྐ', 'ལྐ', 'སྐ', 'བརྐ', 'བསྐ'],
            ['ཁ', 'ྈྑ', 'མཁ', 'འཁ'],
            ['ག', 'དགག', 'དགང', 'དགད', 'དགན', 'དགབ', 'དགཝ', 'དགའ', 'དགར', 'དགལ', 'དགས', 'དགི', 'དགུ', 'དགེ', 'དགོ',
             'དགྭ', 'དགྱ', 'དགྲ', 'བགག', 'བགང', 'བགད', 'བགབ', 'བགམ', 'བགཾ', 'བགཝ', 'བགའ', 'བགར', 'བགལ', 'བགི',
             'བགུ', 'བགེ', 'བགོ', 'བགྭ', 'བགྱ', 'བགྲ', 'བགླ', 'མགག', 'མགང', 'མགད', 'མགབ', 'མགའ', 'མགར', 'མགལ',
             'མགི', 'མགུ', 'མགེ', 'མགོ', 'མགྭ', 'མགྱ', 'མགྲ', 'འགག', 'འགང', 'འགད', 'འགན', 'འགབ', 'འགམ', 'འགཾ',
             'འགའ', 'འགར', 'འགལ', 'འགས', 'འགི', 'འགུ', 'འགེ', 'འགོ', 'འགྭ', 'འགྱ', 'འགྲ', 'རྒ', 'ལྒ', 'སྒ', 'བརྒ',
             'བསྒ'],
            ['ང', 'ྂ', 'ྃ', 'དངག', 'དངང', 'དངད', 'དངན', 'དངབ', 'དངའ', 'དངར', 'དངལ', 'དངི', 'དངུ', 'དངེ', 'དངོ', 'མངག',
             'མངང', 'མངད', 'མངན', 'མངབ', 'མངའ', 'མངར', 'མངལ', 'མངི', 'མངུ', 'མངེ', 'མངོ', 'རྔ', 'ལྔ', 'སྔ', 'བརྔ',
             'བསྔ'],
            ['ཅ', 'གཅ', 'བཅ', 'ལྕ', 'བལྕ'],
            ['ཆ', 'མཆ', 'འཆ'],
            ['ཇ', 'མཇ', 'འཇ', 'རྗ', 'ལྗ', 'བརྗ'],
            ['ཉ', 'ྋྙ', 'གཉ', 'མཉ', 'རྙ', 'ཪྙ', 'སྙ', 'བཪྙ', 'བརྙ', 'བསྙ'],
            ['ཏ', 'ཊ', 'ཏྭ', 'ཏྲ', 'གཏ', 'བཏ', 'རྟ', 'ལྟ', 'སྟ', 'བརྟ', 'བལྟ', 'བསྟ'],
            ['ཐ', 'ཋ', 'མཐ', 'འཐ'],
            ['ད', 'ཌ', 'གདག', 'གདང', 'གདད', 'གདན', 'གདབ', 'གདམ', 'གདཾ', 'གདའ', 'གདར', 'གདལ', 'གདས', 'གདི', 'གདུ', 'གདེ',
             'གདོ', 'གདྭ', 'བདག', 'བདང', 'བདད', 'བདབ', 'བདམ', 'བདཾ', 'བདའ', 'བདར', 'བདལ', 'བདས', 'བདི', 'བདུ', 'བདེ',
             'བདོ', 'བདྭ', 'མདག', 'མདང', 'མདད', 'མདན', 'མདབ', 'མདའ', 'མདར', 'མདལ', 'མདས', 'མདི', 'མདུ', 'མདེ', 'མདོ',
             'མདྭ', 'འདག', 'འདང', 'འདད', 'འདན', 'འདབ', 'འདམ', 'འདཾ', 'འདཝ', 'འདའ', 'འདར', 'འདལ', 'འདས', 'འདི', 'འདུ',
             'འདེ', 'འདོ', 'འདྭ', 'འདྲ', 'རྡ', 'ལྡ', 'སྡ', 'བརྡ', 'བལྡ', 'བསྡ'],
            ['ན', 'ཎ', 'གནག', 'གནང', 'གནད', 'གནན', 'གནབ', 'གནམ', 'གནཾ', 'གནཝ', 'གནའ', 'གནར', 'གནལ', 'གནས', 'གནི', 'གནུ',
             'གནེ', 'གནོ', 'གནྭ', 'མནག', 'མནང', 'མནད', 'མནན', 'མནབ', 'མནམ', 'མནཾ', 'མནའ', 'མནར', 'མནལ', 'མནས', 'མནི',
             'མནུ', 'མནེ', 'མནོ', 'མནྭ', 'རྣ', 'སྣ', 'བརྣ', 'བསྣ'],
            ['པ', 'ྉྤ', 'དཔག', 'དཔང', 'དཔད', 'དཔབ', 'དཔའ', 'དཔར', 'དཔལ', 'དཔས', 'དཔི', 'དཔུ', 'དཔེ', 'དཔོ', 'དཔྱ',
             'དཔྲ', 'ལྤ', 'སྤ'],
            ['ཕ', 'ྉྥ', 'འཕ'],
            ['བ', 'དབག', 'དབང', 'དབད', 'དབན', 'དབབ', 'དབའ', 'དབར', 'དབལ', 'དབས', 'དབི', 'དབུ', 'དབེ', 'དབོ', 'དབྱ',
             'དབྲ', 'འབག', 'འབང', 'འབད', 'འབན', 'འབབ', 'འབམ', 'འབཾ', 'འབའ', 'འབར', 'འབལ', 'འབས', 'འབི', 'འབུ',
             'འབེ', 'འབོ', 'འབྱ', 'འབྲ', 'རྦ', 'ལྦ', 'སྦ'],
            ['མ', 'ཾ', 'དམག', 'དམང', 'དམད', 'དམན', 'དམབ', 'དམཝ', 'དམའ', 'དམར', 'དམལ', 'དམས', 'དམི', 'དམུ', 'དམེ', 'དམོ',
             'དམྭ', 'དམྱ', 'རྨ', 'སྨ'],
            ['ཙ', 'གཙ', 'བཙ', 'རྩ', 'སྩ', 'བརྩ', 'བསྩ'],
            ['ཚ', 'མཚ', 'འཚ'],
            ['ཛ', 'མཛ', 'འཛ', 'རྫ', 'བརྫ'],
            ['ཞ', 'གཞ', 'བཞ'],
            ['ཟ', 'གཟ', 'བཟ'],
            ['ཞ', 'གཞ', 'བཞ'],
            ['ཡ', 'གཡ'],
            ['ར', 'ཪ', 'ཬ', 'བརླ', 'བཪླ'],
            ['ཤ', 'ཥ', 'གཤ', 'བཤ'],
            ['ས', 'གསག', 'གསང', 'གསད', 'གསན', 'གསབ', 'གསའ', 'གསར', 'གསལ', 'གསས', 'གསི', 'གསུ', 'གསེ', 'གསོ', 'གསྭ',
             'བསག', 'བསང', 'བསད', 'བསབ', 'བསམ', 'བསཾ', 'བསའ', 'བསར', 'བསལ', 'བསས', 'བསི', 'བསུ', 'བསེ', 'བསོ',
             'བསྭ', 'བསྲ', 'བསླ'],
            ['ཧ', 'ལྷ'],
            ['ཱ', 'ི', 'ཱི', 'ྀ', 'ཱྀ', 'ུ', 'ཱུ', 'ེ', 'ཻ', 'ོ', 'ཽ'],
            ['།', '༎', '༏', '༐', '༑', '༔', '༴', '\u0F0B']
        ]
        for b in batches:
            self._add_batch(b)

        i, p, s = self._get_longest_match('\u0F0B', 0)
        self._add_to_trie(p, s, '\u0F0C')

    def _add_to_trie(self, p, s, string):
        current = self.trie
        for i in range(len(string)):
            c = string[i]
            if current.get(c) == None:
                current[c] = {}
                current = current[c]
            else:
                current = current[c]

        current["p"] = p
        current["s"] = s

    def _add_batch(self, a: list):
        primary = ord(a[0][0])
        for index in range(len(a)):
            self._add_to_trie(primary, index, a[index])

    def _get_longest_match(self, string, off):
        current = self.trie
        save_nb_chars = 0
        save_primary = 0
        save_secondary = 0
        for i in range(off, len(string)):
            cur_char = string[i]
            if current.get(cur_char) != None:
                current = current[cur_char]
                if current.get("p") != None :
                    save_nb_chars = save_nb_chars + 1
                    save_primary = current.get("p")
                    save_secondary = current.get("s")
                elif save_primary == 0:
                    save_primary = ord(string[i])
                    save_nb_chars = 1
            else:
                if save_nb_chars == 0:
                    return 1, ord(string[i]), 0

                return save_nb_chars, save_primary, save_secondary

        return save_nb_chars, save_primary, save_secondary
