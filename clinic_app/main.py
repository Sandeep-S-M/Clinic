from fastapi import FastAPI
from Routers import patients,users
from Database import data_connect




app = FastAPI(
    title="Main Application Demo",
)
data_connect.Base.metadata.create_all(data_connect.engine)

app.include_router(patients.router)

app.include_router(users.router)


#database setup 
# DATABASE_URL = "sqlite:///./clinic.db"
# engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
# Base = declarative_base()
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# def get_db():
#   db = SessionLocal()
#   try:
#     yield db
#   finally:  
#     db.close()
#//////////////////////////////////////////////////////////////
#table creation

# class UserData(Base):
#     __tablename__ = "user_data"
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, index=True)
#     email = Column(String, unique=True, index=True)
#     password = Column(String)


#     patients = relationship("PatientData",back_populates = "owner" )
    
# class PatientData(Base):
#     __tablename__ = "patient_data"
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, index=True)
#     age = Column(Integer)
#     phone = Column(String, unique=True, index=True)
#     address = Column(String)
#     disease = Column(String)
#     description = Column(String)
    
    
#     owner_id = Column(Integer,ForeignKey("user_data.id" ))
#     owner = relationship("UserData",back_populates= "patients")
  
# /////////////////////////////////////////////////////////////
#pydantic models
#user data
# class UserBase(BaseModel):
#   name:str
#   email:EmailStr
# class UserCreate(UserBase):
#   password:str
  
# class UserResponse(UserBase):
#   id:int
#   class Config():
#     from_attributes = True
# class PatientBase(BaseModel):
#     name: str
#     age: int
#     address: str
#     phone: str
#     disease: str
#     description: str
# class PatientCreate(PatientBase):
#     pass
# class PatientUpdate(BaseModel):
#     name: str | None = None
#     age: int | None = None
#     address: str | None = None
#     phone: str | None = None
#     disease: str | None = None
#     description: str | None = None


# class PatientResponse(PatientBase):
#     id: int
#     owner_id:int
#     owner:UserResponse
#     class Config():
#       from_attributes = True
    
# #//////////////////////////////////////////////////////////////
# #routings of Users
# @app.post("/user/",response_model=UserResponse,status_code =status.HTTP_201_CREATED,tags =["Users"])
# async def post_User(user:UserCreate,db:Session = Depends(get_db)):
#   verify = db.query(UserData).filter(UserData.email == user.email).first()
#   if verify:
#     raise HTTPException(status_code =status.HTTP_226_IM_USED,detail=f"user with {user.email} already exist")
#   new_user = UserData(**user.model_dump())
#   db.add(new_user)
#   db.commit()
#   db.refresh(new_user)
#   login_to_database(new_user.name,new_user.email)
#   return new_user

# @app.get("/users/",response_model = List[UserResponse],status_code=status.HTTP_200_OK,tags =["Users"])
# async def get_users(db:Session = Depends(get_db)):
#   find_users = db.query(UserData).all()
#   return find_users
# @app.get("/user/{id}/",response_model = UserResponse,status_code=status.HTTP_200_OK,tags =["Users"])
# async def get_user(id:int,db:Session = Depends(get_db)):
#   find_user = db.query(UserData).filter(UserData.id == id).first()
#   if not find_user:
#     return "User not found"
#   return find_user


# #//////////////////////////////////////////////////////////////
# #routings of Patients
# @app.get("/patient/",response_model=List[PatientResponse],status_code=status.HTTP_200_OK,tags=["Patient"])
# async def get_patients(db:Session = Depends(get_db)):
#   get_all_patient = db.query(PatientData).all()
#   return get_all_patient

# @app.post("/patient/",response_model=PatientResponse,tags=["Patient"])
# async def create_patient(id:int,patient:PatientCreate,db:Session = Depends(get_db)):
#   user = db.query(UserData).filter(UserData.id == id).first()
#   if not user:
#     raise HTTPException( status_code = status.HTTP_404_NOT_FOUND,detail =  f"Create account Gandu")
#   new_patient = PatientData(**patient.model_dump(),owner_id =id) 
#   db.add(new_patient)
#   db.commit()
#   db.refresh(new_patient)

#   return new_patient

# @app.get("/patient/{id}/",response_model=PatientResponse,status_code=status.HTTP_200_OK,tags=["Patient"])
# async def get_id(id:int,db:Session = Depends(get_db)):
#   user = db.query(PatientData).filter(PatientData.id == id).first()
#   if not user:
#     raise HTTPException( status_code = status.HTTP_404_NOT_FOUND,detail = f"user with {id} not exist")
#   return user

# @app.put("/patient/{id}",status_code=status.HTTP_200_OK,tags= ["Patient"])
# async def update_patient(id:int,patient : PatientUpdate,db:Session = Depends(get_db)):
#   user_query = db.query(PatientData).filter(PatientData.id == id)
#   user = user_query.first()
#   if not user:
#     raise HTTPException( status_code = status.HTTP_404_NOT_FOUND,detail =  f"user with {id} not exist")
#   update_data = patient.model_dump(exclude_unset=True)
#   user_query.update(update_data, synchronize_session=False)
#   db.commit()
#   db.refresh(user)
#   return "Data Updated"
  
