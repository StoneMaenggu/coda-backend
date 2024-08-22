from pydantic import BaseModel, Field


class LoginBase(BaseModel):
    phone_num: str | None = Field(None, example="01012345678")

class IdCheck(LoginBase):
    pass

class Login(LoginBase):
    user_password: str | None = Field(None, example="helloCODA!!")

class IdCheckResponse(IdCheck):
    id_exist: bool

    class Config:
        from_attributes = True

class LoginResponse(Login):
    login_success: bool
    user_id: int

    class Config:
        from_attributes = True


