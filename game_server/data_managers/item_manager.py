import random
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional

from game_server.models.models import Item, AccountItem, Account


class ItemManager:
    def create_item(
            self, db: Session, name: str, description: str, price: float,
            sell_price: float, image_reference: str = None
    ):
        """Create a new game item"""
        item = Item(
            name=name,
            description=description,
            price=price,
            sell_price=sell_price,
            image_reference=image_reference
        )

        # Add and commit the new item to the database
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    def get_item_by_id(self, db: Session, item_id: int):
        """Retrieve an item by its ID"""
        item = db.query(Item).filter(Item.item_id == item_id).first()
        if not item:
            return None
        return item

    def get_item_by_name(self, db: Session, name: str):
        """Retrieve an item by its name"""
        item = db.query(Item).filter(Item.name == name).first()
        if not item:
            return None
        return item

    def get_all_items(self, db: Session, **kwargs):
        return db.query(Item).all()

    def update_item(self, db: Session, item_id: int, name: str = None,
                    description: str = None, price: float = None,
                    sell_price: float = None, image_reference: str = None):
        """Update an existing item's details"""
        item = self.get_item_by_id(db, item_id)
        if not item:
            return None

        # Update only the fields that are provided
        if name is not None:
            item.name = name
        if description is not None:
            item.description = description
        if price is not None:
            item.price = price
        if sell_price is not None:
            item.sell_price = sell_price
        if image_reference is not None:
            item.image_reference = image_reference

        db.commit()
        db.refresh(item)
        return item

    def delete_item(self, db: Session, item_id: int):
        """Delete an item by its ID"""
        item = self.get_item_by_id(db, item_id)
        if not item:
            return {"message": "Item not found"}

        db.delete(item)
        db.commit()
        return {"message": "Item deleted successfully"}


class AccountItemManager:
    def assign_item_to_account(self, db: Session, account_id: int, item_id: int):
        """Assign an item to an account (purchase)"""
        # Check if this account already has this item
        existing = db.query(AccountItem).filter(
            AccountItem.account_id == account_id,
            AccountItem.item_id == item_id
        ).first()

        if existing:
            return {"message": "Account already owns this item"}

        # Create new account_item relationship
        account_item = AccountItem(
            account_id=account_id,
            item_id=item_id,
            acquisition_date=datetime.utcnow()
        )

        db.add(account_item)
        db.commit()
        db.refresh(account_item)
        return account_item

    def get_account_item(self, db: Session, account_id: int, item_id: int):
        """Get a specific account-item relationship"""
        account_item = db.query(AccountItem).filter(
            AccountItem.account_id == account_id,
            AccountItem.item_id == item_id
        ).first()

        if not account_item:
            return None
        return account_item

    def get_all_account_items(self, db: Session, account_id: int):
        """Get all items owned by an account"""
        account_items = db.query(AccountItem).filter(
            AccountItem.account_id == account_id
        ).all()

        return account_items

    def get_accounts_with_item(self, db: Session, item_id: int):
        """Get all accounts that own a specific item"""
        account_items = db.query(AccountItem).filter(
            AccountItem.item_id == item_id
        ).all()

        return account_items

    def remove_item_from_account(self, db: Session, account_id: int, item_id: int):
        """Remove an item from an account (sell)"""
        account_item = self.get_account_item(db, account_id, item_id)

        if not account_item:
            return {"message": "Account does not own this item"}

        db.delete(account_item)
        db.commit()
        return {"message": "Item removed from account successfully"}

    def get_recently_acquired_items(self, db: Session, account_id: int, limit: int = 5):
        """Get the most recently acquired items for an account"""
        recent_items = db.query(AccountItem).filter(
            AccountItem.account_id == account_id
        ).order_by(AccountItem.acquisition_date.desc()).limit(limit).all()

        return recent_items

    def check_if_account_has_item(self, db: Session, account_id: int, item_id: int) -> bool:
        """Check if an account owns a specific item"""
        account_item = self.get_account_item(db, account_id, item_id)
        return account_item is not None


