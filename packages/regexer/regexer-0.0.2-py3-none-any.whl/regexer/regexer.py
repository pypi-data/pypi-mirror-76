import re


class RegexerString(str):
    """Simplify working with regex.

    Examples:
        ::
            >>> RegexerString("Test01 string sentence02")[r"(?P<num>\\d+)", 'num']
            ['01', '02']
            >>> RegexerString("Test01 string sentence02")[r"(?P<num>\\d+)", 1, 'num']
            '02'
            >>> RegexerString("Test01 string sentence02") / r"\\w\\d{2}"
            ['Tes', ' string sentenc']
            >>> RegexerString("Test01 string sentence02") - r"\\d"
            'Test string sentence'

    Raises:
        Exception: type not supported.
        Exception: no item found by index.
    """

    def __sub__(self, other):
        if isinstance(other, str):
            return re.sub(other, "", self)
        else:
            raise Exception("Not supported!")

    def __truediv__(self, other):
        if isinstance(other, str):
            return list(filter(lambda item: item, re.split(other, self)))
        else:
            raise Exception("Not supported!")

    def __getitem__(self, index):
        if isinstance(index, str):
            return [x.groupdict() for x in re.finditer(index, self)]
        r = [x.groupdict() for x in re.finditer(index[0], self)]
        if len(index) == 3:
            if len(r) <= index[1]:
                raise Exception(f"There is no item on index {index[1]}")
            return r[index[1]][index[2]]
        elif len(index) == 2 and len(r) == 1:
            return r[0][index[1]]
        else:
            return [x[index[1]] for x in r]


class RegexerList(list):
    def __getitem__(self, index):
        if isinstance(index, int):
            return list(self)[index]
        if isinstance(index, str):
            return [x[index] for x in self]


class Regexer:
    """Simplify working with regex.

    Examples:
        ::
            >>> Regexer([r"(?P<num>\\d+)")("Test01 string sentence02")['num']
            ['01', '02']
            >>> Regexer([r"(?P<num>\\d+)")("Test01 string sentence02")[1]['num']
            '02'

    Raises:
        Exception: type not supported.
        Exception: no item found by index.
    """

    def __init__(self, r):
        self.r = r

    def __call__(self, s):
        return RegexerList(RegexerString(s)[self.r])
