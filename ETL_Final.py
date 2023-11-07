import requests
import matplotlib.pyplot as ply
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import requests
import os
from datetime import datetime

os.system('clear')

#Declaramos donde se  van a guardar las imagenes que se van a ir generando a medida que el codigo corra, hay que notar que el AD es local
folder_path='/Users/julianadiaz/Documents/GitHub/MUDS/MD002_Infra'

#Declaramos el archivo PDF que se va a general al final del codigo, y especificamos el tamaño de las paginas en linea 17
pdf_file = 'ETL_Documento_Final_B4.pdf'
c = canvas.Canvas(pdf_file, pagesize=letter) 

#Descargamos un unico perfil aleatorio de la web. (No usaremos este comando puesto que nos interesa trabajar con el numero de perfiles mas grandes posibles)
Perfil = requests.get(url='https://randomuser.me/api') #podemos quitarlo

#Mediante el siguinete comando convertimos la información que nos proporciona la web (formato clase) en un diccionario, para poder trabajarlo correctamente. 
primer_usuario=Perfil.json()['results'][0]

#Utilizamos el mismo comando que anteriormente pero esta vez, solicitando datos aleatorio de 60 perfiles. 
Perfiles = requests.get(url='https://randomuser.me/api?results=100') 

#A CONTINUACION VAMOS A DECLARAR LAS VARIABLES PARA ALMACENAR LAS DISTINTAS METRICAS A GENERAR
#Creamos el diccionario para almacenar los tipos de generos y el numero de individuos de cada genero. 
#Creamos tambien las dos listas para separar posteriormente dicha información. 
database_gender = dict ()
generos=list()
generos_totales=list()

#Creamos el diccionario para almacenar las diferentes nacionalidades y el numero de individuos de cada nacionalidad. 
#Creamos tambien las dos listas para separar posteriormente dicha información. 
database_nacionalidades = dict ()
nacionalidades = list ()
nacionalidades_totales = list ()

#Creamos un diccionario extra para alacenar las diferentes nacionalidades separadas por genero masiculino y fenenino y el numero de individuos de cada nacionalidad. 
#Creamos tambien las dos listas para separar posteriormente dicha información. 
database_nacionalidad_y_genero = dict()
nacionalidades_y_genero = list ()
nacionalidades_y_generos_totales = list ()

database_horoscopos = dict()
horoscopo = list()
horoscopo_total = list()

database_edades_hombres = dict ()
database_edades_mujeres = dict ()
database_edades_mujeres['edad media mujeres']=0
database_edades_mujeres['mujeres menores']=0
database_edades_mujeres['mujeres adultas']=0
database_edades_mujeres['mujeres senior']=0
database_edades_hombres['edad media hombres']=0
database_edades_hombres['hombres menores']=0
database_edades_hombres['hombres adultos']=0
database_edades_hombres['hombres senior']=0

#El itrerador es dinamico y guarda la cantidad de los resultados
iterador = len (Perfiles.json()['results'])


#Utilizamos la variable claves_primer_usuario para averiguar cuantas claves tiene cada perfil descargado, y generar el loop que recorrera todos los diccionarios. 
claves_primer_usuario = primer_usuario.keys()
#print (claves_primer_usuario)

