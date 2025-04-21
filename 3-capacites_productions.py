# -*- coding: utf-8 -*-
"""
Analyse des capacités de productions d'électricité en métropole  française

Created on Wed May 29 13:54:11 2024

@author: Thierry ALLEM
"""
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

# Chargement du fichier du registre national des installations de production et stockage d'électricité
df_cap_prod = pd.read_csv('registre_national_installation_production_stockage_electricite.csv', sep=';',low_memory=False)
df_cap_prod.head()

# Affichage du nombre de lignes et colonnes du dataframe et décompte des types des valeurs

print("Nombre de lignes du dataframe : ", len(df_cap_prod.index))
print("Nombre de colonnes du dataframe : ", len(df_cap_prod.columns))
print("Valeurs uniques de la colonne 'region' :", df_cap_prod['region'].unique())
print("Types de valeurs :",df_cap_prod.dtypes.value_counts() )
df_cap_prod.info()

#   Renommage des colonnes

#     Dictionnaire avec les nouveaux noms des colonnes

dictionnaire_entetes = {'nomInstallation ':'nom_installation',
                        'codeEICResourceObject':'code_EIC',
                        'codeRegion' : 'code_region',                
                'dateRaccordement' : 'date_raccordement',
                'dateDeraccordement' : 'date_deraccordement',
                'dateMiseEnService' : 'date_mise_en_service',
                'codeFiliere' :'code_filiere',
                'filiere' : 'filiere_production',
                'codeCombustible' : 'code_combustible',
                'codesCombustiblesSecondaires' : 'codes_combustibles_secondaires',
                'combustiblesSecondaires' : 'combustibles_secondaires',
                'codeTechnologie' : 'code_technologie',
                'typeStockage' : 'type_stockage',
                'puisMaxInstallee' : 'puis_max_installee',
                'puisMaxRacCharge' : 'puis_max_rac_charge',
                'puisMaxCharge' : 'puis_max_charge',
                'puisMaxRac' : 'puis_max_rac',
                'puisMaxInstalleeDisCharge' : 'puis_max_installee_discharge',
                'energieStockable' : 'energie_stockable',
                'energieAnnuelleGlissanteInjectee' : 'energie_annuelle_glissante_injectee',
                'energieAnnuelleGlissanteProduite' : 'energie_annuelle_glissante_produite',
                'energieAnnuelleGlissanteSoutiree' : 'energie_annuelle_glissante_soutiree',
                'energieAnnuelleGlissanteStockee' : 'energie_annuelle_glissante_stockee'}
                
df_cap_prod=df_cap_prod.rename(dictionnaire_entetes, axis = 1)
# DESCRIPTION DES COLONNES
#    Création d'un dataframe de description des colonnes de df_cap_prod, sans regroupement par region

df_colonnes = pd.DataFrame()

#   Stockage du noms des colonnes du  dataframe df_cap_prod
df_colonnes['Nom_colonne'] = list(df_cap_prod.columns)

#   Affichage du type des valeurs des colonnes de df
df_colonnes.index = df_cap_prod.columns
types_valeurs = df_cap_prod.dtypes
df_colonnes['Type_valeurs'] = types_valeurs

#   Affichage des valeurs uniques

df_colonnes.insert(loc=len(df_colonnes.columns), column='Valeurs_uniques', value='Valeurs continues')

