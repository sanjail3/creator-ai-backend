from fastapi import FastAPI
import router.userroutes as userroutes
import  router.webhookroute as webhookroute
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.include_router(userroutes.router)
app.include_router(webhookroute.router)
@app.get("/")
async def home():
    return {"message": "Hello, World!"}



