---
marp: true
theme: dark-custom
---

# What the Fact? Dim'en plus!

## Ou

## Introduction à la modélisation dimensionnelle

<div class="gif-container">
  <img src="assets/joke-pun.gif">
</div>

---

# Pourquoi?

## Être capable de répondre à des questions analytiques du genre :

- Quelle est la moyenne de vente pour nos utilisateurs à Montréal?
- Quelle catégorie de produits a eu la meilleure croissance de revenus pendant le dernier trimestre financier?
- Quels sont les joueurs nés aux USA qui ont frappé la balle avec le plus de vélocité pendant la dernière série de 3 matchs entre les Blue Jays et les Rockies?

---

# Rangée (OLTP) VS Colonne (OLAP)

<div class="img">
  <img src="assets/row-vs-col.png">
</div>

---

# L'approche de Kimball

## Deux composantes importantes :

1. fact table (préfixe fct\_)
2. dimension table (préfixe dim\_)

<div class="img">
  <img src="assets/basic-star.svg">
</div>

---

# Exemple appliqué dans mon sandbox préféré

## Nous allons modéliser une saison de baseball

<div class="gif-container">
  <img src="assets/shrug.gif">
</div>

---

# Méthode standard

- Choisir un processus d'affaires: Performance des joueurs
- Déclarer le grain: Niveau le plus bas de détails
- Identifier les dimensions: Attributs descriptifs utilisés pour filtrer, grouper et étiqueter
- Identifier les faits: Mesures quantitatives

---

# Techniques fact tables

- Transactionnel: chacun des lancers
- Accumulative: présence au bâton ou match
- Snapshot: positionnement dans le classement à chaque semaine

---

# Techniques dimension tables

- Slowly changing dimensions sont des dimensions dont les attributs évoluent lentement au fil du temps
  - **Type 0** : Aucun changement
  - **Type 1** : Écrasement des valeurs
  - **Type 2** : Conservation de l'historique

<div class="scd-example">

**Exemple SCD Type 2 - Transfert de joueur :**
| Joueur | ID | Équipe | Date début | Date fin | Actif |
| ------------ | ------ | ------- | ---------- | ---------- | ----- |
| Danny Jansen | 643376 | **TOR** | 2018-08-15 | 2100-01-01 | true |

devient:

| Joueur       | ID     | Équipe  | Date début | Date fin   | Actif |
| ------------ | ------ | ------- | ---------- | ---------- | ----- |
| Danny Jansen | 643376 | **TOR** | 2018-08-15 | 2024-07-27 | false |
| Danny Jansen | 643376 | **BOS** | 2024-07-27 | 2100-01-01 | true  |

</div>

---

# Qu'est-ce que la normalization
<div class="img">
  <img src="assets/normalization-example.svg">
</div>

---

# Techniques dimension tables

- Normalisation
  - **Schéma en étoile** : Dimensions dénormalisées
  - **Schéma en flocon (3NF)** : Dimensions normalisées
  - **Une grosse table** : Complètement dénormalisé

<div class="comparison-container">
  <div class="comparison-item">
    <h3>Star Schema</h3>
    <img src="assets/mlb-star.svg" alt="MLB Star Schema">
    <p>Moins de jointures, meilleure vélocité des requêtes</p>
  </div>
  
  <div class="comparison-item">
    <h3>Snowflake Schema</h3>
    <img src="assets/mlb-snowflake.svg" alt="MLB Snowflake Schema">
    <p>Plus de jointures, meilleure performance de stockage</p>
  </div>
</div>

---

# Résultats

**Exemple : Joueurs nés aux USA avec la plus haute vélocité de balle frappée**

<div class="queries-container">
  <div class="query-item">
    <h3>Star Schema</h3>
    <pre><code>SELECT p.full_name, p.birth_country,
  ROUND(AVG(f.launch_speed), 2) as avg_exit_velocity
