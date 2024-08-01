"""
Данный пример демонстрирует работу таких принципов ООП как НАСЛЕДОВАНИЕ,
МНОЖЕСТВЕННОЕ НАСЛЕДОВАНИЕ, ПРОТОКОЛЫ
"""

from typing import Protocol, Any


class LongNameDict(dict[str, int]):
    def longestKey(self) -> str | None:
        "In effect, max(self, key=len), but less obscure"
        longest = None
        for key in self:
            if longest is None or len(key) > len(longest):
                longest = key

        return longest


class ContactList(list["Contact"]):
    def search(self, name: str) -> list["Contact"]:
        matchingContacts: list["Contact"] = []
        for contact in self:
            if name in contact.name:
                matchingContacts.append(contact)

        return matchingContacts


class AddressHolder:
    def __init__(
        self,
        /,
        street: str = "",
        city: str = "",
        state: str = "",
        code: str = "",
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs) # type: ignore [call-arg]
        self.street = street
        self.city = city
        self.state = state
        self.code = code


class Contact:
    allContacts: ContactList = ContactList()

    def __init__(self, /, name: str = "", email: str = "", **kwargs: Any) -> None:
        super().__init__(**kwargs) # type: ignore [call-arg]
        self.name = name
        self.email = email
        self.allContacts.append(self)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(" f"{self.name!r}, {self.email!r}" f")"


class Supplier(Contact):
    def order(self, order: "Order") -> None:
        print(
            "If this where a real system we would send "
            f"'{order}' order to '{self.name}'"
        )


class Friend(Contact):
    def __init__(self, /, phone: str = "", **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.phone = phone 


class Emailable(Protocol):
    email: str


class MailSender(Emailable):
    def sendMail(self, message: str) -> None:
        print(f"Sending mail to {self.email=}. {message}")


class EmailableContact(Contact, MailSender):
    pass


e = EmailableContact("John B", "jog@gmail.com")
print(Contact.allContacts)
e.sendMail("Hello, test")
