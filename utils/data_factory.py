from dataclasses import dataclass

from faker import Faker

_fake = Faker()


@dataclass(frozen=True)
class CheckoutInfo:
    first_name: str
    last_name: str
    postal_code: str


def make_checkout_info() -> CheckoutInfo:
    return CheckoutInfo(
        first_name=_fake.first_name(),
        last_name=_fake.last_name(),
        postal_code=_fake.postcode(),
    )