# @app.delete("/patient/{id}/",status_code=status.HTTP_204_NO_CONTENT,tags=["Patient"])
# async def delete_patient(id:int,db:Session = Depends(get_db)):
#   user = db.query(PatientData).filter(PatientData.id == id).first()
#   if not user:
#     raise HTTPException( status_code = status.HTTP_404_NOT_FOUND,detail =f"user not exist")
#   db.delete(user)
#   db.commit()
#   return None
  
'''from fastapi import FastAPI, HTTPException, status, Depends
from typing import List
from pydantic import BaseModel
from sqlalchemy.orm import Session, relationship
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# --- 1. Database Setup (No changes here) ---
DATABASE_URL = "sqlite:///./clinic.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- CORRECTED Dependency to get a DB session ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- 2. SQLAlchemy Models (Updated with Relationship) ---

class UserData(Base):
    __tablename__ = "user_data"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    # This creates a back-reference from User to PatientData
    patients = relationship("PatientData", back_populates="owner")

class PatientData(Base):
    __tablename__ = "patient_data"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    phone = Column(String, unique=True, index=True)
    age = Column(Integer)
    address = Column(String)
    disease = Column(String)
    description = Column(String)
    
    # --- NEW: Foreign Key to link to the user table ---
    owner_id = Column(Integer, ForeignKey("user_data.id"))

    # --- NEW: Relationship to the UserData model ---
    owner = relationship("UserData", back_populates="patients")


# --- Create tables ---
# This needs to be after the models are defined
Base.metadata.create_all(bind=engine)


# --- 3. Pydantic Schemas (Updated for Relationships) ---

# Base schema for a User
class UserBase(BaseModel):
    name: str
    email: str

# Schema for creating a User (can add password validation here later)
class UserCreate(UserBase):
    password: str

# Schema for the response (never include the password!)
class UserResponse(UserBase):
    id: int
    
    class Config:
        from_attributes = True

# Base schema with common patient fields
class PatientBase(BaseModel):
    name: str
    age: int
    address: str
    phone: str
    disease: str
    description: str

# Schema for creating a new patient
class PatientCreate(PatientBase):
    pass

# Schema for updating a patient
class PatientUpdate(BaseModel):
    name: str | None = None
    age: int | None = None
    address: str | None = None
    phone: str | None = None
    disease: str | None = None
    description: str | None = None

# --- UPDATED Response Schema ---
# Now includes the nested User information
class PatientResponse(PatientBase):
    id: int
    owner_id: int
    owner: UserResponse  # Nest the full user response object

    class Config:
        from_attributes = True

# --- 4. FastAPI Application and Routes ---
app = FastAPI(
    title="Clinic API",
    description="A simple API to manage patient and user records."
)

# --- NEW: Basic CRUD for Users so we can test the relationship ---

@app.post("/users/", response_model=UserResponse, status_code=status.HTTP_201_CREATED, tags=["Users"])
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # In a real app, you would hash the password here
    # from passlib.context import CryptContext
    # pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    # hashed_password = pwd_context.hash(user.password)
    # db_user = UserData(email=user.email, name=user.name, password=hashed_password)
    db_user = UserData(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/{id}", response_model=UserResponse, tags=["Users"])
async def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(UserData).filter(UserData.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# --- UPDATED Patient Routes ---

@app.get("/patients/", response_model=List[PatientResponse], tags=["Patients"])
async def get_all_patients(db: Session = Depends(get_db)):
    all_patients = db.query(PatientData).all()
    return all_patients

# --- UPDATED create_patient endpoint ---
@app.post("/patients/", response_model=PatientResponse, status_code=status.HTTP_201_CREATED, tags=["Patients"])
async def create_patient(patient: PatientCreate, user_id: int, db: Session = Depends(get_db)):
    # Check if the user exists first
    user = db.query(UserData).filter(UserData.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not found")

    # Create the patient instance and assign the owner_id
    new_patient = PatientData(**patient.model_dump(), owner_id=user_id)
    
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)
    return new_patient

@app.get("/patients/{id}", response_model=PatientResponse, status_code=status.HTTP_200_OK, tags=["Patients"])
async def get_patient_by_id(id: int, db: Session = Depends(get_db)):
    patient = db.query(PatientData).filter(PatientData.id == id).first()
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Patient with id {id} not found")
    return patient

@app.put("/patients/{id}", response_model=PatientResponse, status_code=status.HTTP_200_OK, tags=["Patients"])
async def update_patient(id: int, patient_update: PatientUpdate, db: Session = Depends(get_db)):
    patient_query = db.query(PatientData).filter(PatientData.id == id)
    db_patient = patient_query.first()

    if not db_patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Patient with id {id} not found")

    update_data = patient_update.model_dump(exclude_unset=True)
    patient_query.update(update_data, synchronize_session=False)

    db.commit()
    db.refresh(db_patient)
    return db_patient

@app.delete("/patients/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Patients"])
async def delete_patient(id: int, db: Session = Depends(get_db)):
    patient = db.query(PatientData).filter(PatientData.id == id).first()
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Patient with id {id} not found")
    db.delete(patient)
    db.commit()
    return None

'''