df_colonnes.loc[(df_colonnes['Nom_colonne'] =='code_region'),'Valeurs_uniques'] = str(df_cap_prod['code_region'].unique())
df_colonnes.loc[(df_colonnes['Nom_colonne'] =='region'),'Valeurs_uniques'] = str(df_cap_prod['region'].unique())
df_colonnes.loc[(df_colonnes['Nom_colonne'] =='code_filiere'),'Valeurs_uniques'] = str(df_cap_prod['code_filiere'].unique())
df_colonnes.loc[(df_colonnes['Nom_colonne'] =='filiere_production'),'Valeurs_uniques'] = str(df_cap_prod['filiere_production'].unique())
df_colonnes.loc[(df_colonnes['Nom_colonne'] =='code_combustible'),'Valeurs_uniques'] = str(df_cap_prod['code_combustible'].unique())
df_colonnes.loc[(df_colonnes['Nom_colonne'] =='combustible'),'Valeurs_uniques'] = str(df_cap_prod['combustible'].unique())
df_colonnes.loc[(df_colonnes['Nom_colonne'] =='combustibles_secondaires'),'Valeurs_uniques'] = str(df_cap_prod['combustibles_secondaires'].unique())
df_colonnes.loc[(df_colonnes['Nom_colonne'] =='code_technologie'),'Valeurs_uniques'] = str(df_cap_prod['code_technologie'].unique())
df_colonnes.loc[(df_colonnes['Nom_colonne'] =='technologie'),'Valeurs_uniques'] = str(df_cap_prod['technologie'].unique())
df_colonnes.loc[(df_colonnes['Nom_colonne'] =='type_stockage'),'Valeurs_uniques'] = str(df_cap_prod['type_stockage'].unique())

pd.set_option('display.max_colwidth', None)
#   Affichage du nombre de valeurs des colonnes de df
df_colonnes['Nb_valeurs'] = df_cap_prod.count()

#   Affichage des NaN

#        Affichage du nombre de NaN de chaque colonne
df_colonnes['nb_NaN'] = df_cap_prod.isna().sum()

#        Quantité totale de 'valeurs' + 'NaN'
df_colonnes['Nb_datas'] = df_colonnes['Nb_valeurs']+df_colonnes['nb_NaN']

#       Affichage du % de données manquantes
df_colonnes['%_Valeurs'] = round(df_colonnes['Nb_valeurs']/df_colonnes['Nb_datas']*100,2)
df_colonnes['%_NaN'] =round(df_cap_prod.isna().sum() /df_colonnes['Nb_datas']*100,2)


#   Export du compte-rendu des colonnes dans un fichier Excel

file_export2 ='2_Rapp_explo_col_registre_prod.xlsx'

df_colonnes.to_excel(file_export2)

print("Rapport préliminaire d'exploration des colonnes du dataframe 'registre_national_installation_production_stockage_electricite' exporté avec succès dans le fichier Excel '2_Rapp_explo_col_registre_prod.xlsx'")



# Suppression des lignes associées à des régions non traitées dans le projet Eco2Mix
regions_to_remove = ['Corse', 'Guadeloupe', 'Martinique', 'Guyane', 'La Réunion']
df_cap_prod = df_cap_prod[df_cap_prod['region'].isin(regions_to_remove) ==False]

# Suppression des lignes avec NaN dans la colonne 'region' (selon les codes INSEE communes, ces NaN semblent correspondre à
# des installations situées dans les DOM-TOM; on les suppose donc hors champs du projet)
df_cap_prod = df_cap_prod.dropna(subset=['region'])

# =========================================================================================================================================
# TRAITEMENT DES DOUBLONS
print("Nombre de doublons dans la colonne 'codeEICResourceObject' (identification de chaque installation):", df_cap_prod['codeEICResourceObject'].duplicated().sum())
print("Nombre de doublons dans la totalité du dataframe :", df_cap_prod.duplicated().sum())
#       Marquage des lignes en double
duplicates_mark = df_cap_prod.duplicated(subset=['codeEICResourceObject'], keep=False)

#       Création d'un nouveau dataframe avec les lignes en double
df_duplicates = df_cap_prod[duplicates_mark]
print(df_duplicates.head())
print("Nombre de doublons du dataframe filtré:",df_duplicates.duplicated().sum())

#       Export du dataframe des doublons dans un fichier Excel

file_export1 ='1_Doublons_installations.xlsx'

df_duplicates.to_excel(file_export1)

print("Doublons des installations du dataframe 'registre_national_installation_production_stockage_electricite' exporté avec succès dans le fichier Excel 1_Doublons_installations.xlsx'")

