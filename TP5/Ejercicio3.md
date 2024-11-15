# **Ejercicio programa de radio**
## Esquema Base de Datos
### Programa <radio, año, programa, conductor, gerente, frecuencia_radio>

##### Restricciones:
- ***a***. Una radio se transmite por una única frecuencia (frecuencia_radio) en un año
determinado, y puede cambiarla en años diferentes.
- ***b***. Cada radio tiene un único gerente por año, pero el mismo gerente puede repetirse en la
misma radio en diferentes años. Y la misma persona puede ser gerente de diferentes
radios durante el mismo año.
- ***c***. Un mismo programa puede transmitirse por varias radios y en diferentes años.
- ***d***. Un programa transmitido en una radio en un año determinado tiene un solo conductor.




 
### Paso 1: Determinar las Dependencias Funcionales (DFs)
A partir del esquema y las restricciones dadas, podemos determinar las siguientes dependencias funcionales:

- 1 . radio, año-> frecuencia_radio: una radio transmite en una sola frecuencia en un año determinado, lo cual implica que **radio** y **año** determinan la **frecuencia_radio**.
- 2 . radio, año -> gerente: cada radio tiene un unico gerente por año, lo que significa que **radio** y **año** determinan al **gerente**.
- 3 . radio, programa, año -> conductor: un programa transmitido en una radio en un año determinado tiene un unico conductor. Esto significa que **radio**, **programa** y **año** determinan al **conductor**.

### Paso 2: Determinar las Claves Candidatas
Para determinar las claves candidatas, necesitamos encontrar un conjunto de atributos que puedan identificar de manera única a cada fila de la tabla PROGRAMA.

En este caso, podemos ver que:
- La combinacion de ***(radio, programa, año)*** es suficiente para identificar de forma unica cada registro en la tabla, ya que: 

    - ***radio*** y ***año*** juntos determinan la ***frecuencia_radio*** y el ***gerente***.

    - ***radio***, ***año*** y ***programa*** juntos determinan el ***conductor***.

Por lo tanto, la ***clave candidata*** es: 
- ***(radio, programa, año)***

### Paso 3: Diseño en Tercera Forma Normal (3FN)

Diseño en 3FN: 
1. ***Tabla Radio_Frecuencia*** 

    - radio (Clave foránea que referencia a Radio)
    - año
    - frecuencia_radio
    - Clave primaria compuesta: (***radio, año***)

2. ***Tabla Radio_Gerente***
    - radio (Clave foránea que referencia a Radio)
    - año
    - gerente
    - Clave primaria compuesta: (***radio, año***)


3. ***Tabla Programa_Conductor***

    - radio (Clave foránea que referencia a Radio)
    - año
    - programa (Clave foránea que referencia a Programa)
    - conductor
    - Clave primaria compuesta: (***radio, año, programa***)

4. ***Tabla Radio***
    - radio (Clave primaria)

5. ***Tabla Programa***
    - programa (Clave primaria)

