from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class Verification(BaseModel):
    status: str
    strategy: str


class EmailAddress(BaseModel):
    email_address: str
    id: str
    linked_to: List
    object: str
    verification: Verification


class ClerkUser(BaseModel):
    birthday: str
    created_at: int
    email_addresses: List[EmailAddress]
    external_accounts: List
    external_id: str
    first_name: str
    gender: str
    id: str
    image_url: str
    last_name: str
    last_sign_in_at: int
    object: str
    password_enabled: bool
    phone_numbers: List
    primary_email_address_id: str
    primary_phone_number_id: Any
    primary_web3_wallet_id: Any
    private_metadata: Dict[str, Any]
    profile_image_url: str
    public_metadata: Dict[str, Any]
    two_factor_enabled: bool
    unsafe_metadata: Dict[str, Any]
    updated_at: int
    username: Any
    web3_wallets: List


class Webhook(BaseModel):
    data: object
    object: str
    type: str
