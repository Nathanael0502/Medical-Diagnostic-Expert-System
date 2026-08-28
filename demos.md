
### Membre 1 : Formalisation et Problématique

* **Temps de parole :** 1 minute 15 secondes (00:00 $\rightarrow$ 01:15)
* **Diapositive support :** *Slide 1 - Définition du Problème & Enjeux Médicaux*
* **Script de parole :**
  > *"Bonjour à tous. Notre projet porte sur la réalisation d'un système expert hybride d'aide au pré-diagnostic médical. Le défi majeur réside dans le fait que les symptômes déclarés par un patient sont souvent incomplets, parfois contradictoires, et partagés entre plusieurs maladies.
  > Nous avons formalisé ce problème avec un espace de 8 symptômes en entrée et 8 classes de sortie. Notre contrainte fondamentale est d'éviter à tout prix les faux négatifs critiques : le système ne doit pas déclarer un patient sain si des signes d'infection existent, et doit savoir admettre son incertitude via un statut 'Diagnostic Complexe'.
  > Pour résoudre ce problème de manière explicite et vérifiable, nous avons combiné deux approches complémentaires : une approche symbolique par règles et une approche probabiliste Bayesienne."*
  >

---

### Membre 2 : Moteur Symbolique (Logique & Règles)

* **Temps de parole :** 1 minute 15 secondes (01:15 $\rightarrow$ 02:30)
* **Diapositive support :** *Slide 2 - Moteur Symbolique à base de Règles (`rules_engine.py`)*
* **Script de parole :**
  > *"Je me suis occupé de la conception du moteur symbolique dans le fichier `rules_engine.py`. Nous avons modélisé la connaissance médicale sous forme de règles formelles avec un indice de confiance attribué à chaque pattern.
  > Par exemple, la règle R1 associe fièvre, toux et fatigue à la Grippe avec une confiance de 85%. L'intérêt majeur du moteur symbolique réside dans la traçabilité complète de son inférence : le système est capable d'expliquer exactement quelle règle s'est déclenchée, avec quel ratio de couverture des conditions.
  > Cependant, la logique pure a ses limites : face à des symptômes isolés ou non répertoriés dans la base, le moteur symbolique seul échoue et renvoie une forme d'incertitude. C'est pour cela que nous l'avons couplé à un moteur probabiliste."*
  >

---

### Membre 3 : Moteur Probabiliste (Réseau Bayesien) (natha)

* **Temps de parole :** 1 minute 15 secondes (02:30 $\rightarrow$ 03:45)
* **Diapositive support :** *Slide 3 - Inférence Probabiliste Bayesienne (`bayesian_engine.py`)*
* **Script de parole :**
  > *"Pour gérer l'incertitude et les informations incomplètes, j'ai développé le moteur probabiliste Bayesien dans `bayesian_engine.py`. Ce moteur évalue la probabilité a posteriori de chaque maladie connaissant les symptômes observés et non-observés.
  > Sur le plan technique, pour éviter les erreurs de sous-dimensionnement numérique lors du produit de probabilités très faibles, tous les calculs sont effectués en log-vraisemblance avant d'être ré-expédiés et normalisés par une fonction Softmax.
  > Ce modèle apporte une grande robustesse face au bruit et aux données manquantes. Il nous fournit une distribution complète de probabilités sur l'ensemble des 8 pathologies, ce qui permet de doser le niveau de doute du système."*
  >

---

### Membre 4 : Intégration, Hybridation et DÉMO LIVE

* **Temps de parole :** 2 minutes 30 secondes (03:45 $\rightarrow$ 06:15)
* **Diapositive support :** *Slide 4 - Architecture Hybride & Démonstration de l'Application Streamlit (`app.py`)*
* **Script de parole (avec manipulation de l'écran Streamlit) :**
  > *"J'ai conçu l'architecture hybride dans `hybrid_system.py` et l'interface utilisateur Streamlit dans `app.py`. Le moteur hybride agit comme un arbitre intelligent : si les deux moteurs concordent, la confiance est renforcée. Si une règle forte s'impose, le symbolique prime. Si le symbolique hésite, le Bayesien prend le relais. En cas de contradiction majeure, le système passe en 'Diagnostic Complexe'.
  > *(Passage sur l'écran de Démo)* : Regardons l'application en direct.
  > Si je coche 'Fièvre', 'Toux' et 'Fatigue', nous constatons une **convergence totale** : le diagnostic 'Grippe' ressort à plus de 90% sur le bar chart Plotly, et l'onglet symbolique nous montre la trace d'inférence claire de la règle R1.
  > Si je coche des symptômes contradictoires comme 'Fièvre Élevée' seule, le moteur symbolique bloque, mais le moteur Bayesien et notre grille d'arbitrage réorientent immédiatement le patient vers un statut de précaution."*
  >

---

### Membre 5 : Évaluation, Cas Limites & Conclusion

* **Temps de parole :** 1 minute 45 secondes (06:15 $\rightarrow$ 08:00)
* **Diapositive support :** *Slide 5 - Benchmark, Cas Limites (`test_cases.json`) et Perspectives*
* **Script de parole :**
  > *"Pour valider notre prototype, j'ai mis en place un protocole d'évaluation automatisé dans `main.py` basé sur 10 cas de test dans `test_cases.json`, dont 3 cas limites très exigeants.
  > Sur les cas limites, comme le cas TC08 qui mélange des symptômes d'Allergie et de Grippe, ou le cas TC10 où l'utilisateur coche tous les symptômes, nous avons pu vérifier l'efficacité de notre sous-système de fusion. Là où un modèle simple aurait donné une prédiction aberrante avec une fausse certitude, notre système hybride détecte le conflit et bascule en 'Diagnostic Complexe' avec une confiance modérée de 35%, sécurisant la prise de décision.
  > En conclusion, l'hybridation des règles symboliques et des réseaux probabilistes nous permet d'allier l'explicabilité métier indispensable en santé à la robustesse face à l'incertitude. Merci pour votre attention, nous sommes à votre disposition pour les questions.et*
  >
