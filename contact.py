from typing import Protocol


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
    def __init__(self, street: str, city: str, state: str, code: str) -> None:
        self.street = street
        self.city = city
        self.state = state
        self.code = code


class Contact:
    allContacts: ContactList = ContactList()

    def __init__(self, name: str, email: str) -> None:
        self.name = name
        self.email = email
        Contact.allContacts.append(self)

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"{self.name!r}, {self.email!r}"
            f")"
        )


class Supplier(Contact):
    def order(self, order: "Order") -> None:
        print(
            "If this where a real system we would send "
            f"'{order}' order to '{self.name}'"
        )


class Friend(Contact):
    def __init__(self, name: str, email: str, phone: str) -> None:
        super().__init__(name, email)  # Вызываем родительский __init__ и передаем аргументы
        self.phone = phone  # И только после вызова родительского __init__, определяем свои атрибуты класса


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
