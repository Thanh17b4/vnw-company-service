import uvicorn
from fastapi import FastAPI
from company import company_router
app = FastAPI()
app.include_router(company_router)
uvicorn.run(app, host="localhost", port=5002)