#       Valeurs uniques de df_duplicates
unique_values_codeEIC = df_duplicates['codeEICResourceObject'].unique()
print("Valeurs uniques des codes EIC du dataframe filtré : ",unique_values_codeEIC)

unique_values_filiere = df_duplicates['filiere'].unique()
print("Valeurs uniques de la colonne 'filiere'du dataframe des doublons : ",unique_values_filiere)

unique_values_nomInstallation = df_duplicates['nomInstallation'].unique()
print("Valeurs uniques de la colonne 'nomInstallation'du dataframe filtré : ",unique_values_nomInstallation)

print("Les doublons de la colonne EIC ne sont que des Nan.")
print("Ces NaN sont associés à des filières de production ['Solaire' 'Autre' 'Eolien' 'Hydraulique'] issues de 'petites' installations de moins de 36kW")
print("On peut donc conclure à l'absence de doublon dans le registre des installations")
# =============================================================================================================================================
# TRAITEMENT DES DONNEES DU REGISTRE df_cap_prod

#   Suppression des colonnes non utiles au projet, notamment celles précisant les localisations; la présence de doublons ayant été exclue
colonnes_to_drop = [2, 3, 4, 5, 6, 7, 8,  11, 12, 13, 17, 18, 19, 20, 35, 36, 37, 39, 40, 42, 43, 44]
df_cap_prod.drop(columns = df_cap_prod.columns[colonnes_to_drop], inplace =True)





#   Copie du dataframe avant pre-processing
df_cap_prod2 = df_cap_prod.copy()
# ===============================================================================================================================
# GESTION DES DATES

#   Remplacement de valeurs des colonnes 'date' inscrit dans un format différent et avec d'autres séparateurs des autres valeurs
liste_dates_replace = {'1893-01-01':'01/01/1893', '1897-03-21':'21/03/1897','1898-01-01':'01/01/1898'}
df_cap_prod2.replace(liste_dates_replace, inplace =True)

#   Conversion des formats de date
colonnes_a_convertir = ['date_raccordement','date_deraccordement','date_mise_en_service']

for colonne in colonnes_a_convertir:
    df_cap_prod2[colonne] = pd.to_datetime(df_cap_prod2[colonne], format="%d/%m/%Y", dayfirst=True).dt.strftime("%Y-%m-%d")
    df_cap_prod2[colonne] = pd.to_datetime(df_cap_prod2[colonne])
df_cap_prod2.dtypes

#   Gestion des valeurs manquantes des colonnes de dates  ****************************
#       Colonne 'date_raccordement': si non-renseignée, on suppose que l'installation très ancienne; on remplace donc les
#        NaN par la date virtuelle '1800-01-01'
missing_values = df_cap_prod2['date_raccordement'].isna()
df_cap_prod2.loc[missing_values, 'date_raccordement'] = '1800-01-01'

#       Colonne 'date_deraccordement': si non-renseignée, l'installation est supposée active; on remplace donc les NaN 
#        par la date virtuelle '2100-01-01'
missing_values = df_cap_prod2['date_deraccordement'].isna()
df_cap_prod2.loc[missing_values, 'date_deraccordement'] = '2100-01-01'

#       Colonne 'date_mise_en_service'  : si absence, on la suppose identique à la date de date_raccordement
df_cap_prod2.loc[df_cap_prod2['date_mise_en_service'].isna(), 'date_mise_en_service'] = df_cap_prod2['date_raccordement']
# ==============================================================================================================
#  GESTION DES COLONNES RENSEIGNANT LES COMBUSTIBLES

#          Suppression des colonnes codes, incomplètes et non essentielles au projet
colonnes_to_drop = [9,11,13]
df_cap_prod2.drop(columns = df_cap_prod2.columns[colonnes_to_drop], inplace =True)

