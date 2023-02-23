import pandas as pd
import datetime
import re

# Charger les données à partir du fichier CSV
df = pd.read_csv('JobSite.csv')

# Supprimer les colonnes inutiles
df = df.drop(columns=['URL'])


# Nettoyer la colonne 'Job Title' en supprimant les informations de salaire et les balises HTML
df['Job Title'] = df['Job Title'].apply(lambda x: re.sub('\$[\d,]+', '', x)) # Supprimer les informations de salaire
df['Job Title'] = df['Job Title'].apply(lambda x: re.sub('<.*?>', '', x)) # Supprimer les balises HTML

# Nettoyer la colonne 'Company name' en supprimant les espaces en double
df['Company name'] = df['Company name'].apply(lambda x: x.strip() if isinstance(x, str) else x)
df['Company name'] = df['Company name'].apply(lambda x: re.sub('\s+', ' ', str(x).strip()))

# Nettoyer la colonne 'Type' en supprimant les informations de contrat et les espaces en double
df['Type'] = df['Type'].apply(lambda x: re.sub('Contract', '', str(x).strip())) # Supprimer les informations de contrat
df['Type'] = df['Type'].apply(lambda x: re.sub('\s+', ' ', str(x).strip())) # Supprimer les espaces en double

# Nettoyer la colonne 'Location' en supprimant les informations de région et les espaces en double
df['Location'] = df['Location'].apply(lambda x: re.sub('.*Region', '', str(x).strip())) # Supprimer les informations de région
df['Location'] = df['Location'].apply(lambda x: re.sub('\s+', ' ', str(x).strip())) # Supprimer les espaces en double

# Nettoyer la colonne 'Job Description' en supprimant les balises HTML
df['Job Description'] = df['Job Description'].apply(lambda x: re.sub('<.*?>', '', str(x)))

# Enregistrer les données nettoyées dans un nouveau fichier CSV
for column in df.columns:
    if df[column].dtype == float:
        df[column] = df[column].apply(lambda x: str(x).strip() if isinstance(x, str) else x)

    if df[column].dtype == object:
        df[column] = df[column].apply(lambda x: str(x).strip() if isinstance(x, str) else x)

date = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
df.to_csv(f'Cleaned_JobSite_{date}.csv', index=False)
print('Cleaned data saved in CSV!')
