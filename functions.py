# Importamos librerias
import pandas as pd

# Cargamos data
df_recommend = pd.read_csv('/data/df_recommend.csv', encoding='utf-8', lineterminator='\n')
df_sentiment = pd.read_csv('/data/df_sentiment.csv', encoding='utf-8', lineterminator='\n')
df_user_genre = pd.read_csv('/data/df_user_genre.csv', encoding='utf-8', lineterminator='\n')


def PlayTimeGenre(genre: str):
    """
    Devuelve el año con más horas jugadas para un género dado.

    Args:
        genre: El género del juego.

    Returns:
        El año de lanzamiento con más horas jugadas para un género dado.
        Ejemplo de retorno: {"Año de lanzamiento con más horas jugadas para Género X" : 2013}
    """

    # Filtra el DataFrame por género
    df_genre = df_user_genre[df_user_genre['genres'].str.contains(genre)]

    # Agrupa por año y calcula la suma total de horas jugadas para cada año
    playtime_by_year = df_genre.groupby('release_year')['playtime_forever'].sum()

    # Encuentra el año con más horas jugadas
    max_playtime_year = playtime_by_year.idxmax()
    response = {f"Año de lanzamiento con más horas jugadas para el género {genre}" : max_playtime_year}

    return response

def UserForGenre(genre: str):
    """
    Devuelve el usuario que acumula más horas jugadas para un género dado.

    Args:
        genre: El género del juego.

    Returns:
        El usuario con más horas jugadas y una lista de la acumulación de horas jugadas por año.
        Ejemplo de retorno: {"Usuario con más horas jugadas para Género X" : us213ndjss09sdf, "Horas jugadas":[{Año: 2013, Horas: 203}, {Año: 2012, Horas: 100}, {Año: 2011, Horas: 23}]}
    """

    # Filtra el DataFrame por género
    df_genre = df_user_genre[df_user_genre["genres"].str.contains(genre)]

    # Agrupa por usuario y año, y calcula la suma total de horas jugadas para cada usuario y año
    playtime_by_user_year = df_genre.groupby(['user_id', 'release_year'])['playtime_forever'].sum().reset_index()

    # Encuentra el usuario con más horas jugadas
    max_playtime_user = playtime_by_user_year.groupby('user_id')['playtime_forever'].sum().idxmax()

    # Obtiene una lista de la acumulación de horas jugadas por año para el usuario con más horas jugadas
    playtime_by_year = playtime_by_user_year[(playtime_by_user_year['user_id'] == max_playtime_user) & (playtime_by_user_year['release_year'] != -1)][['release_year', 'playtime_forever']].rename(columns={'release_year': 'Año', 'playtime_forever': 'Horas'}).to_dict('records')

    response = {f"Usuario con más horas jugadas para el género {genre}" : max_playtime_user, "Horas jugadas": playtime_by_year}

    return response

def UsersRecommend(year: int):
    """
    Devuelve el top 3 de juegos MÁS recomendados por usuarios para el año dado.
    (reviews.recommend = True y comentarios positivos/neutrales)

    Args:
        year: El año a filtrar.

    Returns:
        El top 3 de juegos recomendados.
        Ejemplo de retorno: [{"Puesto 1" : X}, {"Puesto 2" : Y},{"Puesto 3" : Z}]
    """

    # Filtra el DataFrame por año y recomendación
    df_year = df_recommend[(df_recommend['posted_year'] == year) & (df_recommend['recommend'] == True) & (df_recommend['sentiment_analysis'] > 1)]

    # Agrupa por juego y cuenta el número de recomendaciones para cada juego
    recommendations = df_year.groupby('item_name').size()

    # Ordena los juegos en función del número de recomendaciones y toma el top 3
    top_games = recommendations.sort_values(ascending=False).head(3)

    response = [{"Puesto {}".format(i+1): game} for i, game in enumerate(top_games.index)]

    return response

def UsersNotRecommend(year: int):
    """
    Devuelve el top 3 de juegos MENOS recomendados por usuarios para el año dado. (reviews.recommend = False y comentarios negativos)

    Args:
        year: El año a filtrar.

    Returns:
        El top 3 de juegos no recomendados.
        Ejemplo de retorno: [{"Puesto 1" : X}, {"Puesto 2" : Y},{"Puesto 3" : Z}]
    """

    # Filtra el DataFrame por año y no recomendación
    df_year = df_recommend[(df_recommend['posted_year'] == year) & (df_recommend['recommend'] == False) & (df_recommend['sentiment_analysis'] < 1)]

    # Agrupa por juego y cuenta el número de no recomendaciones para cada juego
    not_recommendations = df_year.groupby('item_name').size()

    # Ordena los juegos en función del número de no recomendaciones y toma el top 3
    top_games = not_recommendations.sort_values(ascending=False).head(3)

    response = [{"Puesto {}".format(i+1): game} for i, game in enumerate(top_games.index)]

    return response

def sentiment_analysis(year: int):
    """
    Según el año de lanzamiento, se devuelve una lista con la cantidad de registros de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento.

    Args:
        year: El año a filtrar.

    Returns:
        El análisis de sentimiento para el año dado.
        Ejemplo de retorno: {Negative = 182, Neutral = 120, Positive = 278}
    """

    # Filtra el DataFrame por año
    df_year = df_sentiment[df_sentiment['release_year'] == year]

    # Cuenta el número de registros de reseñas que se encuentren categorizados con un análisis de sentimiento
    sentiment_counts = df_year['sentiment_analysis'].value_counts().rename({0: 'Negative', 1: 'Neutral', 2: 'Positive'})

    response = sentiment_counts.to_dict()

    return response