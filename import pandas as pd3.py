import pandas as pd
import numpy as np
import plotly.express as px

# 1. CREAZIONE DI DATI DI ESEMPIO COMPLESSI (Simulazione N = 2100)
np.random.seed(42)
N_totale = 2100

# Varianze e Medie Simulati (Femmine > Maschi, 1° Anno > Successivi, Salute > Altri)
df_list = []
corsi = ['Scienze Salute', 'Ingegneria', 'Umanistiche']
anni = ['1° Anno', 'Anni Successivi']
sesso = ['F', 'M']

# Generazione iterativa dei dati con medie diverse
for corso in corsi:
    for anno in anni:
        for s in sesso:
            # Determinazione della media di stress simulata
            base_mean = 25 # Punteggio Totale IPSS-R su una scala 0-60 (Esempio)
            if corso == 'Scienze Salute':
                base_mean += 5
            if anno == '1° Anno':
                base_mean += 3
            if s == 'F':
                base_mean += 4
            
            # Generazione del numero di studenti nel sottogruppo
            count = int(N_totale / 12 * (1.5 if corso == 'Scienze Salute' else 1)) # Bilanciamento
            
            # Generazione dei punteggi
            scores = np.random.normal(base_mean, 6.0, count).clip(0, 60) # Punteggi tra 0 e 60
            
            # Simulazione della Percentuale di Stress Elevato (es. > 35)
            percent_high_stress = round((scores > 35).mean() * 100, 1)

            df_temp = pd.DataFrame({
                'Punteggio IPSS-R Totale': scores,
                'Area disciplinare': corso,
                'Anno di Corso': anno,
                'Sesso': s,
                'Percentuale Stress Elevato': percent_high_stress 
            })
            df_list.append(df_temp)

df_completo = pd.concat(df_list)

# 2. CREAZIONE DEL GRAFICO A SCATOLA (BOX PLOT) CON FACETS
fig_box = px.box(
    df_completo,
    
    # Asse X: Anno di Corso
    x='Anno di Corso',
    
    # Asse Y: Punteggio Totale
    y='Punteggio IPSS-R Totale',
    
    # Colore: Sesso
    color='Sesso',
    color_discrete_map={'F': '#FF69B4', 'M': '#1E90FF'},
    
    # Colonne (Facets): Tipo di Corso di Studi
    facet_col='Area disciplinare',
    
    # Dati aggiuntivi mostrati al passaggio del mouse (simula la "percentuale di stress")
    hover_data=['Percentuale Stress Elevato'],
    
    title='Confronto della Distribuzione dello Stress Totale (IPSS-R) per Sottogruppo'
)

# Impostazioni di Layout
fig_box.update_layout(
    xaxis_title='',
    yaxis_title='Punteggio Totale IPSS-R (Scala 0-60)',
    boxmode='group' # Raggruppa le scatole sullo stesso asse X
)
fig_box.update_yaxes(range=[0, 60])

# Visualizzazione
fig_box.show()
# Esporta il grafico in un file HTML autonomo
fig_stacked.write_html("grafico_analisi.html")