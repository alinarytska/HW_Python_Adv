from pydantic import BaseModel, Field, EmailStr, ValidationError, field_validator, model_validator


class Address(BaseModel):
    city: str = Field(min_length=2)
    street: str = Field(min_length=3)
    house_number: int = Field(gt=0)


class User(BaseModel):
    name: str = Field(min_length=2)
    age: int = Field(ge=0, le=120)
    email: EmailStr
    is_employed: bool
    address: Address

    @field_validator("name")
    def validate_name(cls, value: str) -> str:
        cleaned_value = value.replace(" ", "")
        if not cleaned_value.isalpha():
            raise ValueError("Name must contain only letters.")
        return value

    @model_validator(mode="after")
    def validate_employment_age(self):
        if self.is_employed and not (18 <= self.age <= 65):
            raise ValueError("If user is employed, age must be between 18 and 65.")
        return self


def process_user_json(json_data: str) -> str:
    try:
        user = User.model_validate_json(json_data, strict=True)
        return user.model_dump_json(indent=4)
    except ValidationError as error:
        return error.json()


json_valid = """
{
    "name": "John Doe",
    "age": 30,
    "email": "john.doe@example.com",
    "is_employed": true,
    "address": {
        "city": "New York",
        "street": "5th Avenue",
        "house_number": 123
    }
}
"""

json_invalid_age = """
{
    "name": "John Doe",
    "age": 70,
    "email": "john.doe@example.com",
    "is_employed": true,
    "address": {
        "city": "New York",
        "street": "5th Avenue",
        "house_number": 123
    }
}
"""

json_invalid_name = """
{
    "name": "John123",
    "age": 25,
    "email": "john.doe@example.com",
    "is_employed": true,
    "address": {
        "city": "Berlin",
        "street": "Main Street",
        "house_number": 10
    }
}
"""

print("Valid example:")
print(process_user_json(json_valid))
print()

print("Invalid age example:")
print(process_user_json(json_invalid_age))
print()

print("Invalid name example:")
print(process_user_json(json_invalid_name))
print()