from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET")  # Get this from Supabase settings
SUPABASE_PROJECT_ID = os.getenv("SUPABASE_PROJECT_ID")  # e.g. abcdefghijklmnop
JWT_ALGORITHM = "HS256"

print(SUPABASE_JWT_SECRET)
# print(SUPABASE_PROJECT_ID)
app = FastAPI()
templates = Jinja2Templates(directory="templates")
security = HTTPBearer()

# Allow frontend to call API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# Auth helper
def verify_jwt(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    print("🔐 Received Token:", token[:30] + "...")

    try:
        payload = jwt.decode(token, SUPABASE_JWT_SECRET, algorithms=[JWT_ALGORITHM], options={"verify_aud": False})
        print(payload)
        return payload
    except JWTError as e:
        # print("❌ JWT Error:", str(e))
        # raise HTTPException(status_code=401, detail="Invalid token")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )


@app.post("/add")
async def add_numbers(data: dict, user=Depends(verify_jwt)):
    a = data.get("a")
    b = data.get("b")
    return {"result": a + b, "user_email": user.get("email")}
