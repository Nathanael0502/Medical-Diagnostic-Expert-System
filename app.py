import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src.hybrid_system import HybridExpertSystem

st.set_page_config(page_title="Système Expert Médical Hybride", layout="wide")

st.title("Système Expert d'Aide au Diagnostic Médical")
st.caption("Hybridation Symbolique  et Probabiliste ")

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

st.sidebar.header("Symptômes observés")
selected_symptoms = []
for label, key in symptoms_map.items():
    if st.sidebar.checkbox(label, key=key):
        selected_symptoms.append(key)

if st.button("Lancer le diagnostic", type="primary"):
    result = system.diagnose(selected_symptoms)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Diagnostic Retenu", result["diagnostic"])
    with col2:
        st.metric("Niveau de Confiance Global", f"{result['confiance'] * 100:.1f} %")
        
    st.info(f"**Explication du raisonnement :** {result['explication']}")
    
  
    tab1, tab2, tab3 = st.tabs([
        "Analyse Probabiliste ", 
        "Analyse Symbolique ", 
        "Comparaison des Moteurs"
    ])
    
 
    probs_dict = result['details']['probabiliste']['distribution']
    df_probs = pd.DataFrame([
        {"Diagnostic": k.replace("_", " "), "Probabilité": v * 100} 
        for k, v in probs_dict.items()
    ]).sort_values(by="Probabilité", ascending=True)

    with tab1:
        st.subheader("Distribution a posteriori des probabilités")
        
        col_g1, col_g2 = st.columns(2)
        
        with col_g1:
            
            fig_bar = px.bar(
                df_probs, 
                x="Probabilité", 
                y="Diagnostic", 
                orientation='h',
                text_auto='.1f',
                title="Probabilités par Pathologie (%)",
                color="Probabilité",
                color_continuous_scale="Blues"
            )
            fig_bar.update_layout(
                xaxis_title="Probabilité (%)", 
                yaxis_title="", 
                height=400,
                showlegend=False
            )
            fig_bar.update_traces(texttemplate='%{x:.1f}%', textposition='outside')
            st.plotly_chart(fig_bar, use_container_width=True)

        with col_g2:
          
            df_pie = df_probs[df_probs["Probabilité"] > 1.0] 
            fig_pie = px.pie(
                df_pie, 
                values="Probabilité", 
                names="Diagnostic", 
                title="Répartition des hypothèses probables (>1%)",
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig_pie.update_traces(textinfo='percent+label')
            fig_pie.update_layout(height=400)
            st.plotly_chart(fig_pie, use_container_width=True)

    with tab2:
        st.subheader("Inférence du Moteur de Règles Symboliques")
        st.write(f"**Conclusion du moteur :** {result['details']['symbolique']['conclusion']}")
        st.write(f"**Confiance attribuée :** {result['details']['symbolique']['confiance'] * 100:.1f} %")
        st.write("**Trace d'exécution des règles :**")
        for trace in result['details']['symbolique']['trace']:
            st.code(trace, language="text")

    with tab3:
        st.subheader("Analyse Comparative Symbolique vs Probabiliste")
        
        symb_class = result['details']['symbolique']['conclusion']
        symb_conf = result['details']['symbolique']['confiance'] * 100
        prob_class = result['details']['probabiliste']['conclusion']
        prob_conf = result['details']['probabiliste']['confiance'] * 100

        df_comp = pd.DataFrame({
            "Moteur": ["Symbolique ", "Probabiliste "],
            "Diagnostic": [symb_class, prob_class],
            "Confiance (%)": [symb_conf, prob_conf]
        })
        
        fig_comp = px.bar(
            df_comp,
            x="Moteur",
            y="Confiance (%)",
            color="Diagnostic",
            text="Confiance (%)",
            title="Niveau de confiance par Approche",
            barmode="group",
            height=350
        )
        fig_comp.update_traces(texttemplate='%{y:.1f}%', textposition='outside')
        fig_comp.update_layout(yaxis_range=[0, 110])
        st.plotly_chart(fig_comp, use_container_width=True)