#          Gestion des valeurs manquantes des colonnes renseignant les combustibles 
#            Remplacement des NaN des colonnes 'code_EIC','combustible', 'combustibles_secondaires','technologie' et 'type_stockage'
columns_to_replace = ['code_EIC', 'combustible', 'combustibles_secondaires', 'technologie', 'type_stockage']
df_cap_prod2[columns_to_replace] = df_cap_prod2[columns_to_replace].fillna('NR')

#           Remplacement des NaN des colonnes numériques par 0
columns_to_replace2 = ['puis_max_installee','puis_max_rac_charge','puis_max_charge','puis_max_rac','puis_max_installee_discharge',
'energie_stockable','productible','energie_annuelle_glissante_injectee','energie_annuelle_glissante_produite',
'energie_annuelle_glissante_soutiree','energie_annuelle_glissante_stockee']
df_cap_prod2[columns_to_replace2] = df_cap_prod2[columns_to_replace2].fillna(0)

df_cap_prod2.info()
df_cap_prod2.isna().sum()
# ===================================================================================================================
# GESTION DES REGIONS
    # Conversion de la colonne 'code_region' en int
df_cap_prod2['code_region'] = df_cap_prod2['code_region'].astype(int)

    # Renommage des noms des régions de la colonne 'region' tels qu'ils le sont dans dataframe Eco2MixRégions traité
dictionnaire_region= {"Provence-Alpes-Côte d'Azur":"PROVENCE ALPES COTE D AZUR",
                      "Bourgogne-Franche-Comté":"BOURGOGNE FRANCHE COMTE",
                      "Bretagne":"BRETAGNE",
                      "Normandie":"NORMANDIE",
                      "Nouvelle-Aquitaine":"NOUVELLE AQUITAINE",
                      "Hauts-de-France":"HAUTS DE FRANCE",
                      "Île-de-France":"ILE DE FRANCE",
                      "Auvergne-Rhône-Alpes":"AUVERGNE RHONE ALPES",
                      "Grand Est":"GRAND EST",
                      "Centre-Val de Loire":"CENTRE VAL DE LOIRE",
                      "Occitanie":"OCCITANIE",
                      "Pays de la Loire":"PAYS DE LA LOIRE"}
df_cap_prod2['region']=df_cap_prod2['region'].replace(dictionnaire_region)

    #  Ajout d'une colonne portant les noms de régions abrégés selon la norme ISO 3166-2
        # Insertion d'une nouvelle colonne 'region_abr' à l'index 3
df_cap_prod2.insert(3, 'region_abr', df_cap_prod2['region'])

        # Affectation des valeurs de 'region_ncc' à 'region_abr'
df_cap_prod2['region_abr'] = df_cap_prod2['region']

        # Renommage des valeurs de 'region_abr'
dictionnaire_region_abr= {"PROVENCE ALPES COTE D AZUR" : "FR-PAC",
                      "BOURGOGNE FRANCHE COMTE" : "FR-BFC",
                      "BRETAGNE" : "FR-BRE",
                      "NORMANDIE" : "FR-NOR",
                      "NOUVELLE AQUITAINE" : "FR-NAQ",
                      "HAUTS DE FRANCE" : "FR-HDF",
                      "ILE DE FRANCE" : "FR-IDF",
                      "AUVERGNE RHONE ALPES":"FR-ARA",
                      "GRAND EST":"FR-GES",
                      "CENTRE VAL DE LOIRE":"FR-CVL",
                      "OCCITANIE":"FR-OCC",
                      "PAYS DE LA LOIRE":"FR-PDL"}
df_cap_prod2['region_abr']=df_cap_prod2['region_abr'].replace(dictionnaire_region_abr)
print("Noms abrégés des régions : ", df_cap_prod2['region_abr'].unique())
# ===============================================================================================================
# GESTION DES NOM DES FILIERES DE PRODUCTION 
print("Valeurs uniques de la colonne 'filiere_production':", df_cap_prod2['filiere_production'].unique())

