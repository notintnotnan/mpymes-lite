from app.core.errors import DuplicateRegistryError
from app.services.base_service import BaseService
from app.schemas.business import Business

class BusinessService(BaseService):

    def list_businesses(self) -> list[Business]:
        return self._db.query(Business).all()

    def get_business(self, business_id:int) -> Business | None:
        return self._db.query(Business).filter(Business.id == business_id).first()

    def create_business(self, data:dict) -> Business:
        if self._db.query(Business).filter(Business.identifier == data['identifier']).first():
            raise DuplicateRegistryError(f"Business with identifier {data['identifier']} already exists.")
        business = Business(name=data['name'], identifier=data['identifier'])
        self._add_registrty(business)
        return business

    def update_business(self, business_id:int, data:dict) -> Business | None:
        business = self.get_business(business_id)
        if not business:
            return None
        for k,v in data.items():
            if hasattr(business,k):
                setattr(business,k,v)
        self._update_registry(business)
        return business

    def delete_business(self, business_id:int) -> bool:
        business = self.get_business(business_id)
        if not business:
            return False
        self._delete_registry(business)
        return True
