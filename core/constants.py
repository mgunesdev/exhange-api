

class Constant:
    STATUS_ACTIVE = 1
    STATUS_PASSIVE = 2
    STATUS_CHOICES = (
        (STATUS_ACTIVE, 'Aktif'),
        (STATUS_PASSIVE, 'Pasif'),
    )

    LANG_TR = 'tr'
    LANG_EN = 'en'
    LANG_CHOICES = (
        (LANG_TR, 'Turkish'),
        (LANG_EN, 'English'),
    )

    PROVIDER_FIXER = 1
    PROVIDER_CURRENCY_DATA = 2

    PROVIDER_CHOICES = (
        (PROVIDER_FIXER, 'Fixer'),
        (PROVIDER_CURRENCY_DATA, 'CurrencyData'),
    )