for x in claves_primer_usuario:
    #print ('CLAVE -> ', x)
    for y in range(iterador):
        
        """
        Mediante la siguinete linia de codigo oculta, nos guardamos la posibilidad de imprimir por pantalla de cada clave, es decir, 
        de cada tipo concreto de información (telefonos, ID, dirección, genero etc...) una lista con los valores de cada usuairo correspondientes
        a esa clave en concreto. 
        """
        #print ('Perfil ',y, ' ', Perfiles.json().get('results')[y][x])

        #CONTADOR GENEROS
        datos_generos = Perfiles.json().get('results')[y][x]
        
        if x == 'dob': 
            if Perfiles.json().get('results')[y]['gender']=='female':
                database_edades_mujeres['edad media mujeres']=database_edades_mujeres['edad media mujeres']+Perfiles.json().get('results')[y]['dob']['age']
                if Perfiles.json().get('results')[y]['dob']['age']<18:
                    database_edades_mujeres['mujeres menores']=database_edades_mujeres['mujeres menores']+1
                if Perfiles.json().get('results')[y]['dob']['age']>=18 and Perfiles.json().get('results')[y]['dob']['age']<65:
                    database_edades_mujeres['mujeres adultas']=database_edades_mujeres['mujeres adultas']+1
                if Perfiles.json().get('results')[y]['dob']['age']>=65:
                    database_edades_mujeres['mujeres senior']=database_edades_mujeres['mujeres senior']+1
            else: 
                database_edades_hombres['edad media hombres']=database_edades_hombres['edad media hombres']+Perfiles.json().get('results')[y]['dob']['age']
                if Perfiles.json().get('results')[y]['dob']['age']<18:
                    database_edades_hombres['mujeres hombres']=database_edades_hombres['hombres menores']+1
                if Perfiles.json().get('results')[y]['dob']['age']>=18 and Perfiles.json().get('results')[y]['dob']['age']<65:
                    database_edades_hombres['hombres adultos']=database_edades_hombres['hombres adultos']+1
                if Perfiles.json().get('results')[y]['dob']['age']>=65:
                    database_edades_hombres['hombres senior']=database_edades_hombres['hombres senior']+1


        if x == 'gender':
            """
            Si el tipo de genero que encontramos ya ha sido introducido como clave en el diccionario datos_generos, 
            sumamos una unidad al valor asignado dicha clave. 
            """
            if datos_generos in database_gender:
                database_gender[datos_generos]=database_gender[datos_generos]+1
            else:
                """
                Si el tipo de genero que encontramos no ha sido introducido como clave en el diccionario datos_generos, 
                guardamos la clave (genero especifico) en el diccionario y definimos el valor asignado a la clave como 1, 
                puesto que es el primer individuo de este genero que encontramos. 
                """
                database_gender[datos_generos]=1
                generos.append (Perfiles.json().get('results')[y][x])

        #CONTADOR NACIONALIDADES
        datos_nacionalidades = Perfiles.json().get('results')[y][x]

        if x == 'nat':
            """
            Utilizamos el mismo procedimiento que previamente. Si la nacionalidad que encontramos ya ha diso introducida como clave en el 
            diccionario datos_nacionalidades, sumamos una unidad al valor asignado dicha clave. 
            """
            if datos_nacionalidades in database_nacionalidades:
                database_nacionalidades[datos_nacionalidades]=database_nacionalidades[datos_nacionalidades]+1
                genero_nacionalidad=Perfiles.json().get('results')[y]['gender']
                genero_nacionalidad=datos_nacionalidades+' '+genero_nacionalidad
                if genero_nacionalidad in database_nacionalidad_y_genero:
                    database_nacionalidad_y_genero[genero_nacionalidad]=database_nacionalidad_y_genero[genero_nacionalidad]+1
                else:
                    database_nacionalidad_y_genero[genero_nacionalidad]=1
            else:
                """
                Si la nacionalidad que encontramos no ha sido introducida como clave en el diccionario datos_nacionalidades, 
                guardamos la clave (nacionalidad especifica) en el diccionario y definimos el valor asignado a la clave como 1, 
                puesto que es el primer individuo de esta nacionalidad que encontramos. 
                """
                database_nacionalidades[datos_nacionalidades]=1
                nacionalidades.append (Perfiles.json().get('results')[y][x])
                genero_nacionalidad=Perfiles.json().get('results')[y]['gender']
                genero_nacionalidad=datos_nacionalidades+' '+genero_nacionalidad

                if genero_nacionalidad in database_nacionalidad_y_genero:
                    database_nacionalidad_y_genero[genero_nacionalidad]=database_nacionalidad_y_genero[genero_nacionalidad]+1
                else:
                    database_nacionalidad_y_genero[genero_nacionalidad]=1
                  
        #CONTADOR HOROSCOPOS
        if x == 'dob':
            cadena_fecha_hora = Perfiles.json().get('results')[y][x]['date'].replace('Z','')
            fecha_hora = datetime.fromisoformat(cadena_fecha_hora)
            fecha = fecha_hora.date()
            cadena_fecha = fecha.strftime("%Y-%m-%d") #pasamos a formato string
            año, mes, dia = cadena_fecha.split('-')
            año = int(año)
            mes = int(mes)
            dia = int(dia)
            if mes == 1 and dia >= 20 or mes == 2 and dia <= 18:
                datos_horoscopo = 'Acuario'
            elif mes == 2 and dia >= 19 or mes == 3 and dia <= 20:
                datos_horoscopo = 'Piscis'
            elif mes == 3 and dia >= 21 or mes == 4 and dia <= 19:
                datos_horoscopo = 'Aries'
            elif mes == 4 and dia >= 20 or mes == 5 and dia <= 20:
                datos_horoscopo = 'Tauro'
            elif mes == 5 and dia >= 21 or mes == 6 and dia <= 20:
                datos_horoscopo = 'Geminis'
            elif mes == 6 and dia >= 21 or mes == 7 and dia <= 22:
                datos_horoscopo = 'Cancer'
            elif mes == 7 and dia >= 23 or mes == 8 and dia <= 22:
                datos_horoscopo = 'Leo'
            elif mes == 8 and dia >= 23 or mes == 9 and dia <= 22:
                datos_horoscopo = 'Virgo'
            elif mes == 9 and dia >= 23 or mes == 10 and dia <= 22:
                datos_horoscopo = 'Libra'
            elif mes == 10 and dia >= 23 or mes == 11 and dia <= 21:
                datos_horoscopo = 'Escorpio'
            elif mes == 11 and dia >= 22 or mes == 12 and dia <= 21:
                datos_horoscopo = 'Sagitario'
            elif mes == 12 and dia >= 22 or mes == 1 and dia <= 19:
                datos_horoscopo = 'Capricornio'
            if datos_horoscopo in database_horoscopos:
                database_horoscopos[datos_horoscopo]=database_horoscopos[datos_horoscopo]+1
            else:
                database_horoscopos[datos_horoscopo]=1
                horoscopo.append (datos_horoscopo)

