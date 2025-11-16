from pydantic import  BaseModel
from .m_users import UserResponse
class PatientBase(BaseModel):
    name: str
    age: int
    address: str
    phone: str
    disease: str
    description: str
class PatientCreate(PatientBase):
    pass
class PatientUpdate(BaseModel):
    name: str | None = None
    age: int | None = None
    address: str | None = None
    phone: str | None = None
    disease: str | None = None
    description: str | None = None


class PatientResponse(PatientBase):
    id: int
    owner_id:int
    owner:UserResponse
    class Config():
      from_attributes = True