print("Nombre de valeurs manquantes de la colonne 'filiere_production' :",df_cap_prod2['filiere_production'].isna().sum())
df_cap_prod2.dropna(subset=['filiere_production'], inplace=True)
print("Nombre de valeurs manquantes de la colonne 'filiere_production' :",df_cap_prod2['filiere_production'].isna().sum())
     

 # Renommage des valeurs de 'filiere_production' pour équivalence avec les données de 'eco2mix-regional-cons-def'
dictionnaire_region_abr= {'Solaire' :'solaire',
                          'Hydraulique': 'hydraulique',
                          'Eolien' : 'eolien',
                          'Thermique non renouvelable':'thermique',
                          'Stockage non hydraulique' : 'stockage_batterie',
                          'Bioénergies' : 'bioenergies',
                          'Nucléaire' : 'nucleaire',
                          'Energies Marines' : 'hydraulique',
                          'Géothermie':'geothermie'}
df_cap_prod2['filiere_production']=df_cap_prod2['filiere_production'].replace(dictionnaire_region_abr)
print(df_cap_prod2['filiere_production'].unique())

apercu = df_cap_prod2.head(20)


# Export du dataFrame nettoyé dans un fichier au format CSV
df_cap_prod2.to_csv('registre_prod_cleaned.csv', sep=';', encoding='latin-1')

# Export du dataFrame nettoyé dans un fichier Excel

file_export3 ='registre_prod_cleaned.xlsx'

df_cap_prod2.to_excel(file_export3)

print("Registre_national_installation_production_stockage_electricite' nettoyé exporté avec succès dans le fichier Excel 'registre_prod_cleaned.xlsx'")


# =========================================================== CALCUL DES CAPACITES INSTALLEES PAR DATE AVEC PAS DE 00H30, REGION ET FILIERE 
# ================================ de '2013-01-01 00:00:00' à '2022-05-31 23:30:00'

# Création d'un dataframe vide pour le stockage des capacités totales de production
df_result_cap_prod = pd.DataFrame()

import time
# Création d'un générateur pour les dates
def date_range(start, end):
    current = start
    while current < end:
        yield current
        current += pd.Timedelta(minutes=30)

dates = date_range(pd.Timestamp('2013-01-01 00:00:00'), pd.Timestamp('2022-05-31 23:30:00'))


# Initialisation des variables
dates = list(dates)  # Conversion du générateur en liste
total_iterations = len(dates)  # Nombre total d'itérations
i=0
cumul_temps = 0
start_time = time.time()

for date in dates:
    start_time = time.time()
    
    df_cap_prod2['date'] = date
    df_filtered = df_cap_prod2[(df_cap_prod2['date_mise_en_service'] <= df_cap_prod2['date']) & (df_cap_prod2['date'] < df_cap_prod2['date_deraccordement'])]
    df_temp = df_filtered.groupby(['region', 'filiere_production', 'date'])['puis_max_installee'].sum().reset_index()
    df_result_cap_prod = pd.concat([df_result_cap_prod, df_temp])
    print(i)
     
    end_time = time.time()  # Enregistrement de l'heure de fin
    temps_execution = end_time - start_time  # Calcul du temps d'exécution
    cumul_temps += temps_execution
    i+=1
    print(f"Temps d'exécution de l'itération {i}={temps_execution} secondes.")
    print(f"Temps d'exécution cumulé ={cumul_temps} secondes.")
    
    # Estimation du temps restant
    duree_moy_iteration = cumul_temps / i
    iterations_restantes = total_iterations - i
    temps_restant_estime = duree_moy_iteration * iterations_restantes/60

    print(f"Iteration {i} terminée en {temps_execution} secondes. Temps restant estimé : {temps_restant_estime} minutes.")
# Suppression de df_filtered
del df_filtered

# Conversion des valeurs de puissance de kW en MW

df_result_cap_prod['puis_max_installee']=df_result_cap_prod['puis_max_installee'].div(1000)