#CONTADOR GENEROS
"""
En este apartado procedemos a separar el diccionario database_gender, en dos listas, 
una para los generos y otra para especificar le numero de inviduos de cada genero.
1. Generos totales: Diferentes generos encontrados en la base de datos.
2. Numero de inviduos de cada uno de los generos. 
"""
print ('CONTADOR GENEROS')
for a in database_gender:
    generos_totales.append (database_gender[a])  
print (generos)
print (generos_totales)

#CONTADOR EDADES
print ('MEDIA EDADES')

edad_media_mujeres = int (database_edades_mujeres ['edad media mujeres']/generos_totales[0])
edad_media_hombres = int (database_edades_hombres ['edad media hombres']/generos_totales[1])
edades_medias_calculadas=list()
edades_medias_calculadas_totales=list()
edades_medias_calculadas.append('Edad media mujeres')
edades_medias_calculadas.append('Edad media hombres')
edades_medias_calculadas_totales.append(edad_media_mujeres)
edades_medias_calculadas_totales.append(edad_media_hombres)

#METRICAS DE EDADES
print (edades_medias_calculadas)
print (edades_medias_calculadas_totales)

datos_edades_mujeres = list()
datos_edades_mujeres_totales = list ()

database_edades_mujeres ['edad media mujeres'] = edad_media_mujeres
for a in database_edades_mujeres:
    datos_edades_mujeres.append(a)
    datos_edades_mujeres_totales.append(database_edades_mujeres[a])
print (datos_edades_mujeres)
print (datos_edades_mujeres_totales)

datos_edades_hombres = list()
datos_edades_hombres_totales = list ()

database_edades_hombres ['edad media hombres'] = edad_media_hombres
for a in database_edades_hombres:
    datos_edades_hombres.append(a)
    datos_edades_hombres_totales.append(database_edades_hombres[a])
