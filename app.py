import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src.hybrid_system import HybridExpertSystem

st.set_page_config(page_title="Système Expert Médical Hybride", layout="wide")

st.title("Système Expert d'Aide au Diagnostic Médical")
st.caption("Hybridation Symbolique et Probabiliste — Démonstration par Rôle")

system = HybridExpertSystem()

symptoms_map = {
    "Fièvre": "fievre",
    "Fièvre Élevée": "fievre_elevee",
    "Toux": "toux",
    "Fatigue": "fatigue",
    "Éternuement": "eternuement",
    "Yeux Rouges": "yeux_rouges",
    "Mal de Gorge": "mal_de_gorge",
    "Courbatures": "courbatures"
}

# Menu Démo 
st.sidebar.title(" Menu Démo / Rôles")
role_selected = st.sidebar.radio(
    "Sélectionnez votre rôle pour la démo :",
    [
        "1. Formalisation et Ontologie — RATOVONJANAHARY Rojo Ny Ony Fitahiana (N°107I23)",
        "2. Moteur Symbolique — FANOMEZANIRINA Miaro Ny Anjara (N°197I23)",
        "3. Moteur Probabiliste — RANDRIANJAFY Nathanaël (N°079I23)",
        "4. Intégrateur — RATSIMBA Vahatriniaina (N°104I23)",
        "5. Tests et Qualité — ANDRIAMAHERIMANANA Johnson Rolly (N°011I23)"
    ]
)

st.sidebar.markdown("---")
st.sidebar.header("Symptômes observés")
selected_symptoms = []
for label, key in symptoms_map.items():
    if st.sidebar.checkbox(label, key=key):
        selected_symptoms.append(key)



# RÔLE 1 : FORMALISATION ET CONNAISSANCES

if role_selected.startswith("1."):
    st.header(" Rôle 1 : Formalisation et Base de Connaissances")
    st.subheader("Responsable : RATOVONJANAHARY Rojo Ny Ony Fitahiana — N°107I23")
    st.markdown("""
    * **Contributions :** Cadrage du problème, formalisation mathématique, rédaction des Sections 1 et 2 du rapport.
    * **Description :** *Ce menu présente la modélisation des connaissances et la cartographie des symptômes d'entrée.*
    """)
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Base de Symptômes Formalisés")
        df_symptomes = pd.DataFrame(list(symptoms_map.items()), columns=["Nom d'affichage", "Clé Interne"])
        st.dataframe(df_symptomes, use_container_width=True)
        
    with col2:
        st.subheader("Symptômes Actuellement Sélectionnés")
        if selected_symptoms:
            st.success(f"Clés envoyées aux moteurs : `{selected_symptoms}`")
        else:
            st.warning("Veuillez cocher des symptômes dans la barre latérale.")



# RÔLE 2 : MOTEUR SYMBOLIQUE

elif role_selected.startswith("2."):
    st.header(" Rôle 2 : Moteur de Règles Symboliques")
    st.subheader("Responsable : FANOMEZANIRINA Miaro Ny Anjara — N°197I23")
    st.markdown("""
    * **Contributions :** Conception du moteur d'inférence, écriture des règles R1-R6, création de `src/rules_engine.py`.
    """)
    
    if st.button("Exécuter le Moteur Symbolique", type="primary"):
        result = system.diagnose(selected_symptoms)
        symb_data = result['details']['symbolique']
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Conclusion Symbolique", symb_data['conclusion'])
        with col2:
            st.metric("Confiance", f"{symb_data['confiance'] * 100:.1f} %")
            
        st.subheader("Trace d'exécution des Règles Déclenchées")
        for trace in symb_data['trace']:
            st.code(trace, language="text")



# RÔLE 3 : MOTEUR PROBABILISTE

