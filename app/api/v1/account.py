from fastapi import APIRouter, Depends, HTTPException


from app.core.errors import DuplicateRegistryError
from app.db.session import database_session
from app.models.account import AccountCreate, AccountRead, AccountUpdate, AccountDelete
from app.services.account_service import AccountService

account_router = APIRouter(
    prefix="/account"
)

def get_account_service() -> AccountService:
    return AccountService(database_session())

@account_router.get("/by_business/{business_id}", response_model=list[AccountRead])
def get_account_list(business_id:int, service:AccountService = Depends(get_account_service)):
    return service.list_accounts(business_id)

@account_router.get("/{account_id}", response_model=AccountRead)
def get_account(account_id:int, service:AccountService = Depends(get_account_service)):
    return service.get_account(account_id)

@account_router.post("/", response_model=AccountRead)
def create_account(account:AccountCreate, service:AccountService = Depends(get_account_service)):
    try:
        return service.create_account(account.model_dump())
    except DuplicateRegistryError as exc:
        raise HTTPException(status_code=400, detail=exc)

@account_router.put("/{account_id}", response_model=AccountRead)
def update_account(account_id:int, account:AccountUpdate, service:AccountService = Depends(get_account_service)):
    updated = service.update_account(account_id, account.model_dump())
    if not updated:
        raise HTTPException(status_code=404, detail=f"Account with id {account_id} not found.")
    return updated

@account_router.delete("/{account_id}")
def delete_account(account_id:int, service:AccountService = Depends(get_account_service)):
    deleted = service.delete_account(account_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Account with id {account_id} not found.")
