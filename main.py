from fastapi import FastAPI
import router.userroutes as userroutes

from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.include_router(userroutes.router)

@app.get("/")
async def home():
    return {"message": "Hello, World!"}



