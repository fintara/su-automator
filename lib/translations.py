from abc import ABC, ABCMeta, abstractmethod, abstractproperty
from dataclasses import dataclass


class Translation(ABC, metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, code: str):
        self.__code = code

    @property
    def code(self):
        return self.__code

    @property
    @abstractmethod
    def value(self):
        pass


__existing_names = []
__existing_codes = []


def __mk_translation(name: str, code: str):
    if name in __existing_names:
        raise Exception(f"Translation named '{name}' already created.")
    __existing_names.append(name)
    if code in __existing_codes:
        raise Exception(f"Translation code '{code}' already created.")
    __existing_codes.append(code)

    class C(Translation):
        @property
        def value(self):
            return self.__value

        def __init__(self, value: str):
            super().__init__(code)
            self.__value = value
    C.__name__ = name
    return C


Belarusian = __mk_translation("Belarusian", "be")
Bulgarian = __mk_translation("Bulgarian", "bg")
Chinese = __mk_translation("Chinese", "zh")
Croatian = __mk_translation("Croatian", "hr")
Czech = __mk_translation("Czech", "cs")
English = __mk_translation("English", "en")
German = __mk_translation("German", "de")
Greek = __mk_translation("Greek", "el")
Hungarian = __mk_translation("Hungarian", "hu")
Italian = __mk_translation("Italian", "it")
Japanese = __mk_translation("Japanese", "ja")
Portuguese = __mk_translation("Portuguese", "pt")
Romanian = __mk_translation("Romanian", "ro")
Russian = __mk_translation("Russian", "ru")
Slovak = __mk_translation("Slovak", "sk")
Slovenian = __mk_translation("Slovenian", "sl")
Turkish = __mk_translation("Turkish", "tr")
Ukrainian = __mk_translation("Ukrainian", "uk")