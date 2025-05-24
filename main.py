''' 
imagina que esta API es una biblioteca de peliculas
La función load_movies() es como una biblioteca de libros (peliculas) cuando se abre la biblioteca
La función get_movies() muestra todo el catalogo cuando alguien lo pide.
La fucnción get_movie(id) es como si alguien preguntara por un libro especifico es decir, por un codigo de identificación
La funcion chat bot (query) es un asistente que busca peliculas segun palabras clave y sinonimo.
La función get_movies_by_category(category) ayuda a encontrar peliculas segun su genero (acción, comedia, etc...)
'''

# Importamos las herramientas necesarias para continuar nuestra API
from fastapi import FastAPI, HTTPException # FastAPI nos ayuda a crear la API, HTTPException nos ayuda a mejorar errores
from fastapi.responses import HTMLResponse, JSONResponse # HTMLResponse nos ayuda a mejorar respuestas HTML, JSONResponse nos ayuda a manejar respuestas
import pandas as pd # pandas nos ayuda a manejar tablas como si fuera un Excel
import nltk # nltk es una libreria para procesar texto y analizar palabras
from nltk.tokenize import word_tokenize # word_tokenize nos ayuda a tokenizar texto, es decir, a convertirlo en palabras
from nltk.corpus import wordnet # wordnet es una libreria para analizar sinonimos

# Indicamos la ruta donde nltk buscara los datos descargados en nuestro computador
nltk.data.path.append(r'C:\Users\USER\AppData\Roaming\nltk_data')
nltk.download('punkt') # es un paquete para dividir frases en palabras
nltk.download('punkt_tab') # paquete para encontrar sinonimos en palabras

# función para cargar las peliculas desde un archivo csv

def load_movies():
    # leemos el archivo que contiene información de peliculas y selecciónamos las columnas mas importantes 
    df = pd.read_csv("Dataset/netflix_titles.csv")[['show_id','title','release_year','listed_in','rating','description']]
    
    # Renombramos las colunmas para que sean mas faciles de entender
    df.columns = ['id', 'title', 'year', 'category', 'rating', 'overview']
    
    # Llenamos los espacios vacios con texto vacio y convertimos los datos en una lista de diccionarios
    return df.fillna('').to_dict(orient='records')

# Cargamos las peliculas al iniciar la API para no leer el archivo cada vez que alguien pregunte por ellas
movies_list = load_movies()

# Función para encontrar sinonimos de una palabra
def get_synonyms(word):
    # Usamos wordnet para encontrar distintas palabras que significan lo mismo
    return{lemma.name().lower() for syn in wordnet.synsets(word) for lemma in syn.lemmas()}

# Creamos la aplicación FastAPI, que será el motor de nuestra API
# Esto inicializa la API con una versión
app = FastAPI(title='mi aplicacion de peliculas', version='1.0.0')

@app.get('/', tags=['Home'])
def home():
    # cuando entremos en el navegador a http://127.0.0.1:8000 veremos un mensaje de bienvenida
    return HTMLResponse('<h1> Bienvenido a la API de peliculas </h1>')
    
# Obteniendo la lista de películas
# Creamos una ruta para obtener todas las películas
# Ruta para obtener todas las películas
@app.get('/movies', tags=['Movies'])
def get_movies():
    # Si hay películas, las enviamos, si no mostramos un error
    return movies_list or HTMLResponse(status_code=500, detail="No hay datos de películas disponibles")
# Ruta para obtener una película específica por su ID
# ruta para obtener una película específica por su ID
@app.get('/movies/{id}', tags=['Movies'])
def get_movies(id: str):
     # buscamos en la lista de películas la que tenga el mismo ID
     return next((m for m in movies_list if m ['id'] == id), {"detalle": "película no encontrada"})
# Ruta del chatbot que responde con películas segun palabras clave de la categoria
@app.get('/chatbot', tags=['chatbot'])
def chatbot(query: str):
    # Dividimos la consulta en palabras clave, para entender mejor la intension del usuario
    query_words = word_tokenize(query.lower())
    # Buscamos sinonimos de las palabras clave para ampliar la busqueda
    synonyms = {word for q in query_words for word in get_synonyms(q)} | set(query_words)
    
    # Filtramos la lista de peliculas buscando coinsidencias en la categoria
    results =[m for m in movies_list if any (s in m ['category'].lower() for s in synonyms)]
    
    # Si encontramos las peliculas, enviamos la lista de películas; sino, ostramos un mensaje de que no se encontraron cinsidencias
    
    return JSONResponse (content={
    "respuesta": "aqui tienes algunas peliculas relacionadas." if results else "no encontre peliculas en esa categoria.",
    "peliculas": results
    })
    
# Ruta para buscar películas por categoría específica
@app.get ('/movies/by_category/', tags=['Movies'])
def get_movies_by_category(category: str):
    # Filtramos la lista de películas según la categoría ingresada
    return [m for m in movies_list if category.lower() in m ['category'].lower()]