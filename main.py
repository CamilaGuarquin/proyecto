""" 
Imagina que esta API es una biblioteca de peliculas:
La funcion load_movies() es como una biblioteca que carga el catalogo de libros (peliculas) cuando se abre la biblioteca.
La funcion get_movies() muestra todo el catalogo cuando alguien lo pide.
La funcion get_movie(id) es como si alguien preguntara por un libro especifico es decir, por un coidgo de identificacion.
La funcion chatbot (query) es un asistente que busca peliculas segun palabras clave y sinonimo.
La funcion get_movies_by_category(category) ayuda a encontrar peliculas segun su genero (accion, comedia, etc...)
"""
# Importamos las herramientas necesarias para continuar nuestra API
from fastapi import FastAPI, HTTPException # FastAPI nos ayuda a crear la API, HTTPException nos ayuda a manejar errores  # noqa: F401
from fastapi.responses import HTMLResponse, JSONResponse # HTMLResponse nos ayuda a manejar respuestas HTML, JSONResponse nos ayuda a manejar respuestas en formato JSON
import pandas as pd # pandas nos ayuda a manejar datos en tablas como si fuera un Excel
import nltk # nltk es una libreria para procesar texto y analizar palabras
from nltk.tokenize import word_tokenize # word_tokenize nos ayuda a tokenizar texto, es decir, a convertirlo en palabras
from nltk.corpus import wordnet # wordnet es una libreria para analizar sinonimos

# indicamos la ruta donde nltk buscara los datos descargados en nuestro computador
nltk.data.path.append(r'C:\Users\CAMILA\AppData\Roaming\nltk_data\tokenizers')
nltk.download('punkt') # Paquete para dividir frases en palabras
nltk.download('wordnet') # Paquete para encontrar sinonimos en palabras

# Función para cargar las peliculas  desde un archivo csv

def load_movies():
    #Leemos el archivo qur contiene información de peliculas y seleccioanmos las columnas mas importantes
    df = pd.read_csv(r"./Dataset/netflix_titles.csv")[['show_id','title','release_year','listed_in', 'rating','description']]
    
    # Renombramos las columnas para que sean más fáciles de entender
    df.columns = ['id', 'year', 'category', 'genres', 'rating', 'overview']
    
    # LLenamos los espacios vacios con texto vacio y convertimos los datos en una lista de diccionaruis 
    return df.fillna('').to_dict(orient='records')

# Cargamos las peliculas al iniciar la API para no leer el archivo cada vez que alguien pregunte por ellas
movies_list = load_movies()

# Función para encontrar sinonimos de una palabra
def get_synonyms(word):
    # Usamos wordnet para encontrar distintas palabras que significan lo mismo
    return{lemma.name().lower() for syn in wordnet.synsets_(word) for lemma in syn.lemmas()}

# Creamos la aplicación FastAPI, que sera el motot de nuestro API
# Esto inicializa la API con una versión