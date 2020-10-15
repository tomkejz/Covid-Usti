#!/usr/bin/env python
# coding: utf-8
"""
covid-prehled.py

Program stahuje aktuální opendata CSV z MZČR
a generuje grafy s přehledy pro Ústecký kraj.
Grafy se ukládají jako PNG.

TODO
Ošetřit kontrolu, zda je CSV dostupné a případně poslat zprávu a ukončit program.
Nastavit ukládání grafů do úložiště webu, aby se mohly načítat rovnou do stránek.
Vylepšit vizuál grafů.
Vytvořit další pohledy na data.
"""

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/kraj-okres-nakazeni-vyleceni-umrti.csv')

# Vytvoří nový dataframe obsahující pouze Ústecký kraj
kraj_df = df.loc[df['kraj_nuts_kod'] == 'CZ042']
kraj_df = kraj_df.sort_values('datum', ascending=True)
kraj_df.reset_index(drop=True, inplace=True)

# kraj_df.to_csv('covid_kraj.csv', index=False) # Možnost uložit upravený dataframe

# Graf s přehledem za celý kraj
pocty = kraj_df.groupby(['datum']).sum()
pocty = pocty.reset_index()

plt.figure(figsize=(14,8))
plt.title('Průběh pandemie v Ústeckém kraji', fontdict={'fontweight':'bold', 'fontsize':18})
plt.plot(pocty.datum, pocty.kumulativni_pocet_nakazenych, label='Nakažení', color='red')
plt.plot(pocty.datum, pocty.kumulativni_pocet_vylecenych, label='Vyléčení', color='green')
plt.plot(pocty.datum, pocty.kumulativni_pocet_umrti, label='Úmrtí', color='black')
plt.xticks(pocty.datum[::30], rotation='45')
plt.legend()
plt.ylabel("Počet osob", fontdict={'fontweight':'bold', 'fontsize':12})

plt.savefig('covid-ustecky-kraj.png', dpi=300)
#plt.show()

okresKod = ["CZ0421", "CZ0422", "CZ0423", "CZ0424", "CZ0425", "CZ0426", "CZ0427"]
okresJmeno = ["Děčín", "Chomutov", "Litoměřice", "Louny", "Most", "Teplice", "Ústí"]

# Graf nakažených s detaily jednotlivých okresů
plt.figure(figsize=(14,8))
plt.title('Kumulativní počet nakažených dle okresů', fontdict={'fontweight':'bold', 'fontsize':18})

for i in range (0, 6):
	plt.plot(kraj_df.loc[kraj_df['okres_lau_kod'].str.contains(okresKod[i])].datum, kraj_df.loc[kraj_df['okres_lau_kod'].str.contains(okresKod[i])].kumulativni_pocet_nakazenych, label = okresJmeno[i])

plt.legend()
plt.xticks(kraj_df.datum[::200], rotation='45')
plt.ylabel("Počet osob", fontdict={'fontweight':'bold', 'fontsize':12})
plt.savefig('covid-ustecky-nakazeni.png', dpi=300)


# Graf vyléčených s detaily jednotlivých okresů
plt.figure(figsize=(14,8))
plt.title('Kumulativní počet vyléčených dle okresů', fontdict={'fontweight':'bold', 'fontsize':18})

for i in range (0, 6):
	plt.plot(kraj_df.loc[kraj_df['okres_lau_kod'].str.contains(okresKod[i])].datum, kraj_df.loc[kraj_df['okres_lau_kod'].str.contains(okresKod[i])].kumulativni_pocet_vylecenych, label = okresJmeno[i])

plt.legend()
plt.xticks(kraj_df.datum[::200], rotation='45')
plt.ylabel("Počet osob", fontdict={'fontweight':'bold', 'fontsize':12})
plt.savefig('covid-ustecky-vyleceni.png', dpi=300)


# Graf úmrtí s detaily jednotlivých okresů
plt.figure(figsize=(14,8))
plt.title('Kumulativní počet úmrtí dle okresů', fontdict={'fontweight':'bold', 'fontsize':18})

for i in range (0, 6):
	plt.plot(kraj_df.loc[kraj_df['okres_lau_kod'].str.contains(okresKod[i])].datum, kraj_df.loc[kraj_df['okres_lau_kod'].str.contains(okresKod[i])].kumulativni_pocet_umrti, label = okresJmeno[i])

plt.legend()
plt.xticks(kraj_df.datum[::200], rotation='45')
plt.ylabel("Počet osob", fontdict={'fontweight':'bold', 'fontsize':12})
plt.savefig('covid-ustecky-umrti.png', dpi=300)
