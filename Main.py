# -*- coding: utf-8 -*-
#################################################################################################################################################################
#########################################################################      PARTIE IMPORT  ###################################################################
#################################################################################################################################################################
import random
import sys
import math
import numpy as np
from numpy import linalg as LA

#Importer les scripts qu'on va utiliser par la suite.
#script qui gère la lecture et écriture des fichiers ainsi que générer des données aléatoires.
import lecture_ecriture as gestion

#script qui sert à executer de beaux tests ( essayer les données a 2D pour voir)
import test




#################################################################################################################################################################
#########################################################################      PARTIE INPUT  ###################################################################
#################################################################################################################################################################

print("Bonjour , Bienvenue dans le programme K-Means ")
print("si vous voulez entrer vos propres données appuyez sur 1")
print("si vous voulez faire une simulation iris appuyez sur 2")
print("si vous voulez une simulation quelconque appuyez sur 3 ( essayer en 2D pour de beaux graphiques :p)")


queltype=int(input())

#Si l'utilisateur choisit de charger ses propres données
if queltype==1:
        print("vérifier que le fichier d'entrée est dans le même dossier que le script ")
        fichier_entree=str(input("donner le nom de votre fichier (format csv)   "))
        fichier_de_sortie=str(input("donner le nom du fichier de sortie   "))



        
        #########################################################
        ############## Zone Distance ############################
        #########################################################

        print("choisissez le type de distance que vous voulez")
        print("tapez 1 pour Euclidienne")
        print("tapez 2 pour Euclidienne standarisée")
        print("tapez 3 pour Minkowski")
        print("tapez 4 pour Tchebychev")
        distance=int(input())

        if distance==1:
                distance="Euclidienne"
        
        if distance==2:
                distance="Euclidienne standarisée"
                print("inserer votre vecteur de standarisation")
                vecteur=[float(x) for x in input().split()]
        
        if distance==3:
                distance="Minkowski"
                puissance=int(input("choisissez la puissance  "))
        
        if distance==4:
                distance="Tchebychev"
        
        ###########################################################
        ##########################################################     
        nombre_de_centres=int(input("nombre de centres   "))
        condition=int(input("si vous voulez nominer vos centres appuyer sur 1 , sinon appuyer sur 2   "))
        
        #cette partie sert à stocker les différents noms des groupes 
        if condition==1:
                Numeros=[]
                i=1
                while i<(nombre_de_centres+1):
                        num=str(input("donner le nom du centre %s  "%i))
                        Numeros+=[num]
                        i+=1   

if queltype==2:
        fichier_entree="iristest.csv"
        fichier_de_sortie="resultat.csv"
        distance="Euclidienne standarisée"     
        vecteur=[0.7826,-0.4194,0.9490,0.9565]
        nombre_de_centres=3
        condition=0
                                         
#Si l'utilisateur choisit de faire une simulation
if queltype==3:
        

        nombre_de_donnes=int(input("saisissez le nombre de données  "))
        nombre_de_coordonnees=int(input("saississez le nombre de coordonnees   "))
        nombre_de_centres=int(input("nombre de centres   "))
        distance="Euclidienne"

                
#Condition d'arrêt
condition_arret=float(input("entrer la condition d'arret ( le maximum de variation de centre)  "))

#################################################################################################################################################################
#########################################################################      PARTIE CLASSES ###################################################################
#################################################################################################################################################################

# une classe de Groupes  , une classe de Calcul

#Cette classe sert à effectuer toute sorte de calcul nécéssaire pour notre algorithme.
#on choisit une norme 'Euclidienne' mais au lieu de prendre les distances au carré , on les prend à la puissance 8 pour un meilleur résultat

