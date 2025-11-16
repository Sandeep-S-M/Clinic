from fastapi import HTTPException,status,Depends,APIRouter
from typing import List
from sqlalchemy.orm import Session
from Database import data_connect,patient_data
from Models import m_users
from . import emailservices 
router = APIRouter()


@router.post("/user/",response_model=m_users.UserResponse,status_code =status.HTTP_201_CREATED,tags =["Users"])
async def post_User(user:m_users.UserCreate,db:Session = Depends(data_connect.get_db)):
  verify = db.query(patient_data.UserData).filter(patient_data.UserData.email == user.email).first()
  if verify:
    raise HTTPException(status_code =status.HTTP_226_IM_USED,detail=f"user with {user.email} already exist")
  new_user = patient_data.UserData(**user.model_dump())
  db.add(new_user)
  db.commit()
  db.refresh(new_user)
  emailservices.send_welcome_email(new_user)

  return new_user

@router.get("/users/",response_model = List[m_users.UserResponse],status_code=status.HTTP_200_OK,tags =["Users"])
async def get_users(db:Session = Depends(data_connect.get_db)):
  find_users = db.query(patient_data.UserData).all()
  return find_users
@router.get("/user/{id}/",response_model = m_users.UserResponse,status_code=status.HTTP_200_OK,tags =["Users"])
async def get_user(id:int,db:Session = Depends(data_connect.get_db)):
  find_user = db.query(patient_data.UserData).filter(patient_data.UserData.id == id).first()
  if not find_user:
    return "User not found"
  return find_user