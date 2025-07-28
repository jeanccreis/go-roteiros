from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.api import routes_auth, routes_user

app = FastAPI(title="Go Roteiros")

@app.get("/", tags=["Root"])
async def root():
    return JSONResponse(content={"message": "API Go Roteiros está no ar 🚀"}, status_code=200)


app.include_router(routes_auth.router, prefix="/auth", tags=["Auth"])
app.include_router(routes_user.router, prefix="/users", tags=["Users"])
