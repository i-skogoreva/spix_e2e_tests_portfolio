from faker import Faker

fake = Faker()

class BaseGenerator:
    username = f"{fake.word()}_{fake.random_int(0, 99999)}"
    password = fake.password()
    email = fake.email()