from sqlalchemy.orm import Session

import api.models.tables as tables
import api.schemas.login as login_schema


# 1. 회원 조회
def id_check(db: Session, id_check_body: login_schema.IdCheck):
    user = db.query(tables.User).filter(tables.User.phone_num == id_check_body.phone_num).first()
    if user:
        return login_schema.IdCheckResponse(id_exist=True, **id_check_body.dict())
    else:
        return login_schema.IdCheckResponse(id_exist=False, **id_check_body.dict())
    
# 2. 로그인
def login(db: Session, login_body: login_schema.Login):
    user = db.query(tables.User).filter(tables.User.phone_num == login_body.phone_num).first()
    if user is None:
        return login_schema.LoginResponse(login_success=False, **login_body.dict())
    if user.user_password == login_body.user_password:
        return login_schema.LoginResponse(login_success=True, **login_body.dict())
    else:
        return login_schema.LoginResponse(login_success=False, **login_body.dict())
    