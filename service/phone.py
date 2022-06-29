class PhoneService:
    __slots__ = []

    def __init__(self):
        pass

    async def auth_code(self, phone):
        return input("Input authentication code: ")