from typing import Set, Tuple, List

class RulesEngine:
    def __init__(self):
        self.rules = [
            {"id": "R1", "conditions": {"fievre", "toux", "fatigue"}, "conclusion": "Grippe", "confiance": 0.85},
            {"id": "R2", "conditions": {"fievre", "toux", "courbatures"}, "conclusion": "Grippe", "confiance": 0.90},
            {"id": "R3", "conditions": {"eternuement", "yeux_rouges"}, "conclusion": "Allergie", "confiance": 0.80},
            {"id": "R4", "conditions": {"fievre", "mal_de_gorge"}, "conclusion": "Infection", "confiance": 0.75},
            {"id": "R5", "conditions": {"toux", "eternuement"}, "conclusion": "Rhume", "confiance": 0.70},
            {"id": "R6", "conditions": {"fatigue"}, "conclusion": "Repos_Necessaire", "confiance": 0.50},
        ]

    def infer(self, facts: Set[str]) -> Tuple[str, float, List[str]]:
        trace = []
        best_match = None
        max_score = 0.0

        if not facts:
            return "Aucune_Pathologie", 1.0, ["Absence de symptômes : hypothèse de santé normale."]

        for rule in self.rules:
            intersection = rule["conditions"].intersection(facts)
            if intersection:
                match_ratio = len(intersection) / len(rule["conditions"])
                trace.append(f"[{rule['id']}] {rule['conclusion']} : {len(intersection)}/{len(rule['conditions'])} conditions validées.")
                
                if match_ratio > max_score or (match_ratio == max_score and best_match and rule["confiance"] > best_match["confiance"]):
                    max_score = match_ratio
                    best_match = rule

        if best_match and max_score >= 0.6:
            final_conf = best_match["confiance"] * max_score
            return best_match["conclusion"], final_conf, trace
        elif best_match and max_score < 0.6:
            return "Diagnostic_Complexe", 0.40, trace + ["Incohérence : symptômes contradictoires ou insuffisants pour valider une règle."]
        else:
            return "Inconnu_Incertitude", 0.20, trace + ["Incomplétude : aucun symptôme ne correspond aux règles de la base."]