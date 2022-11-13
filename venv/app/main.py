from fastapi import FastAPI, Response, status, HTTPException, Depends

from . import models, utils
from .schemas import TmpCodeBase, UserResponse, UserCreate
from .database import engine, get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def check_404(value: str, email: str):
    if value == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with email {email} was not found")


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Welcome to my API!"}


# GET all TmpCodes stored in database
# @app.get("/tmpcodes")
# def get_tmpcodes(db: Session = Depends(get_db)) -> dict[str, list]:
#     tmpcodes = db.query(models.TmpCode).all()
#     return {"codes": tmpcodes}


# GET one TmpCode by email
@app.get("/tmpcodes/{email}", response_model=TmpCodeBase)
def get_tmpcode(email: str, db: Session = Depends(get_db)) -> dict[str, str]:
    tmpcode = db.query(models.TmpCode).filter(
        models.TmpCode.email == email).first()
    return tmpcode


# CREATE new TmpCode with email, code and expiration_time
@app.post("/tmpcodes", status_code=status.HTTP_201_CREATED, response_model=TmpCodeBase)
def create_tmpcode(tmpcode: TmpCodeBase, db: Session = Depends(get_db)) -> dict[str, TmpCodeBase]:
    new_tmpcode = models.TmpCode(**tmpcode.dict())
    db.add(new_tmpcode)
    db.commit()
    db.refresh(new_tmpcode)
    print(new_tmpcode)
    return new_tmpcode


@app.delete("/tmpcodes/{email}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tmpcode(email: str, db: Session = Depends(get_db)) -> Response:
    deleted_tmpcode = db.query(models.TmpCode).filter(
        models.TmpCode.email == email)
    tmpcode = deleted_tmpcode.first()
    check_404(tmpcode, email)
    deleted_tmpcode.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/tmpcodes/{email}", response_model=TmpCodeBase)
def update_tmpcode(email: str, tmpcode: TmpCodeBase, db: Session = Depends(get_db)) -> dict[str, str]:
    tmpcode_query = db.query(models.TmpCode).filter(
        models.TmpCode.email == email)
    tmpcode_found = tmpcode_query.first()
    check_404(tmpcode_found, email)
    tmpcode_query.update(tmpcode.dict(), synchronize_session=False)
    db.commit()
    return tmpcode_query.first()


@app.get("/users/{email}", response_model=UserResponse)
def get_user_by_email(email: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with email {email} was not found")
    return user


@app.get("/users/username/{username}", response_model=UserResponse)
def get_user_by_username(username: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(
        models.User.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with username {username} was not found")
    return user


@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):

    # Hash the password: user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
