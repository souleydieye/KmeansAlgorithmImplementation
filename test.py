#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
#################################################################################################################################################################
#########################################################################      PARTIE IMPORT  ###################################################################
#################################################################################################################################################################


import os, sys
import math
from numpy import linalg as LA
import numpy as np
import random

import matplotlib.pyplot as plt
import matplotlib.cm as cm

#fichiers nécessaires au traitement
import lecture_ecriture as gestion

#################################################################################################################################################################
#########################################################################      PARTIE Variables ###################################################################
#################################################################################################################################################################


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
                self.D+= math.pow(point1[i]-point2[i],8)
            self.D=math.pow(self.D,1.0/8)
            return self.D

        if self.distance=="Euclidienne":
                for i in range(1,len(point1)):
                        self.D+= math.pow(point1[i]-point2[i],2)
                        self.D=math.pow(self.D,1.0/2)
                return self.D      
              
        if self.distance=="Euclidienne standarisée":
        
            v=[0.7826,-0.4194,0.9490,0.9565]
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


calculette=calcul("Euclidienne")


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

#Fonction qui sert à lancer la simulation
def simulation(nombre_de_donnes,nombre_de_coordonnees,nombre_de_centres,condition_arret):
        #on génère nos données aléatoires
        Data=gestion.generate_random_data(nombre_de_donnes,nombre_de_coordonnees)
        #on prend un échantillon aléatoire de données comme centres
        Centres=random.sample(Data,nombre_de_centres)
        #on crée nos groupes
        StockDeGroupes=creerGroupes(Centres)
        #variable de variation de centres
        mu=10000
       
        #mode graphique pour des données a 2 coordonnées        
        if nombre_de_coordonnees==2:
                #on lance la figure
                fig = plt.figure()
                
                while mu>condition_arret:
                        fig.clear()
                        #on actualise les groupes et on récupère le maximum des variations des centres
                        mu=actualiserGroupes(StockDeGroupes,Data)
                        print(mu)
                        
                        #on choisit des couleurs pour la figure
                        colors = iter(cm.rainbow(np.linspace(0, 1, len(StockDeGroupes))))
                        #mode interactif
                        plt.ion()
                        #on mets les points sur la figure
                        for j in StockDeGroupes:
                            x,y=zip(*listeDePoints(j.groupe))
                            plt.scatter(x,y,color=next(colors))
                        #on met les centres
                        Liste_centres=listeDeCentres(StockDeGroupes)
                        plt.scatter(*zip(*Liste_centres))
                        #on affiche sur l'écran        
                        plt.draw()
                        plt.show()
                        plt.pause(0.01)
    
                print(" le programme est fini")
                #cette ligne sert à laisser la fenêtre ouverte sur l'écran
                plt.show(block=True)
        else:
                mu=actualiserGroupes(StockDeGroupes,Data)
                print(mu)
        #on affiche nos groupes sur l'écran
        for i in StockDeGroupes:
                print("\n")
                print("Groupe ")
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




