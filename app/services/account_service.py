from app.core.enums import AccountTypes
from app.core.errors import DuplicateRegistryError
from app.services.base_service import BaseService
from app.schemas.business import Account

class AccountService(BaseService):

    def list_accounts(self, business_id:int) -> list[Account|None]:
        return self._db.query(Account).filter(Account.business_id == business_id).all()

    def get_account(self, account_id:int) -> Account | None:
        return self._db.query(Account).filter(Account.id = account_id).first()

    def _get_account_by_number(self, account_number:int) -> Account | None:
        return self._db.query(Account).filter(Account.number == account_number).first()

    def create_account(self, data:dict) -> Account:
        if self._get_account_by_number(data['number']):
            if self._get_account_by_number(data['number']).business_id == data['business_id']:
                return DuplicateRegistryError(f"Account with number {data['number']} already exists for business with id {data['business_id']}.")

        account = Account(
            number=data['number'],
            business_id=data['business_id'],
            account_type=AccountTypes(data['account_type'])
        )
        self._add_registrty(account)
        return account

    def update_account(self, account_id:int, data:dict) -> Account | None:
        account = self.get_account(account_id)
        if not account:
            return None

        for k,v in data.items():
            if hasattr(account,k):
                setattr(account,k,v)
        self._update_registry(account)
        return account
        
    def delete_account(self, account_id:int) -> bool:
        account = self.get_account(account_id)
        if not account:
            return False
        self._delete_registry(account)
        return True
