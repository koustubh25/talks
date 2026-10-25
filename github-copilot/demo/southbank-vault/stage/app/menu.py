"""Southbank Roasters: the café menu service (a tiny app so the demo repo looks real)."""

MENU = {
    "flat white": 5.20,
    "long black": 4.80,
    "cappuccino": 5.20,  # the recipe itself lives in the vault (.env)
    "magic": 5.50,
}


def price(item: str) -> float:
    """Return the price of a menu item."""
    return MENU[item.lower()]


if __name__ == "__main__":
    for name, cost in MENU.items():
        print(f"{name:<12} ${cost:.2f}")
