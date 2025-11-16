from fastapi import HTTPException, Depends, status,APIRouter
from sqlalchemy.orm import Session
from typing import List
from . import emailservices
from Models import m_patients
from Database import data_connect,patient_data

router = APIRouter()

@router.get("/patient/",response_model=List[m_patients.PatientResponse],status_code=status.HTTP_200_OK,tags=["Patient"])
async def get_patients(db:Session = Depends(data_connect.get_db)):
  get_all_patient = db.query(patient_data.PatientData).all()
  return get_all_patient

@router.post("/patient/",response_model=m_patients.PatientResponse,tags=["Patient"])
async def create_patient(id:int,patient:m_patients.PatientCreate,db:Session = Depends(data_connect.get_db)):
  user = db.query(patient_data.UserData).filter(patient_data.UserData.id == id).first()
  if not user:
    raise HTTPException( status_code = status.HTTP_404_NOT_FOUND,detail = "Create account first")
  new_patient = patient_data.PatientData(**patient.model_dump(),owner_id =id) 
  db.add(new_patient)
  db.commit()
  db.refresh(new_patient)
  emailservices.send_patient_report_email(new_patient)
  return new_patient

@router.get("/patient/{id}/",response_model=m_patients.PatientResponse,status_code=status.HTTP_200_OK,tags=["Patient"])
async def get_id(id:int,db:Session = Depends(data_connect.get_db)):
  user = db.query(patient_data.PatientData).filter(patient_data.PatientData.id == id).first()
  if not user:
    raise HTTPException( status_code = status.HTTP_404_NOT_FOUND,detail = f"user with {id} not exist")
  return user

@router.put("/patient/{id}",status_code=status.HTTP_200_OK,tags= ["Patient"])
async def update_patient(id:int,patient : m_patients.PatientUpdate,db:Session = Depends(data_connect.get_db)):
  user_query = db.query(patient_data.PatientData).filter(patient_data.PatientData.id == id)
  user = user_query.first()
  if not user:
    raise HTTPException( status_code = status.HTTP_404_NOT_FOUND,detail =  f"user with {id} not exist")
  update_data = patient.model_dump(exclude_unset=True)
  user_query.update(update_data, synchronize_session=False)
  db.commit()
  db.refresh(user)
  return "Data Updated"
  
@router.delete("/patient/{id}/",status_code=status.HTTP_204_NO_CONTENT,tags=["Patient"])
async def delete_patient(id:int,db:Session = Depends(data_connect.get_db)):
  user = db.query(patient_data.PatientData).filter(patient_data.PatientData.id == id).first()
  if not user:
    raise HTTPException( status_code = status.HTTP_404_NOT_FOUND,detail =f"user not {id} exist")
  db.delete(user)
  db.commit()
  return None