class calcul:

    #on initialise par défaut nos attributs de type de distance et de calcul du centre d'un groupe
    distance=""
    typeCentre="Barycentre"
    #notre constructeur
    def __init__(self,distance):
        self.distance=distance

    #########################################################################################################################
    ################################# C'est ici que vous pouvez ajouter une distance entre 2 points #########################  
    #########################################################################################################################  
    #méthode qui sert à calculer la distance entre 2 points    
    def calculDistanceEntre2points(self,point1,point2):
        #on vérifie que les 2 points ont déjà le même nombre de coordonnées
        assert len(point1)==len(point2) ,"%r n'as pas la même dimensio que %r" (point1,point2)
        #on initialise une variable de calcul
        self.D=0
        self.L=[]
        #Cette partie cherche à calculer une distance Euclidienne
        if self.distance=="Minkowski":
            
            for i in range(1,len(point1)):
                self.D+= math.pow(point1[i]-point2[i],puissance)
            self.D=math.pow(self.D,1.0/puissance)
            return self.D

        if self.distance=="Euclidienne":
                for i in range(1,len(point1)):
                        self.D+= math.pow(point1[i]-point2[i],2)
                        self.D=math.pow(self.D,1.0/2)
                return self.D      
              
        if self.distance=="Euclidienne standarisée":
        
            v=vecteur
            for i in range(1,len(point1)):
                self.D+= v[i-1]*((point1[i]-point2[i])**2)
            self.D=self.D**1/2
            return self.D

        if self.distance=="Tchebychev":
                
                for i in range(1,len(point1)):
                        self.L+=[abs(point1[i]-point2[i])]
                return(max(self.L))
                        
    #méthode qui sert à calculer la distance entre le centre d'un groupe et un pour quelconque
    def calculDistanceAuCentre(self,Groupe,point):
        return(self.calculDistanceEntre2points(Groupe.centre,point))

    
    #méthode qui sert à calculer le centre d'un groupe
    def calculCentre(self,Groupe):
        #on vérifie déjà que le groupe est non vide
       
        assert len(Groupe.groupe)!=0 ,"le groupe %r est vide"%(Groupe.numero)
        
        #On initialise un point qui servira de nouveau centre
        self.NewCenter=[0]*len(Groupe.groupe[0])
        #Cette partie cherche à calculer le barycentre classique non pondéré
        if self.typeCentre=="Barycentre":
            for i in range(1,len(Groupe.groupe[0])):
                for j in range(0,len(Groupe.groupe)):
                    self.NewCenter[i]+=Groupe.groupe[j][i]
                self.NewCenter[i]=self.NewCenter[i]/(len(Groupe.groupe))
        return self.NewCenter 
        
    
    #méthode qui sert à calculer la distance minimale entre les points et les groupes et affecter chaque point au groupe correspondant.
    def CalculAffectation(self,StockDeGroupes,Data):
        #on initialise une liste d'affectation vide
        self.Affectation=[0]*len(Data)
        #on initialise une variable de calcul pour calculer la distance entre un point et TOUS les centres
        self.distancesAuCentre=[0]*len(StockDeGroupes)
        #on initialiser une variable de calcul pour sauvegarder l'index du minimum de distances
        self.minimumDistance=0
        #on parcourt la liste de données
        for i in range(0,len(Data)):
            #on parcourt la liste des groupes
            for j in range(0,len(StockDeGroupes)):
                #on calcule les distances aux centres de ces groupes
                self.distancesAuCentre[j]=self.calculDistanceAuCentre(StockDeGroupes[j],Data[i])
            #on stock l'index du minimum ici
            self.minimumDistance=self.distancesAuCentre.index(min(self.distancesAuCentre))
            #on cherche le groupe correspondant et on y affecte le point
            self.Affectation[i]=StockDeGroupes[self.minimumDistance].numero
        return self.Affectation


    #méthode pour calculer la norme de 2 vecteurs    
    def calculNorme(self,a,b):
        self.L=[a_i - b_i for a_i, b_i in zip(a, b)]
        return LA.norm(self.L)
        
########################################### On instancie la première classe pour faire le traitement sur les groupes #############################################


calculette=calcul(distance)


###################################################################################################################################################################

# On considère les groupes comme des objets , donc on se sert d'une classe pour initialiser nos groupes et gérer les principales méthodes associés

class Groupe:
    # il nous faut un numéro, un centre de groupe et les points qu'il contient pour bien le définir    
    numero=0
    groupe=[]
    centre=[]
    
    #On utilise le constructeur pour définir le numéro et le centre ( il ne contient pas de points à priori au début)
    def __init__(self,numero,centre):
        self.numero=numero
        self.centre=centre
        self.groupe=[centre]
        
    #méthode qui sert à ajouter les points    
    def ajouterPoint(self,point):
        self.groupe+=[point]
    
    
    #méthode qui sert à modfier les centres    
    def modifierCentre(self,centre):
        self.centre=centre
    
    #méthode qui sert à modifier le groupe
    def modifierGroupe(self,groupe):
        self.groupe=groupe
    
    #méthode qui sert à modifier numéro(nom) du groupe
    def modifierNumero(self,numero):
        self.numero=numero
    