elif role_selected.startswith("3."):
    st.header(" Rôle 3 : Moteur Probabiliste / Réseau Bayésien")
    st.subheader("Responsable : RANDRIANJAFY Nathanaël — N°079I23")
    st.markdown("""
    * **Contributions :** Modélisation du réseau bayésien naïf, gestion du sous-dimensionnement logvraisemblance, `src/bayesian_engine.py`.
    """)
    
    if st.button("Calculer la Distribution a posteriori", type="primary"):
        result = system.diagnose(selected_symptoms)
        probs_dict = result['details']['probabiliste']['distribution']
        
        df_probs = pd.DataFrame([
            {"Diagnostic": k.replace("_", " "), "Probabilité": v * 100} 
            for k, v in probs_dict.items()
        ]).sort_values(by="Probabilité", ascending=True)

        col_g1, col_g2 = st.columns(2)
        with col_g1:
            fig_bar = px.bar(
                df_probs, x="Probabilité", y="Diagnostic", orientation='h',
                text_auto='.1f', title="Probabilités par Pathologie (%)",
                color="Probabilité", color_continuous_scale="Blues"
            )
            fig_bar.update_traces(texttemplate='%{x:.1f}%', textposition='outside')
            st.plotly_chart(fig_bar, use_container_width=True)

        with col_g2:
            df_pie = df_probs[df_probs["Probabilité"] > 1.0] 
            fig_pie = px.pie(
                df_pie, values="Probabilité", names="Diagnostic", 
                title="Hypothèses probables (>1%)", hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig_pie.update_traces(textinfo='percent+label')
            st.plotly_chart(fig_pie, use_container_width=True)



# RÔLE 4 : INTÉGRATION ET INTERFACE

elif role_selected.startswith("4."):
    st.header(" Rôle 4 : Système Hybride et Explication Globale")
    st.subheader("Responsable : RATSIMBA Vahatriniaina — N°104I23")
    st.markdown("""
    * **Contributions :** Développement de `src/hybrid_system.py`, création du dashboard interactif Streamlit `app.py`.
    """)
    
    if st.button("Lancer le Diagnostic Hybride Complet", type="primary"):
        result = system.diagnose(selected_symptoms)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Diagnostic Retenu Final", result["diagnostic"])
        with col2:
            st.metric("Niveau de Confiance Global", f"{result['confiance'] * 100:.1f} %")
            
        st.info(f"**Explication de la fusion :** {result['explication']}")
        
        st.subheader("Comparaison Symbolique vs Probabiliste")
        symb_class = result['details']['symbolique']['conclusion']
        symb_conf = result['details']['symbolique']['confiance'] * 100
        prob_class = result['details']['probabiliste']['conclusion']
        prob_conf = result['details']['probabiliste']['confiance'] * 100

        df_comp = pd.DataFrame({
            "Moteur": ["Symbolique", "Probabiliste"],
            "Diagnostic": [symb_class, prob_class],
            "Confiance (%)": [symb_conf, prob_conf]
        })
        
        fig_comp = px.bar(
            df_comp, x="Moteur", y="Confiance (%)", color="Diagnostic",
            text="Confiance (%)", title="Confrontation des Moteurs", barmode="group"
        )
        fig_comp.update_traces(texttemplate='%{y:.1f}%', textposition='outside')
        fig_comp.update_layout(yaxis_range=[0, 110])
        st.plotly_chart(fig_comp, use_container_width=True)



# RÔLE 5 : TESTS ET QUALITÉ

elif role_selected.startswith("5."):
    st.header(" Rôle 5 : Évaluation, Validation et Cas Limites")
    st.subheader("Responsable : ANDRIAMAHERIMANANA Johnson Rolly — N°011I23")
    st.markdown("""
    * **Contributions :** Élaboration de `data/test_cases.json`, protocole d'évaluation, analyse des erreurs, `main.py`.
    """)
    
    st.subheader("Jeux de tests pré-enregistrés")
    test_scenario = st.selectbox(
        "Choisissez un scénario de test à exécuter :",
        ["Cas Nominal : Grippe Franche", "Cas Limite : Symptômes Contradictoires", "Cas Incomplet : Un seul symptôme"]
    )
    
    if st.button("Exécuter le scénario sélectionné"):
        if "Grippe" in test_scenario:
            symptom_list = ["fievre_elevee", "toux", "courbatures", "fatigue"]
        elif "Contradictoires" in test_scenario:
            symptom_list = ["yeux_rouges", "courbatures", "eternuement"]
        else:
            symptom_list = ["fievre"]
            
        res = system.diagnose(symptom_list)
        st.write(f"**Symptômes de test passés :** `{symptom_list}`")
        st.success(f"**Résultat obtenu :** {res['diagnostic']} ({res['confiance']*100:.1f}%)")
        st.json(res['details'])