# Export du dataFrame nettoyé dans un fichier au format CSV
df_result_cap_prod.to_csv('df_result_cap_prod.csv', sep=';', encoding='latin-1')
print("CONVERSIONS DES KW EN MW EFFECTUEES")
resultats = df_result_cap_prod.head(200)
df_result_cap_prod.info()

# =========================================================== CALCUL DES CAPACITES INSTALLEES PAR DATE AVEC PAS DE 00H30, REGION ET FILIERE 
# ================================ de '2013-01-01 00:00:00' à '2022-05-31 23:30:00'

# Création d'un dataframe vide pour le stockage des capacités totales de production
df_result_cap_prod2 = pd.DataFrame()

import time
# Création d'un générateur pour les dates
def date_range(start, end):
    current = start
    while current < end:
        yield current
        current += pd.Timedelta(minutes=30)

dates2 = date_range(pd.Timestamp('2022-06-01 00:00:00'), pd.Timestamp('2022-12-31 23:30:00'))


# Initialisation des variables
dates2 = list(dates2)  # Conversion du générateur en liste
total_iterations = len(dates2)  # Nombre total d'itérations
i=0
cumul_temps = 0
start_time = time.time()

for date in dates2:
    start_time = time.time()
    
    df_cap_prod2['date'] = date
    df_filtered2 = df_cap_prod2[(df_cap_prod2['date_mise_en_service'] <= df_cap_prod2['date']) & (df_cap_prod2['date'] < df_cap_prod2['date_deraccordement'])]
    df_temp2 = df_filtered2.groupby(['region', 'filiere_production', 'date'])['puis_max_installee'].sum().reset_index()
    df_result_cap_prod2 = pd.concat([df_result_cap_prod2, df_temp2])
    print(i)
     
    end_time = time.time()  # Enregistrement de l'heure de fin
    temps_execution = end_time - start_time  # Calcul du temps d'exécution
    cumul_temps += temps_execution
    i+=1
    print(f"Temps d'exécution de l'itération {i}={temps_execution} secondes.")
    print(f"Temps d'exécution cumulé ={cumul_temps} secondes.")
    
    # Estimation du temps restant
    duree_moy_iteration = cumul_temps / i
    iterations_restantes = total_iterations - i
    temps_restant_estime = duree_moy_iteration * iterations_restantes/60

    print(f"Iteration {i} terminée en {temps_execution} secondes. Temps restant estimé : {temps_restant_estime} minutes.")
# Suppression de df_filtered
del df_filtered2

# Conversion des valeurs de puissance de kW en MW

df_result_cap_prod2['puis_max_installee']=df_result_cap_prod2['puis_max_installee'].div(1000)

# Export du dataFrame nettoyé dans un fichier au format CSV
df_result_cap_prod2.to_csv('df_result_cap_prod_2022.csv', sep=';', encoding='latin-1')
print("CONVERSIONS DES KW EN MW EFFECTUEES")
df_result_cap_prod2.info()

# Concaténation des 2 périodes traitées:
# Chargement du fichier du registre national des installations de production et stockage d'électricité
df_result_cap_prod = pd.read_csv('df_result_cap_prod.csv', sep=';',low_memory=False)
# Concaténation
# Concaténation des deux dataframes
df_result_cap_prod_2013_2022 = pd.concat([df_result_cap_prod, df_result_cap_prod2], ignore_index=True)
df_result_cap_prod_2013_2022.info()

# =================================== SUPPRESSION de la colonne 'Unnamed: 0' de 'ind_prod_comp' ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
colonnes_to_drop = [0]
df_result_cap_prod_2013_2022.drop(columns = df_result_cap_prod_2013_2022.columns[colonnes_to_drop], inplace =True)
df_result_cap_prod_2013_2022.info()
# Export du dataFrame complet de 2013 à 2022 dans un fichier au format CSV
df_result_cap_prod_2013_2022.to_csv('df_result_cap_prod_2013_2022.csv', sep=';', encoding='latin-1')
