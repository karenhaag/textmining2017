**Minería de datos para texto 2017: Feature Selection**
=========================================
**Karen Haag**
--------------------------
6 de Octubre del 2017
--------------------------
### 1. Introducción

En este informe detallo el proceso desarrollado para utilizar técnicas de Feature Selection para reducir dimensionalidad a espacios que luego se utilizarán para realizar una tarea de clustering.

Se utilizaron dos corpus para distintos experimentos. Por un lado 10000 oraciones del corpus no anotado del diario La Voz del Interior y por otro una parte del Wikicorpus en español, un corpus anotado que contiene por cada palabra del corpus lematización, part of spech y sentidos asociados a las palabras.
Se utilizó nltk para el procesamiento del corpus, eliminación de stopwords y POS taggin en el corpus no anotado, también la librería re para la limpieza de caracteres no alfabéticos. Para lematización  se utilizó un diccionario en español de [lexiconista](http://www.lexiconista.com/datasets/lemmatization/). Para reduccíon de dimensionalidad se utilizó LSA en el corpus no anotado y en el anotado también y SelectKBest de Scikit Learn solo para el corpus anotado. Luego para vectorizar utilicé Dicvectorizer de Scikit Learn. Por último para clusterizar utilicé el algoritmo de kmeans de Scikit Learn.

### 2. Descripción del sampleo del corpus anotado
El corpus Wikicorpus contiene una gran porción de la wikipedia, cuenta con más de 750 millones de palabras pero se utilizó solo una parte de este para trabajar. Cada linea del corpus puede ser o bien una linea de código html, o bien una linea que se compone de:
Palabra, lemma de la palabra, POS taggin de la palabra y sentido de la palabra.
Cabe aclarar que la palabra puede ser una palabra del lenguaje español o un signo de puntuación.
Por lo tanto:
1. Se dividió el texto en listas de líneas.
2. Cada lista de linea se dividió a la vez en lista de componentes de la linea(Palabra, lemma, POS taggin, sentido) filtrando las que contenían numeros en la componente "palabra" o caracteres especiales. Solo se dejaron palabras que esten compuestas de caracteres alfabéticos o también puntos, para poder separar en oraciones.
3. Finalmente se construyó una lista de "oraciones" para poder facilitar la selección de features. 

### 3. Descripción del sampleo del corpus no anotado
Mediante nltk se tokenizó el corpus dividiendo el texto en oraciones, y cada una de estas en palabras.
Limpieza de tokens no alfabeticos mediante expresiones regulares. Unificacion del texto a minúsculas. También se eliminaron stopwords a las oraciones mediante nltk. Cabe aclarar que se utilizó el corpus con stopwords y sin ellas también para diferentes análisis.

### 4. Descripción de las librerías utilizadas
Para feature selection supervisado se utilizó la librería SelectKBest de Scikit Learn que implementa un algoritmo de feature selection que selecciona features con respecto a las k puntuaciones más altas. En este caso la "puntuación" se la da la función chi2 de scikit learn que calcula las estadísticas chi-cuadrado entre cada feature y las clases.
También se utilizó TruncatedSVD de Scikit Learn para reducción de dimensionalidad no supervisada. Esta función toma la dimensión deseada de los datos de salida, que debe ser estrictamente inferior al número de features y algunas opciones como numero de iteraciones, algoritmo a utilizar, etc. que por simplicidad se utilizaron las que venían por defecto.
 
### 5. Preparacíon de los espacios 
Luego del sampleo de los corpus, se los utilizó para armar el vector de cada palabra en base a los contextos en los que aparecían. Para los features se utilizó: lema, palabra anterior y posterior con la que ocurría,taggin de la palabra anterior y posterior con las que ocurría, sentido de la palabra, sentido anterior y posterior de las palabras con las que ocurria.

### 6. Descripción de la técnica supervisada de feature selection
Para esta técnica se armó además una lista de las clases a la que pertenecía cada uno de los vectores de palabras, así luego dárselo como parámetro al algoritmo de feature selection supervisado para que haga la reducción de dimensionalidad. Las clases estaban basadas respecto a la categoría morfosintáctica a la que pertenecía cada palabra. 
Este algoritmo devuelve la matriz reducida con una cantidad de k features con respecto a la función chi2. Chi2 se utiliza para seleccionar los features con los valores más altos para la estadística de chi-cuadrado de prueba de la matriz de features, que debe contener únicamente features no negativos tales como booleanos o frecuencias (por ejemplo, conteos de cantidad de frecuencia encontrada de una palabra en un texto).

### 7. Descripción de la técnica no supervisada de feature selection
Se utilizó TruncatedSVD de Scikit Learn. Este transformador realiza reducción de dimensionalidad lineal por medio la descomposición de valor singular(LSA). Esta librería nos permite trabajar con matrices esparsas de scipy eficientemente.

### 8. Análisis de los resultados
Se decidió no usar el corpus procesado anteriormente para clustering(la voz). Para ver mejor la diferencia de los clusters se prefirió utilizar las diferentes dimensionalidades aplicadas al corpus de Wikicorpus.

1. Utilizando los espacios sin reducción de dimensionalidad se utilizaron varios numeros de clusters pero no se encontraron clusters muy significativos. La mayoría de las palabras se agrupaban en un solo cluster y el resto de los clusters tenia un solo elemento. EL proximo notebook muestra algunos de los clusters obtenidos utilizando 30 clusters en el algoritmo kmeans. 

```
------------------------------
CLUSTER : 0
santo
mayordomo
palacio
Hispania
Omeyas
sunes
chies
omeyas
acceden
califato
islmico
Al
muri
traicionado
suyos
monje
annimo
realiza
monte
Fuji
Japn_Nacimientos
artculo
trata
------------------------------
CLUSTER : 16
como
------------------------------
CLUSTER : 2
es
------------------------------
...
```
2. Utilizando los espacios con reducción de dimensionalidad LSA reduciendo las componentes a 45 features. Se utilizaron varios números de clusters y se redujeron la cantidad de clusters con una sola palabra, pero aún siguen habiendo algunos. También se notó que se agruparon en el cluster 0 palabras similares que en el cluster 0 mostrado en el notebook anterior. Al igual que se hicieron clusters con ciudades de españa como se muestran en el cluster 19.


```
CLUSTER : 0
santo
espaol
mayordomo
palacio
Neustria
ltima
reina
visigoda
Hispania
Omeyas
sunes
chies
omeyas
acceden
califato
islmico
Al
muri
traicionado
suyos
monje
annimo
realiza
primera
escalada
monte

----------------------------------------
CLUSTER : 27
franco
poder
asesinado
bizantino
astrnomo
convierte
reino
primer
rabes
noble
reinado
nombre
----------------------------------------
CLUSTER : 24
Los
Se
El
En
------------------------------
CLUSTER : 23
Fulgencio_de_cija
Erquinoaldo
Egilona
Fin_de_el_Califato_Perfecto
Califato_de_Damasco
Divisin
Mundo
Un
Snodo_de_Whitby
Este
C._Para
La
Constante_II
Chilperico_II
Brahmagupta
Wamba
Adeodato_II
Vitaliano
Recesvinto
Clotario_III
Childerico_II
Dono
San_Agatn
Aisha
Ervigio
Hussein
XII_Concilio_de_Toledo
Agatn
San_Len_II
Len_II
San_Benedicto_II
Abd
Juan_V
Benedicto_II
Conn
Carlos_Martel
------------------------------------------------
CLUSTER : 19
su
Espaa
contra
Asturias
que
Galicia
Inglaterra
Crdoba
Castilla
Len
------------------------------------------------

...
```

3. Utilizando los espacios con reducción de dimensionalidad con la técnica no supervisada de reduciendo las componentes a 10 features. Se observó mucha diferencia con respecto a los otros clusters. Los datos estan más dispersos pero también se encontraron clusters de una sola palabra. Por ejemplo en los clusters 5, 6 y 7. Observando el corpus se pudo entender que esas palabras se tomaban como oraciones de una sola palabra ya que luego de ellas había un punto y el algoritmo las clusterizó por separado a cada una. Luego en el cluster 28 se encuentran algunas Stopwords.

```
...................................
CLUSTER : 0
Acontecimientos
santo
ltima
Los
islmico
los
asesinado
otros
La
historia
bizantino
despus
su
Espaa
nieto
mrtir
chi
un
sur
------------------------------
CLUSTER : 5
Acontecimientos
------------------------------
CLUSTER : 6
Fallecimientos
------------------------------
CLUSTER : 7
ENDOFARTICLE
------------------------------
CLUSTER : 10
Fulgencio_de_cija
espaol
Erquinoaldo
franco
palacio
Neustria
Egilona
visigoda
Hispania
-----------------------
CLUSTER : 28
por
con
ibn
----------------------
...
```