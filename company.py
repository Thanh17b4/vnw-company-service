from starlette import status

from schemas import Company, CompanyResult, CompanyListResult
from model.check_data import is_blank
from config import mydb
from slugify import slugify
from fastapi import APIRouter, Response

company_router = APIRouter()


@company_router.post('/company/create/', status_code=201)
def create_company(request: Company, response: Response):
    company = request.company_to_dict()
    # Validate data
    is_ok, msg = __validate(company)
    if is_ok is False:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return msg
    slug = slugify(company["name"])
    with mydb:
        my_cursor = mydb.cursor()
        sql = "INSERT INTO company (name, address, website, scale, contact, slug) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (company["name"], company["address"], company["website"], company["scale"], company["contact"], slug)
        my_cursor.execute(sql, val)
        mydb.commit()
        response.status_code = status.HTTP_201_CREATED
        return f"{my_cursor.rowcount} company has been inserted successfully"


def __validate(req: dict):
    if req.get("name") is None or is_blank(req.get("name")) is True:
        return False, "name cannot be null"
    if req.get("address") is None or is_blank(req.get("address")) is True:
        return False, "address cannot be null"
    if req.get("contact") is None or is_blank(req.get("contact")) is True:
        return False, "contact cannot be null"
    return req, ""


@company_router.get('/company/detail/{id}', status_code=200)
def detail_company(id: int, response: Response):
    with mydb:
        my_cursor = mydb.cursor()
        my_cursor.execute("SELECT * FROM company WHERE id = %d" % id)
        company = my_cursor.fetchone()
        if company is None:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return False, f"company_id is not correct"
        return True, CompanyResult(company)


@company_router.get('/company/all/', status_code=200)
def all_company(page: int, limit: int, response: Response):
    with mydb:
        my_cursor = mydb.cursor()
        my_cursor.execute("SELECT COUNT(*) FROM company")
        total_companies = my_cursor.fetchone()[0]
        d = total_companies % limit
        if d == 0:
            total_page = total_companies // limit
        else:
            total_page = total_companies // limit + 1
        offset = (page - 1) * limit
        if page > total_page or page <= 0:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return f"page is not exist, total page is {total_page}"
        my_cursor.execute("SELECT * FROM company LIMIT %s OFFSET %s", (limit, offset))
        companies = my_cursor.fetchall()
        if companies is None:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return f"query was wrong"
        return CompanyListResult(companies)


@company_router.put('/company/update/{id}', status_code=200)
async def update_company(id: int, req: Company, response: Response):
    company = req.company_to_dict()
    boolean, result = detail_company(id, response)
    if boolean is False:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return result
    # check have some changes or not
    ok, msg = __check_changes(result, company)
    if ok is False:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return msg
    slug = slugify(company["name"])
    with mydb:
        my_cursor = mydb.cursor()
        sql = "UPDATE company SET name = %s, address = %s, website = %s, scale = %s, contact = %s, slug = %s   WHERE id = %s"
        val = (company["name"], company["address"], company["website"], company["scale"], company["contact"], slug, id)
        my_cursor.execute(sql, val)
        return f"{my_cursor.rowcount} row affected"


def __check_changes(req: dict, new_req: dict):
    if req["name"] == new_req["name"] and req["address"] == new_req["address"] and req["website"] == new_req["website"] and \
       req["scale"] == new_req["scale"] and req["contact"] == new_req["contact"]:
        return False, "no information have been changed"
    return new_req, ""


@company_router.delete('/company/delete/{id}', status_code=200)
async def delete_company(id: int, response: Response):
    boolean, result = detail_company(id, response)
    if boolean is False:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return result
    with mydb:
        my_cursor = mydb.cursor()
        my_cursor.execute("DELETE FROM company WHERE id = %d" % id)
        return f"{my_cursor.rowcount} row affected"
