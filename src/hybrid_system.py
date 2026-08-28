from typing import List, Dict
from .bayesian_engine import NaiveBayesEngine
from .rules_engine import RulesEngine

class HybridExpertSystem:
    def __init__(self):
        self.nb_engine = NaiveBayesEngine()
        self.rules_engine = RulesEngine()

    def diagnose(self, symptoms: List[str]) -> Dict:
        facts = set(symptoms)
        rule_class, rule_conf, rule_trace = self.rules_engine.infer(facts)
        nb_class, nb_conf, nb_probs = self.nb_engine.predict(symptoms)

        if rule_class == nb_class:
            final_class = rule_class
            final_conf = min(1.0, (rule_conf + nb_conf) / 2 + 0.1)
            explanation = "Convergence totale entre le moteur symbolique et le modèle probabiliste."
        elif rule_conf >= 0.75:
            final_class = rule_class
            final_conf = rule_conf
            explanation = f"Priorité au moteur symbolique (Règle forte validée). Naïve Bayes proposait : {nb_class} ({nb_conf:.2f})."
        elif nb_conf >= 0.60:
            final_class = nb_class
            final_conf = nb_conf
            explanation = f"Priorité au modèle probabiliste (Incertitude symbolique). Les règles proposaient : {rule_class} ({rule_conf:.2f})."
        else:
            final_class = "Diagnostic_Complexe"
            final_conf = 0.35
            explanation = "Divergence majeure entre les moteurs. Orientation vers un avis médical."

        return {
            "diagnostic": final_class,
            "confiance": float(final_conf),
            "explication": explanation,
            "details": {
                "symbolique": {"conclusion": rule_class, "confiance": rule_conf, "trace": rule_trace},
                "probabiliste": {"conclusion": nb_class, "confiance": nb_conf, "distribution": nb_probs}
            }
        }