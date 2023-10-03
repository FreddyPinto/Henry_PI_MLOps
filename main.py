# Importaciones
from fastapi import FastAPI, Query
import functions as af

import importlib
importlib.reload(af)

# Se instancia la aplicación
app = FastAPI()

# Endpoint para PlayTimeGenre
@app.get("/playtime/{genre}")
async def playtime_genre(genre: str):
    return PlayTimeGenre(genre)

# Endpoint para UserForGenre
@app.get("/user/{genre}")
async def user_for_genre(genre: str):
    return UserForGenre(genre)

# Creamos un endpoint para UsersRecommend
@app.get("/recommend/{year}")
async def users_recommend(year: int):
    return UsersRecommend(year)

@app.get("/not_recommend/{year}")
async def users_not_recommend(year: int):
    return UsersNotRecommend(year)

@app.get("/sentiment_analysis/{year}")
async def sentiment_analysis(year: int):
    return sentiment_analysis(year)