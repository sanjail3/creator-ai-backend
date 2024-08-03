import json
import os
from AI.shorts.utils.script_generator import ScriptGenerator
import router.userroutes as userroutes
from fastapi import FastAPI
from pydantic import BaseModel
from AI.shorts.prompts.video_generator_prompt import VIDEO_PROMPT
from AI.shorts.utils.video_syntax import SHORT_VIDEO_WITH_IMAGES

import  router.webhookroute as webhookroute
from dotenv import load_dotenv


class Item(BaseModel):
    topic:str
    duration:str
    tone :str
    language :str
    instructions:str
    num_of_images :int

load_dotenv()

app = FastAPI()

app.include_router(userroutes.router)
app.include_router(webhookroute.router)
@app.get("/")
async def home():
    return {"message": "Hello, World!"}



@app.post("/script")
def generate_script(item: Item):
    try:
        api_key = os.getenv("OPENAI_API_KEY")
        text_creator = ScriptGenerator(api_key=api_key)

        print("Generating script...")
        generated_script = text_creator.generate(
            prompt=VIDEO_PROMPT,
            topic=item.topic,
            duration=item.duration,
            tone=item.tone,
            language=item.language,
            instructions=item.instructions,
            num_of_images=item.num_of_images,
            syntax=SHORT_VIDEO_WITH_IMAGES,
        )
        
        return {"script": generated_script}
    except Exception as e:
        print(e)
        return {"error": str(e)}
