from ..schemas import TmpCodeBase
from .. import models, utils
from sqlalchemy.orm import Session
from ..database import get_db
from fastapi import Response, status, Depends, APIRouter

router = APIRouter(
    prefix="/tmpcodes",
    tags=['TmpCodes']
)


# GET all TmpCodes stored in database
# @app.get("/tmpcodes")
# def get_tmpcodes(db: Session = Depends(get_db)) -> dict[str, list]:
#     tmpcodes = db.query(models.TmpCode).all()
#     return {"codes": tmpcodes}


# GET one TmpCode by email
@router.get("/{email}", response_model=TmpCodeBase)
def get_tmpcode(email: str, db: Session = Depends(get_db)) -> dict[str, str]:
    tmpcode = db.query(models.TmpCode).filter(
        models.TmpCode.email == email).first()
    return tmpcode


# CREATE new TmpCode with email, code and expiration_time
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=TmpCodeBase)
def create_tmpcode(tmpcode: TmpCodeBase, db: Session = Depends(get_db)) -> dict[str, TmpCodeBase]:
    new_tmpcode = models.TmpCode(**tmpcode.dict())
    db.add(new_tmpcode)
    db.commit()
    db.refresh(new_tmpcode)
    return new_tmpcode


@router.delete("/{email}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tmpcode(email: str, db: Session = Depends(get_db)) -> Response:
    deleted_tmpcode = db.query(models.TmpCode).filter(
        models.TmpCode.email == email)
    tmpcode = deleted_tmpcode.first()
    utils.check_404(tmpcode, email)
    deleted_tmpcode.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{email}", response_model=TmpCodeBase)
def update_tmpcode(email: str, tmpcode: TmpCodeBase, db: Session = Depends(get_db)) -> dict[str, str]:
    tmpcode_query = db.query(models.TmpCode).filter(
        models.TmpCode.email == email)
    tmpcode_found = tmpcode_query.first()
    utils.check_404(tmpcode_found, email)
    tmpcode_query.update(tmpcode.dict(), synchronize_session=False)
    db.commit()
    return tmpcode_query.first()
