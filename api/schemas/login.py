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
        orm_mode = True

class LoginResponse(Login):
    login_success: bool

    class Config:
        orm_mode = True


