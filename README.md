**Minería de datos para texto 2017: Clusterización**
=========================================
**Karen Haag**
--------------------------
27 de septiembre del 2017
--------------------------
### 1. Introducción

En este informe detallo el proceso desarrollado para encontrar grupos de equivalencia entre palabras de un corpus, utilizando una herramienta de clustering.

EL corpus utilizado fue el de la voz, pero por falta de memoria para el ultimo caso de contextos solo utilicé parte del corpus.
Se utilizó nltk para el procesamiento del corpus, eliminación de stopwords y POS taggin, también la librería re para la limpieza de caracteres no alfabéticos. Para lematización se utilizó un diccionario en español de [lexiconista](http://www.lexiconista.com/datasets/lemmatization/). Luego para vectorizar utilicé matrices esparsas de scipy. Por último para clusterizar utilicé el algoritmo de kmeans de scikitlearn.



### 2. Pre-proceso aplicado al corpus:
Mediante nltk se tokenizó el corpus dividiendo el texto en oraciones, y cada una de estas en palabras.
Limpieza de tokens no alfabeticos mediante expresiones regulares. Unificacion del texto a minúsculas. También se eliminaron stopwords a las oraciones mediante nltk. Cabe aclarar que se utilizó el corpus con stopwords y sin ellas también para diferentes análisis.


### 3. Selección de contextos:
Se realizaron varios diccionarios de co-ocurrencia para la posterior vectorización:
1. Palabras con las que co-ocurre con ventana de 1 sin orden.
2. Palabras con las que co-ocurre con ventana de 2 sin orden.
3. Palabras con las que co-ocurre con ventana de 2 con orden.
4. Categoría gramatical con las que co-ocurre con ventana de 1 con orden.

En primera instancia se utilizaron la totalidad de los diccionarios, luego se redujo sacando las palabras que tenian menos de 5 apariciones. Al igual que los contextos que aparecian menos de 10, 50 y 100 veces. Cabe aclarar que solo se redujo mucho la dimensionalidad de los diccionarios en el diccionario de co-ocurrencia numero 4 para reducir el tiempo de ejecución mas chico, al igual que se redujo notablemente el corpus.

### 4. Vectorización:
Para la vectorizacón de cada diccionario de contexto se utilizó matrices esparsas de scipy.

### 5. Clustering:
Se utilizó el algoritmo de kmeans de scikit learn con diferentes cantidad de clusters (Entre 20 y 50) para el analisis de los datos.

### 6. Análisis de resultados
1. Utilizando de contexto palabras con las que co-ocurre con ventana de 1 sin orden:
Se utilizaron varios numeros de clusters pero no se encontraron clusters muchos significativos. La mayoría de las palabras se agrupaban en un solo cluster y el resto de los clusters tenia un solo elemento. En algunos clusters aparecían nombres propios seguramente por ser palabras que aparecían pocas veces por lo tanto tenían poca información de contextos. Tales como los que se muestran en la siguiente notebook:

```
-----------------------------
CLUSTER:  10
el
-----------------------------
CLUSTER:  11
poder
deber
-----------------------------
CLUSTER:  12
daniel
-----------------------------
CLUSTER:  13
año
-----------------------------
CLUSTER:  14
juan

...
```

2. Utilizando de contexto palabras con las que co-ocurre con ventana de 2 sin orden no se vieron cambios significativos con respecto al anterior análisis pero se pudo observar que se agrupaban mas palabras que tenian una semejanza un poco mas semántica tales como "provincia", "ciudad", "municipalidad"
 
```
-----------------------------
CLUSTER: 3
gobernar
estar
nacional
provincia
ciudad 
municipalidad
-----------------------------
...
```
3. Utilizando de contexto palabras con las que co-ocurre con ventana de 2 con orden se pudo apreciar un cluster con muchas palabras (se reflejan algunas en el CLUSTER 0), las cuales no tienen algun significado en la lengua española. También se volvieron a visualizar clusters de palabras solas y el CLuster 11  es muy parecido al cluster 3 de la iteración anterior pero un poco mas "limpio".

```
-----------------------------
CLUSTER: 0

ximas
chain
hadrian
arzuza
gimnasta
ramitas
yiddish
marlcom
rítmico
mjc
oblivion
jaurena
ciavattini
libertango
subsidiariamente
atienza
dagatti
gq
distendiéndose
seguidamente
temerles
reglarlos
sabbat
alarmarnos
autoerigió
inconvincente
antijudía
baadermeinhoff
panam
schohüchinsk
eyjafjallajökull
ñandubaysal
citröen
gürtel
-----------------------------
CLUSTER:  5
poder
deber
-----------------------------
CLUSTER:  6
estar
-----------------------------
CLUSTER:  7
bueno
-----------------------------
CLUSTER:  8
santo
-----------------------------
CLUSTER:  9
hacer
-----------------------------
CLUSTER:  10
mil
-----------------------------
CLUSTER:  11
nacional
provincia
ciudad
municipalidad
-----------------------------

...
```
4. Por último utilizando de contexto categoría gramatical con las que co-ocurre con ventana de 1 con orden:
Se pudieron apreciar clusters de tamaños más uniformes y conteniendo, por ejemplo, grupos de verbos juntos y grupos de sustantivos juntos. Pero aún así no se logra apreciar grandes resultados. 

```
-----------------------------
CLUSTER:  13
cuatro
edad
ver
tres
mil
circuito
-----------------------------
CLUSTER:  14
hacer
sutil
bueno
crecer
tratar
importante
ayer
refacción
públicamente
sentirme
mañana
caminar
-----------------------------
...
```
 ### 7. Conclusión:

Para obtener clusters que reflejen mas el conocimiento del dominio se podría incluir triplas de dependencia en la carecterización del contexto de la palabra como tarea futura.