
---

## Architecture du Projet et Structure des Fichiers

```bash
.
├── README.md                 # Documentation globale et guide d'utilisation
├── requirements.txt          # Dépendances Python nécessaires au projet
├── main.py                   # Point d'entrée en ligne de commande (CLI)
├── app.py                    # Interface utilisateur web Streamlit (Démo live)
├── src/
│   ├── rules_engine.py       # Moteur symbolique à base de règles déductives
│   ├── bayesian_engine.py    # Moteur probabiliste / réseau bayésien
│   └── hybrid_system.py      # Module d'hybridation et d'arbitrage
└── data/
    └── test_cases.json       # Dataset d'évaluation
```
