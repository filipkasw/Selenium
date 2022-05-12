
class UnexpectedElementDesplayed(Exception):
    def __init__(self, method, value):
        self.message = "Element sa greskom na stranici"
        self.method = method
        self.value = value
        super().__init__(self.message, self.method, self.value)

class NoSuchElement(Exception):
    def __init__(self, method, value, message="Nije pronadjen element na stranici : "):
        self.message = message + method + " : " + value
        super().__init__(self.message)

class BadCredentials(Exception):
    def __init__(self):
        self.message = "Neispravni podaci za logovanje"
        super().__init__(self.message)


class ExpectedError(Exception):
    def __init__(self, value, message="Očekivana greška pronadjena, samo nastavljam..."):
        self.message = message
        self.value = value
        super().__init__(self.message)

class BadAppOrOrgJed(Exception):
    def __init__(self, at_val , dom_value,  message="Aplikacija i organizaciona jedinica se nepodudaraju : "):
        self.message = message
        self.at_val = at_val
        self.dom_value = dom_value
        super().__init__(self.message + at_val + " <>" + dom_value )

class NoResultInTable(Exception):
    def __init__(self, message="Nema rezultata u tabeli"):
        self.message = message
        super().__init__(self.message)

class ErrorSummary(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class ComparisonNotCorrect(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)



