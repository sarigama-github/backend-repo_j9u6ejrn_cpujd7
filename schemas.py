"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field
from typing import Optional, List

# Example schemas (retain for reference):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# New schemas for this project

class Service(BaseModel):
    """
    Service offerings you sell (e.g., website development, SEO, maintenance)
    Collection name: "service"
    """
    title: str = Field(..., description="Service title")
    slug: str = Field(..., description="URL-friendly identifier")
    description: str = Field(..., description="Short description of the service")
    price_from: float = Field(..., ge=0, description="Starting price")
    features: List[str] = Field(default_factory=list, description="Key features included")
    popular: bool = Field(False, description="Mark as popular for highlighting")

class Inquiry(BaseModel):
    """
    Leads from the contact/quote form
    Collection name: "inquiry"
    """
    name: str = Field(..., description="Client name")
    email: str = Field(..., description="Client email")
    company: Optional[str] = Field(None, description="Company name")
    service_id: Optional[str] = Field(None, description="Selected service id or slug")
    budget: Optional[str] = Field(None, description="Budget range text")
    message: Optional[str] = Field(None, description="Message details")
