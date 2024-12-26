# Projet : Tableau de Bord d'Analytique en Temps Réel avec Apache Spark et Kafka

## Architecture du Projet
![Architecture du Projet](architecture.jpeg)

---

## Aperçu du Projet
Dans ce projet, nous avons développé un pipeline d'analytique en temps réel qui traite des flux de données en direct, tels que les cours boursiers. En utilisant **Apache Kafka** pour l'ingestion des données et **Apache Spark** pour le traitement en temps réel, les données sont traitées en continu et visualisées dans un tableau de bord en direct (utilisant **Grafana**).

L'objectif de ce projet est de démontrer la capacité à gérer des données en temps réel, à les traiter efficacement et à présenter des insights actionnables visuellement. Le résultat final est un tableau de bord entièrement fonctionnel qui se met à jour au fur et à mesure que les données arrivent, fournissant des insights immédiats comme les tendances des cours boursiers.

---

## Étapes Impliquées

### 1. 🚀 Ingestion des Données avec Apache Kafka
- **Kafka** sert de système pour le streaming de données en temps réel. Il permet l'intégration facile de diverses sources de données, telles que les cours boursiers via Yahoo Finance.
- Un **producteur Kafka** pousse continuellement les données en direct dans un topic Kafka, tandis qu'un **consommateur Kafka** tire les données pour un traitement ultérieur.

### 2. ⚙️ Traitement des Données en Temps Réel avec Apache Spark
- **Spark** est utilisé pour effectuer des tâches de traitement de données en temps réel, telles que le calcul des moyennes mobiles ou le nettoyage des données.
- **Spark Streaming**, un composant de Spark, permet le calcul continu, permettant ainsi le traitement des données dès qu'elles sont ingérées depuis Kafka.
- Exemples de tâches de traitement :
  - Pour les cours boursiers : calcul des moyennes de prix sur une fenêtre de 1 minute.

### 3. 📊 Visualisation des Données avec un Tableau de Bord
- Un tableau de bord en direct est créé en utilisant **Grafana** pour visualiser les données traitées.
- Le tableau de bord reflète les mises à jour en temps réel, affichant les tendances des données, les analyses et d'autres métriques utiles à l'utilisateur.
- Exemples de visualisations :
  - Un graphique linéaire montrant les changements de prix des actions au fil du temps.

---

## Problèmes Potentiels et Solutions
- **Gestion de la Perte de Données** : Dans le streaming en temps réel, il y a un risque de perte de données lors des défaillances. Pour gérer cela, nous utilisons les fonctionnalités tolérantes aux pannes de Kafka et activons le checkpointing de Spark pour assurer la récupération après une défaillance.
- **Mise à l'Échelle** : Si le jeu de données augmente ou si les flux de données deviennent trop volumineux pour une machine locale, envisagez d'optimiser les configurations de Spark et Kafka, ou d'utiliser un échantillon de données plus petit à des fins de démonstration.

---

## Alternatives d'Acquisition de Données
- **Données Réelles** : Nous avons connecté Yahoo Finance pour les cours boursiers en temps réel. Ces sources fournissent d'excellents exemples de flux de données rapides qui sont parfaits pour le traitement en temps réel.
- **Données Simulées** : Si l'accès aux API en direct est restreint (en raison de limites ou de coûts), vous pouvez simuler des flux de données en utilisant des scripts Python. Cette méthode vous permettra de contrôler le flux de données et de reproduire un environnement de streaming en temps réel.

---

## Outils Alternatifs
- Si vous rencontrez des problèmes avec Kafka et Spark, vous pourriez utiliser des alternatives telles qu'**Apache Flink** pour le traitement de flux ou **RabbitMQ** pour le courtage de messages au lieu de Kafka. De même, le tableau de bord pourrait être construit en utilisant **Power BI** si Grafana ne convient pas à vos besoins.

---

## Résultat du Projet
À la fin de ce projet, nous avons un tableau de bord d'analytique en temps réel qui se met à jour en continu en fonction des flux de données entrants. L'ensemble du pipeline, de l'ingestion des données à la visualisation, démontre comment les technologies modernes de big data peuvent être utilisées pour la prise de décision et la surveillance en temps réel, une exigence essentielle dans les environnements axés sur les données d'aujourd'hui. Ce projet améliore votre compréhension de l'architecture des données en streaming, du traitement avec Spark et de la création de tableaux de bord perspicaces pour l'analytique en temps réel.

---

## Technologies Utilisées
- **Yahoo Finance** : Pour l'acquisition des données boursières en temps réel.
- **Kafka** : Pour l'ingestion des données en streaming.
- **Zookeeper** : Pour la coordination des services Kafka.
- **Spark** : Pour le traitement des données en temps réel.
- **InfluxDB** : Pour le stockage des données temporelles.
- **Grafana** : Pour la visualisation des données en temps réel.
- **Docker Compose** : Pour la gestion et l'orchestration des conteneurs.

---

## Comment Démarrer
1. **Cloner le dépôt** :
   ```bash
   git clone https://github.com/votre-repo/projet-big-data.git
   cd projet-big-data
   ```
2. **Démarrer les services avec Docker Compose** :
   ```bash
   docker-compose up -d --build
   ```
3. **Accéder au tableau de bord Grafana** :
   Ouvrez votre navigateur et accédez à `http://localhost:3000` pour visualiser les données en temps réel.

---

## Contribution
Les contributions sont les bienvenues ! Veuillez ouvrir une issue ou soumettre une pull request pour toute amélioration ou correction.

---

## Licence
Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

