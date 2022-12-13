from datetime import datetime

from pydantic import BaseModel


class Company(BaseModel):
    name: str
    address: str
    website: str or None = None
    scale: str or None = None
    contact: str
    slug: str or None = None
    created_at: datetime or None = None
    updated_at: datetime or None = None

    def company_to_dict(self):
        return vars(self)


def company_result(company) -> dict:
    return {
        "id": company[0],
        "name": company[1],
        "address": company[2],
        "website": company[3],
        "scale": company[4],
        "slug": company[5],
        "contact": company[6],

    }


def company_list_result(companies) -> list:
    return [company_result(company) for company in companies]