print (datos_edades_hombres)
print (datos_edades_hombres_totales)

datos_edades_combinados = list ()
datos_edades_combinados_totales = list ()

for a in range (0, 4):
    datos_edades_combinados.append(datos_edades_mujeres[a])
    datos_edades_combinados.append(datos_edades_hombres[a])
    datos_edades_combinados_totales.append(datos_edades_mujeres_totales[a])
    datos_edades_combinados_totales.append(datos_edades_hombres_totales[a])
print (datos_edades_combinados)
print (datos_edades_combinados_totales)


#CONTADOR NACIONALIDADES

"""
En este apartado procedemos a separar el diccionario database_gender, en dos listas, 
una para los generos y otra para especificar le numero de inviduos de cada genero.
1. Generos totales: Diferentes generos encontrados en la base de datos.
2. Numero de inviduos de cada uno de los generos. 
"""
print ('CONTADOR NACINOALIDADES')
for a in database_nacionalidades:
    nacionalidades_totales.append (database_nacionalidades[a])  
print (nacionalidades)
print (nacionalidades_totales)

#CONTADOR NACIONALIDADES CON GENERO INCLUIDO ORDENADO POR PAISES
print ('CONTADOR NACIONALIDADES CON GENERO INCLUIDO ORDENADO POR PAISES')

"""
En este apartado procedemos a separar el diccionario database_gender, en dos listas, 
una para los generos y otra para especificar le numero de inviduos de cada genero.
1. Generos totales: Diferentes generos encontrados en la base de datos.
2. Numero de inviduos de cada uno de los generos. 
"""
database_nacionalidad_ordenada=dict(sorted(database_nacionalidad_y_genero.items()))
for a in database_nacionalidad_ordenada:
    nacionalidades_y_generos_totales.append (database_nacionalidad_ordenada[a])  
    nacionalidades_y_genero.append (a)
print (nacionalidades_y_genero)
print (nacionalidades_y_generos_totales)

#CONTADOR NACIONALIDADES CON GENERO INCLUIDO ORDENADO POR ORDEN DESCENDENTE EN FUNCION DEL NUMERO DE INDIVIDUOS
print ('CONTADOR NACIONALIDADES CON GENERO INCLUIDO ORDENADO POR ORDEN DESCENDENTE EN FUNCION DEL NUMERO DE INDIVIDUOS')

"""
En este apartado procedemos a separar el diccionario database_gender, en dos listas, 
una para los generos y otra para especificar le numero de inviduos de cada genero.
1. Generos totales: Diferentes generos encontrados en la base de datos.
2. Numero de inviduos de cada uno de los generos. 
"""

nacionalidades_y_generos_orden_numerico_descendiente = list ()
nacionalidades_y_generos_orden_numerico_descendiente_totales = list ()

database_nacionalidad_ordenada = dict(sorted(database_nacionalidad_y_genero.items(), key=lambda item: item[1], reverse=True))
for a in database_nacionalidad_ordenada:
    nacionalidades_y_generos_orden_numerico_descendiente_totales.append (database_nacionalidad_ordenada[a])  
    nacionalidades_y_generos_orden_numerico_descendiente.append (a)
print (nacionalidades_y_generos_orden_numerico_descendiente)
print (nacionalidades_y_generos_orden_numerico_descendiente_totales)

#CONTADOR HOROSCOPOS
for a in database_horoscopos:
    horoscopo_total.append (database_horoscopos[a])  
print (horoscopo)
print (horoscopo_total)

