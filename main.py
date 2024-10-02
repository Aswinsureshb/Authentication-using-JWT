from jwt_util_1 import ACCESS_TOKEN_EXPIRY_MINUTES, create_access_token, get_current_user, is_jwt_valid, ACCESS_TOKEN_EXPIRY_SECONDS;
from datetime import time
from fastapi import FastAPI, Depends, HTTPException, status, Request, Response
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
from typing import List

class Transaction(BaseModel):
    id: int
    amount: float
    date: datetime
    description: str

transactions = [
    Transaction(id=1, amount=100.0, date=datetime.now(), description=" I ate at McDonalds and now I am ready for a heart attack"),
    Transaction(id=2, amount=10.50, date=datetime.now(), description=" I gave it to a street beggar who had apple pay"),
]


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials = True,
    allow_methods=["*"],
    allow_headers=["*"]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password
    
    if username !="aswin" or password != "password":
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRY_MINUTES)
    access_token = create_access_token(payload={"username": username}, expires_delta=access_token_expires)
    response = JSONResponse(content={"access_token": access_token, "token_type": "bearer"})
    response.set_cookie(key="access_token", value=access_token)
    return response
    
@app.get("/welcome")
async def welcome(request: Request):
    token = request.cookies.get("access_token")
    if not token or not is_jwt_valid(token):
         raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    username = get_current_user(token);
    message = f'Glad to see you again {username}'
    return {"message": message}
 
@app.get("/transactions")
async def get_transactions(request: Request):
    token = request.cookies.get("access_token")
    if not token or not is_jwt_valid(token):
         raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    message = transactions
    return {"message": message}        

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
