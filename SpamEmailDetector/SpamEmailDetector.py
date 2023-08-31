# -*- coding: utf-8 -*-
"""
Created on Mon Aug 21 23:49:08 2023

@author: rafae
"""
from email_data_preprocessor import *
from tkinter import filedialog

#En email_data_preprocessor ya tenemos todo el data preprocessing resource, pero hacen
#falta dos funciones más
def parse_index(path_to_index, n_elements): 
    ret_indexes = []
    index = open(path_to_index).readlines()
    for i in range(n_elements):
        mail = index[i].split(" ../")
        label = mail[0]
        path = mail[1][:-1]
        ret_indexes.append({"label": label, "email_path":path})
    return ret_indexes #Esta función devuelve un diccionario con dos categorías: "label" y "email_path"
def parse_email(index):
    p = Parser() #aquí utilizamos la clase Parser que viene en la librería email_data_preprocessor
    pmail = p.parse(index["email_path"]) #aquí utilizamos el método ".parse()" que viene en la librería email_data_preprocessor recordemos que recibe un email file como input
    return pmail, index["label"] #Esta función devuelve dos valores: el contenido del email(incluyendo body y subject), y la label (si es spam o no)


#Algunas funciones para ajustar el formato de rutas de windows
def filename_extractor(falsepath):
    corrector = falsepath.split(r"/") 
    filename = corrector[-1] #data/inmail.8 al partirse en dos, queda ["data", "inmail.n"] sólo nos interesa el último, por eso el -1
    return filename
def empth_replacer(index):
    e = 0
    for i in index:
        filename = filename_extractor(index[e]["email_path"])
        em_pth = emails_path + fr"\{filename}"
        index[e]["email_path"] = em_pth
        e+=1
    return index


"""
Okay, Now here starts our code
"""
#Declare the paths of our main files: index, and emails
index_path = r"C:\Users\rafae\Downloads\5_Regresión+Logística+-+Detección+de+SPAM.ipynb\trec07p\full\index"
emails_path = r"C:\Users\rafae\Downloads\5_Regresión+Logística+-+Detección+de+SPAM.ipynb\trec07p\data"

index = parse_index(index_path, 10) #preprocess data. Within the parse method there is already an open and read command.
index = empth_replacer(index)  #Let's correct the format of the email's path

#print(index)

""" 
At this point, we have just what we need. 
a path (index[0]["email_path"]) and a label (index[0]["label"]). 
Now we have a decent dataset that says that email index[0]["email_path"] is spam or not (index[0]["email_path"] cool isn't it?
"""

#Leemos el primer correo 
open(index[0]["email_path"]).read()
"""
Remember here you have a list so you need [] to specify the element position, 
and the elements of that list are dictionaries, so you need another [] to indicate where in that dictionary are located.
""" 
#As you can see this is Raw data. It means, it is chaotic. unfiltered. hard to use. Let's pre process it:

    #Parseemos este primer correo
mail, label = parse_email(index[8]) #Aquí index [] es la lista, y index[i] ya es un diccionario
print(mail)
print("El correo es: ", label) #Good trick isn't it?

#Let's now talk serious.

#Aplicación de CountVectorizer
from sklearn.feature_extraction.text import CountVectorizer
#preparación del email en una cadena de texto
prep_email = [" ".join(mail["subject"]) + " ".join(mail["body"])]

vectorizer = CountVectorizer()
X = vectorizer.fit(prep_email)
print("Email: ", prep_email, "\n")
print("Caracteristicas de entrada: ", vectorizer.get_feature_names_out())
#CountVectorizer It basically turns non numeric values into actual numeric values.
#NOTA
#en el video de Udemy se usa vectorizer.get_feature_names() ; pero en 
#Versiones más recientes de sklearn, el método correcto es vectorizer.get_feature_names_out()
X = vectorizer.transform(prep_email)
print("\nValues:\n", X.toarray())#el método .toarray() nos devuelve un numpy array lleno con los valores del email

#Now an auxiliar function for the dataset preprocessing (we need a paired X,y or labeled data in order to proceed with the training)
def create_prep_dataset(index_path, n_elements):
    X = []
    y= []
    indexes = parse_index(index_path, n_elements)
    indexes = empth_replacer(indexes)
    for i in range(n_elements):
        print("\rParsing email:", i, " "*5, end='')
        mail, label = parse_email(indexes[i])
        X.append(" ".join(mail["subject"]) + " ".join(mail["body"]))
        y.append(label)
    return X,y

#Leemos unicamente un subconjunto de 100 correos electrónicos
X_train, y_train = create_prep_dataset(index_path, 100)
X_train
#Ahora aplicamos la vectorización a los datos
vectorizer = CountVectorizer()
X_train = vectorizer.fit_transform(X_train)

print(X_train.toarray())
print("\nFeatures: ", len(vectorizer.get_feature_names_out()))

# pandas will help us with data visualization
import pandas as pd
pd.DataFrame(X_train.toarray(), columns=[vectorizer.get_feature_names_out()])

#Ahora sí, entrenemos nuestro algoritmo
from sklearn.linear_model import LogisticRegression #usaremos el módulo "LogisticRegression" porque estamos clasificando
clf = LogisticRegression() #creaos un objeto de tipo LogisticRegression.Este será nuestro ML model
clf.fit(X_train, y_train) #aplicamos la función "Fit" (refer to ML concepts to know what fitting means) y para hacer fit necesitamos datos de entrada paireados.
#en este caso, el conjunto de correos X_train,, y el conjunto de clasificaciones "predicciones" de estos correos conocidos.

#Lectura de un conjunto de correos
#Leemos 150 correos de nuestro conjunto de datos y nos quedamos unicamente con los 50 últimos
X,y = create_prep_dataset(index_path, 150) #recordemos que create_prep_dataset is basically the function we created to do all that is described between lines 
X_test = X[100:]
y_test = y[100:]

#aquí lo que hicimos fue leer 150 elementos y tomar 100 para los tests. 
