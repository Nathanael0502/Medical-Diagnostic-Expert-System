# Système Expert Médical Hybride d'Aide au Diagnostic

**Projet de Raisonnement en Intelligence Artificielle (M1 SDIA - 2026)**

---

## 1. Définition du Problème et État des Connaissances

### 1.1 Contextualisation et Enjeux

Le diagnostic médical préliminaire basé sur les symptômes déclaratifs d'un patient présente plusieurs défis majeurs : la présence d'informations incomplètes, la subjectivité de l'intensité des symptômes et les chevauchements symptomatiques entre diverses pathologies (ex. grippe et infection bactérienne). L'objectif de ce projet est de concevoir un système d'aide à la décision capable d'émettre un pré-diagnostic médical explicite, vérifiable et quantifié en confiance.

### 1.2 Définition de l'Espace du Problème

* **Entrées ($X$)** : Un sous-ensemble de symptômes booléens observés $S \subseteq \{\text{fièvre}, \text{fièvre élevée}, \text{toux}, \text{fatigue}, \text{éternuement}, \text{yeux rouges}, \text{mal de gorge}, \text{courbatures}\}$.
* **Sorties ($Y$)** : Un diagnostic principal $D \in \mathcal{D}$ associé à un indice de confiance $C \in [0, 1]$ et une explication textuelle explicite du raisonnement.
  * $\mathcal{D} = \{\text{Grippe}, \text{Allergie}, \text{Infection}, \text{Rhume}, \text{Repos\_Necessaire}, \text{Diagnostic\_Complexe}, \text{Inconnu\_Incertitude}, \text{Aucune\_Pathologie}\}$.
* **Hypothèses** :
  1. L'absence de symptômes déclarés implique un état sain par défaut.
  2. Les observations fournies par l'utilisateur sont exactes au moment de la saisie.
* **Coût des Erreurs & Faux Négatifs** : Prédire à tort une absence de maladie (`Aucune_Pathologie`) alors qu'une `Infection` grave est présente (Faux Négatif) a un coût médical critique supérieur à l'émission d'un `Diagnostic_Complexe` orientant vers un avis médical humanisé.
* **Critère d'Acceptation** : Le système doit pouvoir converger vers une décision en $< 100\text{ ms}$, fournir la trace d'inférence symbolique complète et gérer la contradiction sans planter.

---

## 2. Formalisation du Domaine et Représentation des Connaissances

### 2.1 Approche Symbolique (Logique des Règles)

La connaissance symbolique est modélisée sous forme de règles de production $R_i : \text{Conditions} \rightarrow \text{Conclusion}$ avec un coefficient de confiance fixe $\alpha_i \in [0, 1]$.

