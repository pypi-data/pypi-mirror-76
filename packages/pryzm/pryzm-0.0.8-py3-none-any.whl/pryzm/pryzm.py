
from pryzm import text_attribute

class Pryzm(object):
    """Pryzm - Base object to handle adding color
    Uses a dictionary of codes to dynamically add functions named as the key, and inserting
    an ascii code which is the value.  For example, "red": 31 would result in a
    function named 'red()', which takes any number of text entries and wraps with
    with an ascii escape color seqence 31 to provide color.
    """
    _text_attributes = text_attribute
    def __init__(self, *text, echo=False):
        """Creates the base object to generate functions.
        *text        any number of text fields.  They will be wrapped end to end, not around each token
        echo         If this is true, a generated function will act like python's print.
                     Otherwise, you need to call print() yourself, useful when composing multiple color

        Returns: a function which when passed text returns ascii encoded text.
                 Optionally, it will also print if echo is set to true
        """
        self.text = " ".join(text)
        self.features = []
        self.ASC = u"\u001b["
        self.CLR = u"\u001b[0m"
        self.echo = echo

        for feature, ansi_code in self._text_attributes.items():
            self._add_color(feature, ansi_code)

    def reset(self):
        self.features = []
        return self

    def _add_color(self, feature, ansi_code):
        """Add dynamic function to insert color code.
            feature: string, the name of the function to add
            ansi_code: integer, the code value to insert

            return: function, adds a function named 'color' wrapping test with ascii code.
        """
        def fn(self, *text):
            text = " ".join(text)
            self.features.append(str(ansi_code))

            if text:
                self.text = text
                saved_return = self.show()
                if self.echo:
                    print(self.show())

                self.reset()
                return saved_return
            else:                          # If no text, return self so we can chain on '.'
                return self

        fn.__name__ = feature
        fn.__doc__ = "Apply {0} to text".format(feature)
        setattr(Pryzm, feature, fn)

    def show(self):
        return u"{}{}m{}{}".format(self.ASC, ";".join(self.features), self.text, self.CLR)

    def __str__(self):
        return self.show()

    def __repr__(self):
        return self.show()