# Realizar un diccionario para saber que paises estan en x continente
countries_by_continent = {
    "Africa": [
        "Algeria", "Angola", "Benin", "Botswana", "Burkina Faso", "Burundi", "Cameroon", "Cape Verde",
        "Central African Republic", "Chad", "Comoros", "Congo (Brazzaville)", "Congo (Kinshasa)", "Djibouti",
        "Egypt", "Equatorial Guinea", "Eritrea", "Eswatini", "Ethiopia", "Gabon", "Gambia", "Ghana", "Guinea",
        "Guinea-Bissau", "Ivory Coast", "Kenya", "Lesotho", "Liberia", "Libya", "Madagascar", "Malawi", "Mali",
        "Mauritania", "Mauritius", "Morocco", "Mozambique", "Namibia", "Niger", "Nigeria", "Rwanda", "Sao Tome and Principe",
        "Senegal", "Seychelles", "Sierra Leone", "Somalia", "South Africa", "South Sudan", "Sudan", "Tanzania", "Togo",
        "Tunisia", "Uganda", "Zambia", "Zimbabwe"
    ],
    "Asia": [
        "Afghanistan", "Armenia", "Azerbaijan", "Bahrain", "Bangladesh", "Bhutan", "Brunei", "Cambodia", "China",
        "Cyprus", "Georgia", "India", "Indonesia", "Iran", "Iraq", "Israel", "Japan", "Jordan", "Kazakhstan",
        "Kuwait", "Kyrgyzstan", "Laos", "Lebanon", "Malaysia", "Maldives", "Mongolia", "Myanmar (Burma)", "Nepal",
        "North Korea", "Oman", "Pakistan", "Palestine", "Philippines", "Qatar", "Saudi Arabia", "Singapore",
        "South Korea", "Sri Lanka", "Syria", "Tajikistan", "Thailand", "Timor-Leste", "Turkey", "Turkmenistan", "United Arab Emirates",
        "Uzbekistan", "Vietnam", "Yemen"
    ],
    "Europe": [
        "Albania", "Andorra", "Austria", "Belarus", "Belgium", "Bosnia and Herzegovina", "Bulgaria", "Croatia",
        "Cyprus", "Czech Republic", "Denmark", "Estonia", "Finland", "France", "Germany", "Greece", "Hungary", "Iceland",
        "Ireland", "Italy", "Kosovo", "Latvia", "Liechtenstein", "Lithuania", "Luxembourg", "Malta", "Moldova", "Monaco",
        "Montenegro", "Netherlands", "North Macedonia", "Norway", "Poland", "Portugal", "Romania", "Russia", "San Marino",
        "Serbia", "Slovakia", "Slovenia", "Spain", "Sweden", "Switzerland", "Ukraine", "United Kingdom", "Vatican City"
    ],
    "America": [
        "Canada", "United States", "Mexico","Belize", "Costa Rica", "El Salvador", "Guatemala", "Honduras", "Nicaragua", "Panama",
        "Argentina", "Bolivia", "Brazil", "Chile", "Colombia", "Ecuador", "Guyana", "Paraguay", "Peru", "Suriname",
        "Uruguay", "Venezuela"
    ],
    "Oceania": [
        "Australia", "Fiji", "Kiribati", "Marshall Islands", "Micronesia", "Nauru", "New Zealand", "Palau", "Papua New Guinea",
        "Samoa", "Solomon Islands", "Tonga", "Tuvalu", "Vanuatu"
    ]
}

# imprimir un ejemplo
#print(countries_by_continent["Europe"])
#definir contadores de personas por continente 

n_europe = 0
n_asia = 0
n_africa = 0
n_america = 0
n_oceania = 0

# buscar dentro de un ciclo el recuento de personas por continente dado su pais
for perfil in Perfiles.json()['results']:
    pais = perfil["location"]['country']
    
    for continente, paises in countries_by_continent.items():
        if pais in paises:
            if continente == "Europe":
                n_europe += 1
            elif continente == "Asia":
                n_asia += 1
            elif continente == "Africa":
                n_africa += 1
            elif continente == "America":
                n_america += 1
            elif continente == "Oceania":
                n_oceania += 1

# Imprime la cuenta de personas por continente
print(f"Europe: {n_europe} personas")
print(f"Asia: {n_asia} personas")
print(f"Africa: {n_africa} personas")
print(f"America: {n_america} personas")
print(f"Oceania: {n_oceania} personas")