$$
\text{Soit } \mathcal{C}_i \text{ l'ensemble des conditions de la règle } R_i, \quad \text{Score}(R_i) = \frac{|\mathcal{C}_i \cap S|}{|\mathcal{C}_i|}
$$

Une règle $R_i$ est partiellement ou totalement déclenchée dès lors que $|\mathcal{C}_i \cap S| > 0$. La confiance résultante transmise par la règle active est calculée par :

$$
\text{Confiance}(R_i) = \alpha_i \times \text{Score}(R_i)
$$

### 2.2 Approche Probabiliste (Moteur Bayesien Naïf)

Le domaine d'incertitude est représenté à l'aide d'un classifieur Bayesien Naïf. Pour chaque classe $c \in \mathcal{D}$, le système évalue la probabilité a posteriori $P(c \mid S)$ sous l'hypothèse d'indépendance conditionnelle des symptômes sachant la classe :

$$
P(c \mid S) \propto P(c) \prod_{s_j \in S} P(s_j \mid c) \prod_{s_k \notin S} (1 - P(s_k \mid c))
$$

Afin d'éviter le sous-dimensionnement numérique (underflow) lors du produit de probabilités faibles, le calcul s'effectue dans l'espace log-vraisemblance avec lissage $\epsilon = 10^{-5}$ :

$$
\log P(c \mid S) = \log P(c) + \sum_{s_j \in S} \log \tilde{P}(s_j \mid c) + \sum_{s_k \notin S} \log (1 - \tilde{P}(s_k \mid c))
$$

$$
\tilde{P}(s \mid c) = \text{clip}(P(s \mid c), \epsilon, 1 - \epsilon)
$$

Les probabilités sont ensuite normalisées via la fonction Softmax / exp-normalize :

$$
P(c \mid S) = \frac{\exp(\log P(c \mid S) - \max_k \log P(k \mid S))}{\sum_{m} \exp(\log P(m \mid S) - \max_k \log P(k \mid S))}
$$

---

## 3. Architecture globale et Méthodes d'Hybridation

### 3.1 Architecture du Système

Le système repose sur une architecture décisionnelle hybride à deux niveaux (Symbolique + Probabiliste) couplée à un sous-système de résolution de conflits et une interface graphique interactive (Streamlit

Système de diagnostic et de décision hybride combinant un moteur de règles symbolique (chaînage avant) et un réseau bayésien naïf pour traiter l'incertitude et l'incomplétude.


[ Formulaire Symptômes (app.py) ]
│
▼
┌───────────────────────┐
│ HybridExpertSystem    │ (src/hybrid_system.py)
└───────────┬───────────┘
├──────────────────────────┐
▼                          ▼
┌───────────────────────┐  ┌───────────────────────┐
│ RulesEngine           │  │ NaiveBayesEngine      │
│ (src/rules_engine.py) │  │(src/bayesian_engine.py)│
└───────────┬───────────┘  └───────────┬───────────┘
│ (Rule_Class,             │ (NB_Class,
│  Rule_Conf)              │  NB_Conf)
└───────────┬──────────────┘
▼
┌───────────────────────┐
│ Arbitrage & Fusion    │
└───────────┬───────────┘
▼
[ Diagnostic Final + Trace ]

### 3.2 Stratégie d'Arbitrage et d'Hybridation

Le module `HybridExpertSystem` fusionne les conclusions des deux moteurs selon l'algorithme d'arbitrage suivant :

1. **Convergence Parfaite** ($Rule\_Class == NB\_Class$) :
   * $\text{Diagnostic Final} = Rule\_Class$
   * $\text{Confiance Final} = \min\left(1.0, \frac{Rule\_Conf + NB\_Conf}{2} + 0.1\right)$
   * *Explication* : "Convergence totale entre le moteur symbolique et le modèle probabiliste."
2. **Prépondérance Symbolique** ($Rule\_Conf \ge 0.75$) :
   * $\text{Diagnostic Final} = Rule\_Class$
   * $\text{Confiance Final} = Rule\_Conf$
   * *Explication* : "Priorité au moteur symbolique (Règle forte validée)."
3. **Prépondérance Probabiliste** ($NB\_Conf \ge 0.60$) :
   * $\text{Diagnostic Final} = NB\_Class$
   * $\text{Confiance Final} = NB\_Conf$
   * *Explication* : "Priorité au modèle probabiliste (Incertitude symbolique)."
4. **Divergence Majeure / Conflit** (Autres cas) :
   * $\text{Diagnostic Final} = \text{"Diagnostic\_Complexe"}$
   * $\text{Confiance Final} = 0.35$
   * *Explication* : "Divergence majeure entre les moteurs. Orientation vers un avis médical."

---

## 4. Protocole d'Évaluation et Reproductibilité

### 4.1 Jeux de Données d'Évaluation (`data/test_cases.json`)

L'évaluation s'appuie sur un ensemble de 10 cas de test soigneusement définis, incluant des cas nominaux, des cas avec données manquantes/incomplètes et 3 cas limites (*edge cases*) complexes.

| ID Cas                      | Symptômes                                      | Attendu / Type          | Description / Défi                                            |
| :-------------------------- | :---------------------------------------------- | :---------------------- | :------------------------------------------------------------- |
| **TC01**              | `[]`                                          | `Aucune_Pathologie`   | Cas nominal à vide                                            |
| **TC02**              | `["fievre", "toux", "fatigue"]`               | `Grippe`              | Cas nominal standard (Règle R1)                               |
| **TC03**              | `["eternuement", "yeux_rouges"]`              | `Allergie`            | Cas nominal standard (Règle R3)                               |
| **TC04**              | `["fievre", "mal_de_gorge"]`                  | `Infection`           | Cas nominal standard (Règle R4)                               |
| **TC05**              | `["fatigue"]`                                 | `Repos_Necessaire`    | Symptôme isolé / Faible couverture                           |
| **TC06**              | `["toux", "eternuement"]`                     | `Rhume`               | Chevauchement de symptômes                                    |
| **TC07**              | `["fievre_elevee"]`                           | `Diagnostic_Complexe` | Symptôme critique isolé                                      |
| **TC08** *(Limite)* | `["fievre", "toux", "yeux_rouges"]`           | Conflit / Arbitrage     | **Cas Limite 1 :** Contradiction Grippe vs Allergie      |
| **TC09** *(Limite)* | `["fievre_elevee", "courbatures", "fatigue"]` | Bayes vs Règles        | **Cas Limite 2 :** Incomplétude des règles d'infection |
| **TC10** *(Limite)* | `[Tous les 8 symptômes]`                     | `Diagnostic_Complexe` | **Cas Limite 3 :** Surcharge / Incohérence maximale     |

### 4.2 Reproductibilité du Projet

L'application est entièrement reproductible sous Linux / MacOS / Windows.

```bash
# 1. Cloner le projet et créer un environnement virtuel
python3 -m venv venv
source venv/bin/activate

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Lancer la démonstration Streamlit
streamlit run app.py

# 4. Lancer la suite de tests unitaires et d'intégration
python main.py
```