FROM star_fact_pitch f
JOIN star_dim_player p 
  ON f.player_id_batter_fk = p.player_id
WHERE p.birth_country = 'USA'
  AND f.launch_speed > 0
GROUP BY p.player_id, p.full_name, p.birth_country
HAVING COUNT(*) >= 5
ORDER BY avg_exit_velocity DESC 
LIMIT 10;</code></pre>
  </div>
  
  <div class="query-item">
    <h3>Snowflake Schema</h3>
    <pre><code>SELECT p.full_name, bl.birth_country,
  ROUND(AVG(f.launch_speed), 2) as avg_exit_velocity
FROM snowflake_fact_pitch f
JOIN snowflake_dim_player p 
  ON f.player_key_batter = p.player_key
JOIN snowflake_dim_birth_location bl 
  ON p.location_key = bl.location_key
WHERE bl.birth_country = 'USA'
  AND f.launch_speed > 0
GROUP BY p.player_key, p.full_name, bl.birth_country
HAVING COUNT(*) >= 5
ORDER BY avg_exit_velocity DESC 
LIMIT 10;</code></pre>
  </div>
</div>

---

# One Big Table

**Même exemple : Simplicité maximale, aucune jointure**

<div class="single-query-container">
  <div class="single-query-item">
    <h3>One Big Table</h3>
    <pre><code>SELECT batter_full_name as full_name, batter_birth_country as birth_country,
  ROUND(AVG(launch_speed), 2) as avg_exit_velocity
FROM one_big_table
WHERE batter_birth_country = 'USA'
  AND launch_speed IS NOT NULL
  AND launch_speed > 0
GROUP BY batter, full_name, birth_country
HAVING COUNT(*) >= 5
ORDER BY avg_exit_velocity DESC 
LIMIT 10;</code></pre>
  </div>
</div>

---

# Style 'opérationnel'

<div class="single-query-container">
  <div class="single-query-item">
    <h3>Operational</h3>
    <pre><code>
SELECT
    CONCAT(p.firstName, ' ', p.lastName) as fullName,
    c.name as birthCountry,
    ROUND(AVG(pb.exitVelocity), 2) as avgExitVelocity,
    COUNT(*) as totalBattedBalls
FROM Player p
JOIN Country c ON p.birthCountryId = c.id
JOIN PlayerStatistic ps ON ps.playerId = p.id
JOIN PitchByPitch pb ON pb.batterStatisticId = ps.id
WHERE c.code = 'USA'
    AND pb.exitVelocity IS NOT NULL
    AND pb.exitVelocity > 0
    AND pb.ballInPlay = true
GROUP BY p.id, p.firstName, p.lastName, c.name
HAVING COUNT(*) >= 5
ORDER BY avgExitVelocity DESC
LIMIT 10;
</code></pre>
  </div>
</div>

---

# Conclusion

Avec l'approche dimensionnelle vous possédez plusieurs leviers :

- Granularité
- Normalisation
- SCD

Pour optimiser les caractéristiques que vos requis demandent :

- Clarté pour les utilisateurs
- Fiabilité historique
- Vélocité des requêtes
- Vélocité de l'écriture
- Minimiser le stockage

---

# Mon avantage favori

## Clarté

Le gain de clarté de la modélisation dimensionnelle accélère le développement, facilite la maintenance et promeut la fiabilité.

<div class="big-img">
  <img src="assets/dying-hill.jpg">
</div>

---

# Wow Phil c'était tellement intéressant, mais où en apprendre plus?

- Data warehouse toolkit de Ralph Kimball et ressources en ligne du Kimball Group
- Joe Reiss Practical Data Modeling blog
- Ben Rogojan Seattle Data Guy blog
- Approches non dimensionnelles (exemple Data Vault ou Anchor)

<div class="gif-container">
  <img src="assets/tell-us-more.gif">
</div>

---

<div class="big-img">
  <img src="assets/frame.png">
</div>
