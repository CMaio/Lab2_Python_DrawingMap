import lightrdf
from bs4 import BeautifulSoup
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


doc = lightrdf.RDFDocument("rows.rdf")
with open("ComarquesProvincies.xls") as fp:
    soup = BeautifulSoup(fp, "html.parser")

alldataToTable=[["Tarragona",0,0,0],["Girona",0,0,0],["Barcelona",0,0,0],["Lleida",0,0,0]]
def addToOne(provin,numPl,ass):
    placeToput=-1
    if provin ==  "Tarragona":
        placeToput=0
    elif provin == "Girona":
        placeToput=1
    elif provin == "Barcelona":
        placeToput=2
    elif provin == "Lleida":
        placeToput=3
    alldataToTable[placeToput][1]+=1
    alldataToTable[placeToput][2]+=numPl
    alldataToTable[placeToput][3]+=ass

paintTable=[]
def addHistory(comar,ofer,assis):
    esta=False
    for n in range(0,len(paintTable)):
        if esta==False:
            if paintTable[n][0] == comar:
                paintTable[n][1]+=ofer 
                paintTable[n][2]+=assis
                paintTable[n][3]=0 
                esta=True 
    
    if esta == False:
        paintTable.append([comar,ofer,assis,0])

class DiferentesPuntos:
    def uno(self):
        found=False
        numCenters=0
        numPlaces=0
        numAverage=0
        data=[]
        with open("ComarquesProvincies.xls") as fp:
            soup = BeautifulSoup(fp, "html.parser")

        i=0
        sup =soup.tbody.find_all("tr")
        for s, p, o in doc.search_triples(None, "https://analisi.transparenciacatalunya.cat/resource/_99md-r3rq/nom_comarca", None):
            result = o.replace('"',"")
            for i in range(0,len(sup)):
                supcomar =  sup[i].find_all("th")
                if supcomar[0].text == result :     
                    supinter = sup[i].find_all("td")
                    placesdoc = doc.search_triples(s, "https://analisi.transparenciacatalunya.cat/resource/_99md-r3rq/places_ofertades_a_la", None)
                    for item1, item2, item3 in placesdoc:
                        numPl = int(item3.replace('"',""))
                    
                    assigndoc = doc.search_triples(s, "https://analisi.transparenciacatalunya.cat/resource/_99md-r3rq/assignacions", None)
                    for item1, item2, item3 in assigndoc:
                        assi = int(item3.replace('"',""))

                    addToOne(supinter[1].text,numPl,assi)
                    break

        for k in alldataToTable:
            print("-Province: "+k[0]+", Number of centers: "+str(k[1])+", Number of places for preinscription: "+str(k[2])+", assignation numbers: "+str(k[3])+", students assigned percentage: "+str(k[3]/k[2]*100)+"%")
        

    def dos(self):
        listGeneral = []
        for s, p, o in doc.search_triples(None, "https://analisi.transparenciacatalunya.cat/resource/_99md-r3rq/nom_comarca", None):
            if fileName in o:
                b = doc.search_triples(s, "https://analisi.transparenciacatalunya.cat/resource/_99md-r3rq/denominaci_completa", None)
                for item1, item2, item3 in b:
                    result1=item3.replace('"',"") 
                
                d = doc.search_triples(s, "https://analisi.transparenciacatalunya.cat/resource/_99md-r3rq/places_ofertades_a_la", None)
                for item1, item2, item3 in d:
                   result2= item3.replace('"',"")

                c = doc.search_triples(s, "https://analisi.transparenciacatalunya.cat/resource/_99md-r3rq/assignacions", None)
                for item1, item2, item3 in c:
                    result3= item3.replace('"',"")

                e = doc.search_triples(s, "https://analisi.transparenciacatalunya.cat/resource/_99md-r3rq/nivell", None)
                for item1, item2, item3 in e:
                    result4= item3.replace('"',"")
                
                v = doc.search_triples(s, "https://analisi.transparenciacatalunya.cat/resource/_99md-r3rq/nom_ensenyament", None)
                for item1, item2, item3 in v:
                    result5= item3.replace('"',"")

                h = doc.search_triples(s, "https://analisi.transparenciacatalunya.cat/resource/_99md-r3rq/oferta_inicial_grups", None)
                for item1, item2, item3 in h:
                   result6= item3.replace('"',"")

                centro=[result1,result2,result3,result4,result5,result6]
                listGeneral.append(centro)

        listGeneral.sort( key=lambda x: (x[0], x[3]))
        for i in listGeneral:
            print("Nom centre: " + i[0] + ", Places: " + i[1] + ", Assignacions: " + i[2] + ", Nivell: " + i[3] + ", Nom ensenyament: " + i[4] + ", Oferta inicial grups: " + i[5]+"\n")
    
    def tres(self):
        geox=0
        geoy=0
        municipiCentres = {}
        municipis=[]

        for s, p, o in doc.search_triples(None, "https://analisi.transparenciacatalunya.cat/resource/_99md-r3rq/nom_comarca", None):
            result = o.replace('"',"")
            if result == fileName:
                j = doc.search_triples(s, "https://analisi.transparenciacatalunya.cat/resource/_99md-r3rq/nom_municipi", None)
                for item1, item2, item3 in j:
                    municipi = item3.replace('"',"")
                if municipi not in municipiCentres:
                    municipiCentres[municipi] = list()
                municipis.append(municipi)
                g = doc.search_triples(s, "https://analisi.transparenciacatalunya.cat/resource/_99md-r3rq/denominaci_completa", None)
                for item1, item2, item3 in g:

                    centre = item3.replace('"',"")
                if centre not in municipiCentres[municipi]:
                    municipiCentres[municipi].append(centre)
        print("Municipis:")
        print(municipis)
        print()

        finalMunicipi = input("Select a Municipi to see all its centers: ")
        print("\nCenters:")
        print(municipiCentres[finalMunicipi])
        print()

        centerselect=input("Select one center: ")
        for s, p, o in doc.search_triples(None, "https://analisi.transparenciacatalunya.cat/resource/_99md-r3rq/denominaci_completa", None):
            result = o.replace('"',"")
            if centerselect == result:
                
                h = doc.search_triples(s, "https://analisi.transparenciacatalunya.cat/resource/_99md-r3rq/coordenades_geo_x", None)
                for item1, item2, item3 in h:
                    geox =float(item3.replace('"',""))

                c = doc.search_triples(s, "https://analisi.transparenciacatalunya.cat/resource/_99md-r3rq/coordenades_geo_y", None)
                for item1, item2, item3 in c:
                    geoy =float(item3.replace('"',""))

        natalidad = "MapaCatProvincies.geojson"
        map_data = gpd.read_file(natalidad)
        
        map_data.head()

        fig, ax = plt.subplots(figsize=(10, 10))
        
        # Control del título y los ejes
        ax.set_title('Ubicacio Centre', 
                    pad = 20, 
                    fontdict={'fontsize':20, 'color': '#4873ab'})
        ax.set_xlabel('Longitud')
        ax.set_ylabel('Latitud')

        # Mostrar el mapa finalizado
        map_data.plot(cmap='Greens', ax=ax,legend=True, zorder=5)
        plt.scatter(geox,geoy, s=100,c='red',zorder=6)
        plt.axis([geox - 0.3, geox+0.3, geoy-0.3, geoy+0.3])

        plt.show()

    def cuatro(self):
        centerselect=input("Which Code would you like to use? ")
        geox=[]
        geoy=[]
        centres=[]
        for s, p, o in doc.search_triples(None, "https://analisi.transparenciacatalunya.cat/resource/_99md-r3rq/codi_municipi_5", None):
            result = o.replace('"',"")
            if centerselect == result:
                j = doc.search_triples(s, "https://analisi.transparenciacatalunya.cat/resource/_99md-r3rq/denominaci_completa", None)
                for item1, item2, item3 in j:
                    result = item3.replace('"',"")
                    if result not in centres:
                        centres.append(item3.replace('"',"")) 

                h = doc.search_triples(s, "https://analisi.transparenciacatalunya.cat/resource/_99md-r3rq/coordenades_geo_x", None)
                for item1, item2, item3 in h:
                    geox.append(float(item3.replace('"',""))) 

                c = doc.search_triples(s, "https://analisi.transparenciacatalunya.cat/resource/_99md-r3rq/coordenades_geo_y", None)
                for item1, item2, item3 in c:
                    geoy.append(float(item3.replace('"',"")))
        
        if not centres:
            print("\nThis code is not a valid one.")
            return
        
        print("\nCenters:")
        print(centres)
        natalidad = "MapaCatProvincies.geojson"
        map_data = gpd.read_file(natalidad)
        
        map_data.head()

        fig, ax = plt.subplots(figsize=(10, 10))
        
        # Control del título y los ejes
        ax.set_title('Ubicacio Centre', 
                    pad = 20, 
                    fontdict={'fontsize':20, 'color': '#4873ab'})
        ax.set_xlabel('Longitud')
        ax.set_ylabel('Latitud')

        # Mostrar el mapa finalizado
        map_data.plot(cmap='Greens', ax=ax,legend=True, zorder=5)
        plt.scatter(geox,geoy, s=10,c='red',zorder=6)
        plt.axis([geox[0] - 0.2, geox[0]+0.2, geoy[0]-0.2, geoy[0]+0.2])

        plt.show()

    def cinco(self):

        percentageComarca = []
        for s, p, o in doc.search_triples(None, "https://analisi.transparenciacatalunya.cat/resource/_99md-r3rq/nom_comarca", None):
            result = o.replace('"',"")
            h = doc.search_triples(s, "https://analisi.transparenciacatalunya.cat/resource/_99md-r3rq/places_ofertades_a_la", None)
            for item1, item2, item3 in h:
                ofer =int(item3.replace('"',""))

            c = doc.search_triples(s, "https://analisi.transparenciacatalunya.cat/resource/_99md-r3rq/assignacions", None)
            for item1, item2, item3 in c:
                assi =int(item3.replace('"',""))
            addHistory(result,ofer,assi)

        for i in range(0,len(paintTable)):
            if paintTable[i][2] == 0:
                percentageComarca.append({"nom_comar": paintTable[i][0], "percentage": 0})
            else:
                percentageComarca.append({"nom_comar": paintTable[i][0], "percentage": paintTable[i][1]/paintTable[i][2]})

        data_df = pd.DataFrame(percentageComarca)

        natalidad = "MapaCatProvincies.geojson"
        map_data = gpd.read_file(natalidad)
        
        dataMapMerge = pd.merge(map_data, data_df, how = 'left', on = 'nom_comar')
        fig, ax = plt.subplots(figsize=(10, 10))

        ax.set_title('percentatge OFERTA/ASSIGNACIONS', 
                    pad = 20, 
                    fontdict={'fontsize':20, 'color': '#4873ab'})
        ax.set_xlabel('Longitud')
        ax.set_ylabel('Latitud')
       
        dataMapMerge.plot(dataMapMerge["percentage"], ax=ax, legend=True, zorder=5)

        plt.show()

    def seis(self):
        found=False
        #x es comarca
        x=[]
        #y es oferta
        y=[]
        
        for s, p, o in doc.search_triples(None, "https://analisi.transparenciacatalunya.cat/resource/_99md-r3rq/nom_comarca", None):
            result = o.replace('"',"")
            h = doc.search_triples(s, "https://analisi.transparenciacatalunya.cat/resource/_99md-r3rq/places_ofertades_a_la", None)
            for item1, item2, item3 in h:
                ofer =int(item3.replace('"',""))
            
            for i in range(0,len(x)):
                if x[i]== result:
                    y[i]+=ofer
                    found = True
            
            if found == False:
                x.append(result)
                y.append(ofer)
            
            found=False      

        plt.bar(x, y)
        plt.xticks(rotation=90)
        plt.title('Ofertas per comarca')
        plt.xlabel('Comarca')
        plt.ylabel('Oferta')

        plt.show()

replay = 'Y'            
d=DiferentesPuntos()          

print("\nMain Menu")
print("---------\n")
print("-Print table with the name of the provinces[1]")
print("-Print a list with all the centers in a COMARCA[2]")
print("-Represent in a map the location of a center selected[3]")
print("-Represent all the centeres within a CODE specified[4]")
print("-Representation of the percentage of OFERTA/ASSIGNACIONS per each COMARCA on a map[5]")
print("-Representation on an histogram of the number of places per COMARCA[6]\n")

while(replay == 'Y'):

    option=int(input("Select one option to execute[1-6]: "))

    while option < 0 or option > 6:
        print("\nThis is not a valid option.")
        option=int(input("Select one option to execute[1-6]: "))

    if option == 1:
        d.uno()
    elif option == 2:
        fileName=input("Which Comarca would you like to use? ")
        d.dos()
    elif option == 3:
        fileName=input("Which Comarca would you like to use? ")
        d.tres()
    elif option == 4:
        d.cuatro()
    elif option == 5:
        d.cinco()
    elif option == 6:
        d.seis()

    replay = input("Would you like to select another option [Y/N]? ")

quit()