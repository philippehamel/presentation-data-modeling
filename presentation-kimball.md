---
marp: true
theme: dark-custom
---

# What the Fact? Dim'en plus!
## Ou
## Introduction à la modélisation dimensionelle

<div class="gif-container">
  <img src="assets/joke-pun.gif">
</div>

---

# Un peu d'histoire
- ~1990 Bill Inmon formalise l'idée d'un entrepôt de donné moderne (Top Down)
  - Objectif: être une source de vérité qui représente la structure et les processus de l'entreprise 
  - Séparation de l'opérationnel et de l'analytique
  - Infrastructure optimisé pour des besoins analytique
  - Utilisation de Data Mart normalisés
  - Optimiser pour la réalité de l'époque, storage et calcul coûteux, lié et on-premise
  
- 1996 Ralph Kimball formalise sa version d'un entrepôt de donné moderne (Bottom Up)
  - Objectif: Bâtir sur la fondation de Inmon, mais prioriser la flexibilité et la simplicité
  - Formalise une approche dimensionnelle qui demande plus de storage mais moins de calcul tout en conservant la qualité des donnés et la mémoire historique
  - Hautement pratique dans un monde les technologies infonuagique permettent d'accèder de manière flexible et abordable au storage

---

# L'approche de Kimball 
## (Star Schema)
<div class="txt_left">
  <li>Fact Tables (fct_table)
    <ul>
      <li>Granulaire</li>
      <li>Longue</li>
      <li>Mesurable (habituellement)</li>
    </ul>
  </li>
  <li>Dimension Tables (dim_table)
    <ul>
      <li>Large</li>
      <li>Slowly Changing Dimensions</li>
      <li>Normalisation</li>
    </ul>
  </li>
</div>
<div class="img">
  <img src="assets/basic_star.svg">
</div>

---

# Exemple appliqué dans mon sand box préféré
## MLB Data