import random, pytest, csv
from faker import Factory

class Employee ():
    def __init__(self, last_name, first_name, id, birthday):
        self.last_name=last_name
        self.first_name=first_name
        self.id=id
        self.birthday = birthday
    @classmethod
    def fake_employee(cls):
        fakerFR = Factory.create('fr_FR')
        last_name=fakerFR.last_name()
        first_name=fakerFR.first_name()
        id=str(random.randrange (100000, 999999))
        birthday = fakerFR.date_of_birth(minimum_age=18, maximum_age=80).strftime("%Y-%m-%d")
        return cls(first_name, last_name, id, birthday)

@pytest.fixture
def test_data():
    with open('logins.csv', 'r') as f:
        reader = csv.DictReader(f)
        data = list(reader)
    return data
def get_by_label(page, label):
    element = page.locator(f"xpath=//label[text()='{label}']/../..//input")
    return (element)