#Variables eje X
continentes = ["Europe", "Asia", "Africa", "America", "Oceania"]
#variables eje Y
personas = [n_europe, n_asia, n_africa, n_america, n_oceania]

#EN LA SIGUIENTE SECCION COMENZAREMOS A CREAR LAS GRAFICAS Y GUARDARLAS EN EL AD LOCAL

# Crear la gráfica de barras
file_name='_personas_por_continente.png'
ply.figure(figsize=(10, 6))
ply.bar(continentes, personas, color=['blue', 'green', 'red', 'purple', 'orange'])
ply.xlabel('Continente')
ply.ylabel('Número de Personas')
ply.title('Número de Personas por Continente')
ply.savefig(folder_path+file_name)
ply.show()

png_pcontinente='/Users/julianadiaz/Documents/GitHub/MUDS/MD002_Infra'+file_name

#Analisis de generos
file_name='_total_de_generos.png'
ply.pie(generos_totales, labels=generos)
ply.title('Distribucion De Generos')
ply.savefig(folder_path+file_name)
ply.show()

png_generos='/Users/julianadiaz/Documents/GitHub/MUDS/MD002_Infra'+file_name

#Analisis de edades medias por genero
file_name='_edades_medias_genero.png'
ply.bar(edades_medias_calculadas, edades_medias_calculadas_totales)
ply.title('Edades Medias')
ply.xlabel('Genero')
ply.ylabel('Edad Media')
ply.savefig(folder_path+file_name)
ply.show()

png_edades_medias='/Users/julianadiaz/Documents/GitHub/MUDS/MD002_Infra'+file_name

#EN LA SIGUIENTE SECCION VAMOS A CREAR Y LOAD EL PDF AL CD LOCAL
#Titulo del Documento
c.setFont('Helvetica-Bold',24)
c.drawString(40, 750, "ETL - Infraestructuras de Computación")

c.setFont('Helvetica',11)
c.drawString(40, 720, "Grupo B4: Josep Oriol Sirvent Añez, Juliana M. Diaz Ochoa, Javier Hernando Calvo, Manuela Medina Gómez")
c.drawString(40, 690, "En el presente trabajo hemos analizado un total de "+str(iterador)+" perfiles. Los cuales se encuentra distribuidos de")
c.drawString(40, 675, "la siguiente manera: ")

#Primer grafico y analisis - Total hombres y total mujeres
c.drawImage(png_generos, 20, 350, width=400, height=300)
c.drawString(350, 600, "En el anterior grafico podemos ver la distribución") 
c.drawString(350, 585, "de generos en los perfiles. De "+str(iterador)+" existen")
c.drawString(350, 570, "un total de " +str(generos_totales[0])+ " hombres y un total de "+str(generos_totales[1])+ " mujeres.")
c.drawString(350, 555, "lo cual corresponde a una distribucion del " +str(round((generos_totales[0]/iterador)*100,1))+ "%")
c.drawString(350,540,"porcentaje de hombres y un total de "+str(round((generos_totales[1]/iterador)*100,1))+ "% mujeres.")

#Segundo grafico y analisis - Edades medias
c.drawImage(png_edades_medias,20,80,width=350, height=300)
c.drawString(350, 280, "Por otro lado, las edades de los generos tienen") 
#c.drawString(350, 585, "una edad media"+str(iterador)+" existen")
#c.drawString(350, 570, "un total de " +str(generos_totales[0])+ " hombres y un total de "+str(generos_totales[1])+ " mujeres.")
#c.drawString(350, 555, "lo cual corresponde a una distribucion del " +str(round((generos_totales[0]/iterador)*100,1))+ "%")
#c.drawString(350,540,"porcentaje de hombres y un total de "+str(round((generos_totales[1]/iterador)*100,1))+ "% mujeres.")

# Create a new page
c.showPage()

# Add content to the second page
c.drawString(100, 750, "This is the second page of the PDF.")
c.drawImage(png_pcontinente, 100, 500, width=400, height=300)
# Remember to save the changes after adding content to each page
c.save()