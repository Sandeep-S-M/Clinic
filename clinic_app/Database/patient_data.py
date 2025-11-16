from sqlalchemy import Column, Integer, String,ForeignKey
from sqlalchemy.orm import relationship
from .data_connect import Base
class UserData(Base):
    __tablename__ = "user_data"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    patients = relationship("PatientData",back_populates = "owner" )
    
class PatientData(Base):
    __tablename__ = "patient_data"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)
    phone = Column(String, unique=True, index=True)
    address = Column(String)
    disease = Column(String)
    description = Column(String)
    owner_id = Column(Integer,ForeignKey("user_data.id" ))
    owner = relationship("UserData",back_populates= "patients")