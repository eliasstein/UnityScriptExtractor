import glob,json,time,re,os

def extractText():
    for x in glob.glob("Scripts_originales/*.txt"):        #Recorre los scripts originales para extraerlos
        file=open(x,"r",encoding="utf-8")       #Abrimos el archivo de texto
        file_len=len(file.readlines())          #Contiene la longitud de lineas del documento de texto
        file.seek(0)                            #Posicionamos el indice a la posicion 0 nuevamente

        strArray=[]                             #Array/Vector donde se almacenaran los textos extraidos
        jsonfile={}                             #Diccionario necesario para guardarlo en formato json
        for index in range(0,file_len):         #Recorremos todas las lineas
            line=file.readline()                #Almacenamos el contenido de la linea de texto en una variable

            if(line.find("m_Name")!=-1):        #Offset del Titulo del archivo
                title=line[line.find("=")+3:-2]   #Almacenamos el titulo en una variable
                strArray.clear()                  #Vaciamos el arreglo en caso de que tenga algun valor almacenado de la iteracion anterior

            elif(line.find("string data")!=-1): #Offset de los strings del archivo
                text=line[line.find("=")+3:-2]    #Almacenamos el texto en una variable
                if(len(text)>2 and len(re.findall(u'[\u2E80-\u9fff]+', text))==0):                #Si el string no esta vacio y no tiene caracteres asiaticos
                    strArray.append(text)           #Lo almacenamos en el arreglo

        jsonfile={title:strArray}   #Una vez se termina de recorrer el archivo se lo guarda en formato json
        fwrite=open("Extracted/"+title+".json",'w',encoding='utf-8')    #Creamos un archivo en la carpeta extracted con codificacion utf-8
        json.dump(jsonfile,fwrite,indent=4,ensure_ascii=False)          #Lo guardamos en formato json
        fwrite.close()
    menu()

def replaceText():
    for x in glob.glob("Scripts_originales/*.txt"): #Recorremos los archivos de la carpeta scripts originales
        file=open(x,"r",encoding="utf-8")       #abrimos el archivo de texto que contiene el script original
        file_len=len(file.readlines())          #contiene la longitud de lineas del documento de texto
        file.seek(0)                            #Posicionamos el indice a la posicion 0 nuevamente

        fileContent=[]                          #Creamos un arreglo/Vector para poder almacenar las lineas y las lineas modificadas
        extractedIndex=0                        #Inicializamos el indice del archivo json en 0 para iterar por cada linea modificada del archivo

        for index in range(0,file_len):         #Recorremos todas las lineas
            line=file.readline()                #Almacenamos el contenido de la linea de texto en una variable
            
            if(line.find("m_Name")!=-1):        #Offset del Titulo del archivo
                title=line[line.find("=")+3:-2]   #Almacenamos el titulo en una variable
                extracted=json.load(open("Extracted/"+title+".json","r",encoding="utf-8"))  #Abrimos el archivo de la carpeta extracted 
                fileContent.append(line)    #Almacenamos la cadena de texto sin ninguna modificacion

            elif(line.find("string data")!=-1): #Offset de los strings del archivo
                text=line[line.find("=")+3:-2]    #Almacenamos el texto en una variable
                if(len(text)>2 and len(re.findall(u'[\u2E80-\u9fff]+', text))==0):       #Si el string no esta vacio y no tiene caracteres asiaticos
                    fileContent.append(line.split("=")[0]+"= \""+extracted[title][extractedIndex]+"\"\n")           #Almacenamos el texto modificado en el script original
                    extractedIndex+=1       #Modificamos el indice del archivo json
                else:                       #En caso que el caracter sea asiatico o vacio
                    fileContent.append(line)    #Almacenamos la linea de texto sin ninguna modificacion
            else:                           #En caso de que no sea un texto valido ni un titulo
                fileContent.append(line)    #Lo almacenamos en el arreglo

        save=open("Patched/"+x[19:],"w+",encoding="utf-8")  #Creamos un archivo en la carpeta patched
        for i in fileContent:                               #Recorremos el arreglo
            save.write(i)                                   #Guardamos los textos del arreglo en el archivo patched
        save.close()                                        #Cerramos el archivo
        extractedIndex=0                                    #Reinicializamos el indice a 0
        fileContent.clear()                                 #Borramos el contenido del arreglo
    menu()

def help():
    os.system("cls")
    print("Tutorial:\n\nTutorial basico sobre como utilizar la herramienta. Colocaremos los scripts en la carpeta")
    print("\"Scripts_originales\" luego ejecutaremos la primera opcion del menu \"1-Extraer texto\" esta opcion")
    print("Extraera los textos de los scripts en la carpeta Extracted en donde podran ser traducidos sin ningun problema")
    print("Una vez realizada la traduccion ejecutar la segunda opcion del menu la de \"2-Reemplazar texto\"")
    print("Esta insertara los textos modificados en el script original y guardara la modficacion en la carpeta \"Patched\"")
    input()
    menu()


def menu():
    os.system("cls")
    print("----UnityToolByKuta----\n\nMenu:\n 1-Extraer texto\n 2-Reemplazar texto\n 3-Tutorial\n 4-Salir")
    try:
        option=int(input()) 
    except:
        print("El valor introducido debe ser de tipo numerico.")
        input()
        menu()
    if(option==1):      
        extractText()
    elif(option==2):
        replaceText()
    elif(option==3):
        help()
    elif(option==4):
        return 0
    else:
        print("La opcion introducida es invalida por favor ingrese una opcion valida")
        input()
        menu()

if __name__ == '__main__':
    menu()