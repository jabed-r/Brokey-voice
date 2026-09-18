from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
import edge_tts

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Brokey AI Voice Server is Live!"}

@app.get("/speak")
async def speak(text: str, voice: str = "hi-IN-MadhurNeural"):
    communicate = edge_tts.Communicate(text, voice)
    audio_data = bytearray()
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_data.extend(chunk["data"])
            
    return Response(content=bytes(audio_data), media_type="audio/mpeg")
