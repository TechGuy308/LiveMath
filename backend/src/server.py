import fastapi
from backend.src.logic import MathTutorEngine
from fastapi.middleware.cors import CORSMiddleware
#uvicorn backend.src.server:app --host 0.0.0.0 --port 8000 --reload

#Initialize the math tutor engine and FastAPI app
brain = MathTutorEngine()
app = fastapi.FastAPI()

origins = [
    "http://localhost:3000",  # Default React port
    "http://localhost:5173",
    "http://localhost:8000"  # Default Vite + React port
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Your React app's URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Define API endpoints
#Calls brain methods
@app.post("/ask")
async def ask(message: str = fastapi.Body()):
    return {"reply":brain.ask(message)}

@app.post("/vision")
async def vision(image: fastapi.UploadFile = fastapi.File()):
    image_bytes = await image.read()
    return {"reply":brain.vision(image_bytes)}

@app.post("/opener")
async def opener(message: str = fastapi.Body(embed=True)):
    return {"reply":brain.get_opening_question(message)}

