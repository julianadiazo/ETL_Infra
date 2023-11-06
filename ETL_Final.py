import requests
import matplotlib.pyplot as ply
import matplotlib as mat
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

folder_path='/Users/julianadiaz/Documents/GitHub/MUDS/MD002_Infra'
file_name='/example.png'

pdf_file = "my_document.pdf"
c = canvas.Canvas(pdf_file, pagesize=letter)

database = dict ()
database1 = dict ()
generos=list()
generos_totales=list()
nacionalidades = list ()
nacionalidades_totales = list ()

Perfil = requests.get(url='https://randomuser.me/api')
Perfiles = requests.get(url='https://randomuser.me/api?results=66') 


primer_usuario=Perfil.json()['results'][0]

claves = primer_usuario.keys()

print(Perfil.json().get('results')[0]['name'])
total_males=0
total_females=0
age_med=0

iterador = len (Perfiles.json()['results'])

my_dict=dict()

for x in claves:
    print ('-------CLAVE -> ', x)
    for y in range(iterador):
        
        print ('Perfil ',y, ' ', Perfiles.json().get('results')[y][x])

        #CONTADOR GENEROS
        datos_generos = Perfiles.json().get('results')[y][x]
        if x == 'gender':
            if datos_generos in database1:
                database1[datos_generos]=database1[datos_generos]+1
            else:
                database1[datos_generos]=1
                generos.append (Perfiles.json().get('results')[y][x])

        #CONTADOR NACIONALIDADES
        datos_nacionalidades = Perfiles.json().get('results')[y][x]
        if x == 'nat':
            if datos_nacionalidades in database:
                database[datos_nacionalidades]=database[datos_nacionalidades]+1
            else:
                database[datos_nacionalidades]=1
                nacionalidades.append (Perfiles.json().get('results')[y][x])
        if x=='dob':
            print('Perfil ',y, ' ', Perfiles.json().get('results')[y][x]['age'])


#CONTADOR GENEROS
print ('CONTADOR GENEROS')
for a in database1:
    generos_totales.append (database1[a])  
print (generos)
print (generos_totales)

#CONTADOR NACIONALIDADES
print ('CONTADOR NACINOALIDADES')
for a in database:
    nacionalidades_totales.append (database[a])  
print (nacionalidades)
print (nacionalidades_totales)

ply.pie(generos_totales, labels=generos)
ply.savefig(folder_path+file_name)
ply.show()

ply.bar(nacionalidades, nacionalidades_totales)
ply.title('title name')
ply.xlabel('x_axis name')
ply.ylabel('y_axis name')
ply.show()

print(age_med)

image_path='/Users/julianadiaz/Documents/GitHub/MUDS/MD002_Infra/example.png'
#c.drawImage(image_path, 100, 500, width=400, height=300)
c.drawString(100, 750, "Hello, this is my PDF document with a Matplotlib plot!")
c.drawString(100, 720, "You can add Matplotlib plots and more.")

# Create a new page
c.showPage()

# Add content to the second page
c.drawString(100, 750, "This is the second page of the PDF.")
c.drawImage(image_path, 100, 500, width=400, height=300)
# Remember to save the changes after adding content to each page
c.save()