#################################################################################################################################################################
#########################################################################      PARTIE Fonctions #################################################################
#################################################################################################################################################################


    
#Fonction qui sert à créer nos groupes à partir de liste de centres 
#elle renvoie une liste de groupes    
def creerGroupes(liste_centres):
    StockDeGroupes=[]
    for i in range(0,len(liste_centres)):
        centre=liste_centres[i]
        groupe=None
        groupe=Groupe(i+1,centre)
        StockDeGroupes+=[groupe]
    return StockDeGroupes

    
#méthode qui sert à donner les centres des groupes  
def listeDeCentres(StockDeGroupes):
    Liste=[]
    for i in StockDeGroupes:
        Liste+=[i.centre[1:]]
    return Liste


#méthode qui sert à donner la liste des points sans leur numérotation( car leur début contient l'ordre(ou numéro) du point)
def listeDePoints(Data):
    Liste=[]
    for i in Data:
        Liste+=[i[1:]]
    return Liste

    
#Fonction qui sert à actualiser le centre d'un groupe    
def actualiserCentre(Groupe):
    Groupe.modifierCentre(calculette.calculCentre(Groupe))

    
#La fonction principale de notre algorithme qui cherche à affecter chaque point au groupe correspondant et actualiser tous les groupes et retourne la variation des centres    
def actualiserGroupes(StockDeGroupes,Data):
    #on calcul les affectations en premier
    ListeDeCentresAncienne=listeDeCentres(StockDeGroupes)
    Affectation=calculette.CalculAffectation(StockDeGroupes,Data)
    
    #on parcourt nos groupes
    for i in StockDeGroupes:
        #on vide notre groupe
        i.modifierGroupe([])
        #on parcourt nos points pour les affecter aux groupe correspondant
        for j in range(0,len(Affectation)):
            if i.numero==Affectation[j]:
                i.ajouterPoint(Data[j])
        # après avoir ajouter tous nos points correspondants , on actualise le centre et c'est bon
        actualiserCentre(i)
    #Cette partie s'intéresse à calculer le max de variation des centres
    ListeDeCentresNouvelle=listeDeCentres(StockDeGroupes)
    Variation=[]
    for i in range (0,len(ListeDeCentresNouvelle)):
        V=calculette.calculNorme(ListeDeCentresNouvelle[i],ListeDeCentresAncienne[i])
        Variation+=[V]
    return max(Variation)


#Cette fonction sert à modifier numéro(aka noms) des groupes
def modiferLesNumeros(Numeros,StockDeGroupes):
        for i in range(len(StockDeGroupes)):
                StockDeGroupes[i].modifierNumero(Numeros[i])



#################################################################################################################################################################
#########################################################################      PARTIE Traitement  ###############################################################
#################################################################################################################################################################


#variable de variation de centres
mu=10000


# Si l'utilisateur charge ses propres données
if queltype==1 or queltype==2:
        #On lit les données
        Data=gestion.read_data(fichier_entree)
        #On prend un échantillon pour les centres
        Centres=random.sample(Data,nombre_de_centres)

        #On crée nos groupes
        StockDeGroupes=creerGroupes(Centres)
        #Variable de variation de centres
        mu=10000
       
        #Boucle qui contrôle la convergence
        while mu>condition_arret:
                #On actualise nos groupes   
                mu=actualiserGroupes(StockDeGroupes,Data)
                print(mu)
        
        print(" le programme est fini")
        #Si l'utilisateur avait choisi de modifier le nom des groupes
        if condition==1:
                modiferLesNumeros(Numeros,StockDeGroupes) 
        #On sauvegarde nos résultats dans un fichier csv
        gestion.write_data(StockDeGroupes,fichier_de_sortie)   
        #on affiche sur l'écran
        for i in StockDeGroupes:
                print("\n")
                print("Groupe: ")
                print(i.numero)
                print("\n")
                print("\n")
                print("\n")
                print("longueur du groupe: ")
                print(len(i.groupe))
                print("\n")
                print("\n")
                print("\n")
                print(i.groupe)
                print("\n")
                print("\n")
                print("\n")
                print("#########################################################################################################")
                print("#########################################################################################################")
                print("#########################################################################################################")


# Si l'utilisateur choisit une simulation
if queltype==3:
        test.simulation(nombre_de_donnes,nombre_de_coordonnees,nombre_de_centres,condition_arret)
