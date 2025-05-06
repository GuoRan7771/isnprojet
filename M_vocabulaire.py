

import csv



class Vocabulaire :

        def __init__(self,français, anglais): 
            self.french = français
            self.anglais= anglais
            self.poids=50
            self.occurence=0

        def __str__(self):
             return (f"le mot {self.anglais} signifiant {self.french} a un poids de {self.poids} et a été vu {self.occurence} fois. ")



with open('vocab.csv', newline='') as csvfile:

    vocab = csv.reader(csvfile, delimiter=';', quotechar='|')
    Flash_all=[]
    for row in vocab:
        carte = Vocabulaire(row[0],row[1])   #creation de l'objet carte 
        Flash_all.append(carte)            #stockage des objets 
        print(carte)                       # affichage pour verifier que l'objet est créé
    



        