from sqlalchemy.orm import Session
from datetime import datetime
import random
from typing import Optional, Tuple, Dict, Any

from game_server.data_managers.account_manager import AccountManager
from game_server.data_managers.item_manager import AccountItemManager, ItemManager
from game_server.models.models import Item, AccountItem


class AuthService:
    def __init__(self):
        self.account_manager = AccountManager()
        self.account_item_manager = AccountItemManager()
        self.items_manager = ItemManager()

    def login(self, db: Session, nickname: str):
        """
        Login or register a user with the given nickname.

        Args:
            nickname: The user's nickname

        Returns:
            Tuple containing:
            - Dictionary with account data (nickname, items, credits)
            - Boolean indicating if this is a new account (True) or existing account (False)
        """
        # Check if account exists
        account = self.account_manager.get_user_by_username(db, nickname)
        if not account:
            account = self.account_manager.create_user(db, nickname)

        # Award login credits (once per login)
        login_credits = random.uniform(self.min_credits, self.max_credits)
        account.credits += login_credits
        db.close()
        db.refresh(account)

        # Prepare account data to return to client
        # Get items owned by this account
        account_items = self.account_item_manager.get_all_account_items(db, account.id)

        # Get all available items
        all_items = self.items_manager.get_all_items(db)

        # Format the response
        account_data = {
            "nickname": account.nickname,
            "credits": account.credits,
            "owned_items": [{"id": item.item_id,
                             "name": item.name,
                             "description": item.description,
                             "sell_price": item.sell_price,
                             "image_ref": item.image_reference}
                            for _, item in account_items],
            "available_items": [{"id": item.item_id,
                                 "name": item.name,
                                 "description": item.description,
                                 "price": item.price,
                                 "image_ref": item.image_reference}
                                for item in all_items]
        }

        return account_data

    def logout(self, nickname: str) -> bool:
        """
        Handle user logout (minimal in this implementation).

        Args:
            nickname: The user's nickname

        Returns:
            Boolean indicating success
        """
        # In a more complex system, we might handle session invalidation here
        # For now, we'll just return success since there's no session management
        return True