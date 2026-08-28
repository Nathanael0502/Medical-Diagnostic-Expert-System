import numpy as np
from typing import List, Dict, Tuple

class NaiveBayesEngine:
    def __init__(self):
        self.classes = [
            "Grippe", "Allergie", "Infection", "Rhume", 
            "Repos_Necessaire", "Diagnostic_Complexe", 
            "Inconnu_Incertitude", "Aucune_Pathologie"
        ]
        
        self.priors = {c: 1.0 / len(self.classes) for c in self.classes}
        
        self.probs = {
            "fievre": {"Grippe": 0.90, "Infection": 0.80, "Rhume": 0.30, "Allergie": 0.05, "Repos_Necessaire": 0.10, "Diagnostic_Complexe": 0.50, "Inconnu_Incertitude": 0.30, "Aucune_Pathologie": 0.01},
            "toux": {"Grippe": 0.80, "Infection": 0.40, "Rhume": 0.80, "Allergie": 0.20, "Repos_Necessaire": 0.10, "Diagnostic_Complexe": 0.50, "Inconnu_Incertitude": 0.30, "Aucune_Pathologie": 0.01},
            "fatigue": {"Grippe": 0.80, "Infection": 0.60, "Rhume": 0.40, "Allergie": 0.30, "Repos_Necessaire": 0.90, "Diagnostic_Complexe": 0.50, "Inconnu_Incertitude": 0.30, "Aucune_Pathologie": 0.01},
            "eternuement": {"Grippe": 0.20, "Infection": 0.10, "Rhume": 0.70, "Allergie": 0.90, "Repos_Necessaire": 0.05, "Diagnostic_Complexe": 0.50, "Inconnu_Incertitude": 0.30, "Aucune_Pathologie": 0.01},
            "yeux_rouges": {"Grippe": 0.10, "Infection": 0.10, "Rhume": 0.20, "Allergie": 0.85, "Repos_Necessaire": 0.05, "Diagnostic_Complexe": 0.50, "Inconnu_Incertitude": 0.30, "Aucune_Pathologie": 0.01},
            "mal_de_gorge": {"Grippe": 0.50, "Infection": 0.85, "Rhume": 0.50, "Allergie": 0.10, "Repos_Necessaire": 0.05, "Diagnostic_Complexe": 0.50, "Inconnu_Incertitude": 0.30, "Aucune_Pathologie": 0.01},
            "courbatures": {"Grippe": 0.85, "Infection": 0.30, "Rhume": 0.20, "Allergie": 0.05, "Repos_Necessaire": 0.20, "Diagnostic_Complexe": 0.50, "Inconnu_Incertitude": 0.30, "Aucune_Pathologie": 0.01},
            "fievre_elevee": {"Grippe": 0.70, "Infection": 0.60, "Rhume": 0.10, "Allergie": 0.01, "Repos_Necessaire": 0.01, "Diagnostic_Complexe": 0.80, "Inconnu_Incertitude": 0.30, "Aucune_Pathologie": 0.01},
        }
        self.epsilon = 1e-5

    def predict(self, symptoms: List[str]) -> Tuple[str, float, Dict[str, float]]:
        if not symptoms:
            return "Aucune_Pathologie", 0.99, {"Aucune_Pathologie": 0.99}

        posteriors = {}
        for c in self.classes:
            score = np.log(self.priors[c])
            for sym, p_dict in self.probs.items():
                p = np.clip(p_dict.get(c, 0.01), self.epsilon, 1.0 - self.epsilon)
                if sym in symptoms:
                    score += np.log(p)
                else:
                    score += np.log(1.0 - p)
            posteriors[c] = score

        max_log = max(posteriors.values())
        exp_scores = {c: np.exp(val - max_log) for c, val in posteriors.items()}
        sum_exp = sum(exp_scores.values())
        norm_probs = {c: float(exp_scores[c] / sum_exp) for c in self.classes}

        best_class = max(norm_probs, key=norm_probs.get)
        return best_class, norm_probs[best_class], norm_probs