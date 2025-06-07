# 📚 Moteur de Recherche pour Bibliothèque Numérique

Projet de Master 2 – Science et Technologie du Logiciel  
Sorbonne Université

## 🧠 Présentation

Ce projet consiste en la création d’un **moteur de recherche performant** pour une bibliothèque numérique.  
Il permet aux utilisateurs de **rechercher, classer et explorer** des documents textuels à l’aide d’un ensemble d’algorithmes d’indexation, de centralité et de similarité.

> 🔍 L’objectif : permettre une navigation intuitive, rapide et pertinente au sein d’une grande collection de documents.

---

## 🛠️ Technologies Utilisées

### Backend
- **Python 3**
- **Flask** – API REST
- **Pandas / Numpy** – Traitement de données
- **Pickle (.pkl)** – Sérialisation d’objets (index, matrices)
- **TF-IDF**, Graphe de **Jaccard**, Centralités (Closeness, Betweenness, PageRank)

### Frontend
- **Angular** – Application Web et Mobile

### Stockage
- Objets sérialisés (`.pkl`) pour les structures suivantes :
  - Index inversé (Hashmap)
  - Matrice d’adjacence
  - Indices de centralité

---

## ⚡ Performances

- Temps de réponse : **quasi-instantané**
- Accès aux documents en temps constant grâce à la **structure hashmap**
- Données précalculées et chargées à la volée
- Tests de performance validés même sur des **requêtes complexes**

---

## 🧩 Fonctionnalités

- Recherche de documents textuels par mots-clés
- Classement des résultats selon la **pertinence (TF-IDF)** et la **centralité**
- Suggestions basées sur la **similarité Jaccard**
- Interface web/mobile ergonomique et fluide

---

## ⚠️ Limitations et Sécurité

- Les fichiers `.pkl` peuvent poser des problèmes :
  - Limitation mémoire pour objets très volumineux
  - Risques de sécurité si chargés depuis une source externe
- Pour un déploiement à grande échelle, on recommande :
  - Une **base de données relationnelle** (ex: PostgreSQL)
  - Ou un **cache en mémoire** (ex: Redis)

---

## 🚀 Lancer le Projet

### 1. Backend

```bash
cd backend
pip install -r requirements.txt
python app.py
```

### 2. Frontend

```bash
cd frontend
npm install
ng serve
```
