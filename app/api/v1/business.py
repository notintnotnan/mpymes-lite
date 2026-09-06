from fastapi import APIRouter, Depends, HTTPException

from app.db.session import database_session
from app.models.business import BusinessCreate, BusinessRead, BusinessUpdate
from app.services.business_service import BusinessService

business_router = APIRouter(
    prefix="/business"
)

def get_business_service() -> BusinessService:
    return BusinessService(database_session())

@business_router.get("/", response_model=list[BusinessRead])
def get_business_list(service:BusinessService = Depends(get_business_service)):
    return service.list_businesses()

@business_router.get("/{business_id}", response_model=BusinessRead)
def get_business(business_id:int, service:BusinessService = Depends(get_business_service)):
    return service.get_business(business_id)

@business_router.post("/", response_model=BusinessRead)
def create_business(business: BusinessCreate, service:BusinessService = Depends(get_business_service)):
    return service.create_business(business.model_dump())

@business_router.put("/{business_id}", response_model=BusinessRead)
def update_business(business_id:int, business: BusinessUpdate, service:BusinessService = Depends(get_business_service)):
    updated = service.update_business(business_id, business.model_dump())
    if not updated:
        raise HTTPException(status_code=404, detail=f"Business with id {business_id} not found.")
    return updated

@business_router.delete("/{business_id}")
def delete_business(business_id:int, service:BusinessService = Depends(get_business_service)):
    deleted = service.delete_business(business_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Business not found.")
