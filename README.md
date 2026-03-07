# PyXOR-SSH-PoC : Simulation de Ransomware Éducatif

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![Sécurité](https://img.shields.io/badge/Recherche-Sécurité-red?style=for-the-badge)
![Protocole](https://img.shields.io/badge/Protocole-SSH-orange?style=for-the-badge)

> **⚠️ AVERTISSEMENT & CADRE ÉTHIQUE**
>
> Ce projet a été développé **strictement à des fins éducatives et de recherche**. Il vise à démontrer le fonctionnement bas niveau des algorithmes de chiffrement (XOR) et l'automatisation de protocoles réseau sécurisé.
>
> * **Sécurité par Conception (Safety by Design) :** La clé de déchiffrement est explicitement affichée à l'utilisateur en permanence (Console & Interface Graphique).
> * **Aucune Malveillance :** Ce programme ne contient aucun mécanisme d'évasion ou de propagation réseau (Worm), il contient néanmoins un mécanisme de persistance, dans le but d'explorer cet aspect de la killchain.
> * **Environnement Contrôlé :** Conçu pour être exécuté exclusivement dans une Machine Virtuelle (VM) Windows isolée.

---

## 📋 Présentation du Projet

**PyXOR-SSH-PoC** est une simulation de ransomware développée à la main ("from scratch") pour étudier l'implémentation des différentes phases de la killchain (phases 5, 6 et 7), le développement de compétences en algorithmie et en compréhension du langage python ainsi que de se donner une meilleure interprétation du panorama des risques cyber, grâce à cet exercice "d'immersion".

Contrairement aux implémentations standards qui reposent sur des librairies cryptographiques pré-faites (comme OpenSSL ou PyCrypto) ou des protocoles HTTP, ce projet se concentre sur :

1.  **La Cryptographie Manuelle :** Implémentation d'un algorithme de chiffrement symétrique à la main utilisant des opérations bit à bit.
2.  **Transport Sécurisé :** Utilisation du **protocole SSH** pour simuler un canal de Command & Control (C2) robuste pour la négociation des clés ainsi que l'expérimentation des communications programme-serveurs, que je n'avais jamais expérimenté jusque-là.

Ce projet sert d'étude pratique en ingénierie logicielle Python, en automatisation système et en analyse défensive de malwares.

---

## 🛠️ Architecture & Flux de Données

L'architecture est divisée en un **Serveur** (Générateur de Clés) et un **Client** (La Charge Utile), communiquant via un tunnel SSH sécurisé, grâce à paramiko.

```mermaid 
sequenceDiagram
    participant User as 👤 Victime
    participant Script as 🐍 Ransomware
    participant Server as ☁️ Serveur C2 (SSH)

    Note over Script, Server: 1. Initialisation
    Script->>Server: Demande de clé (via SSH)
    Server-->>Script: Génère et renvoie la clé

    Note over Script: 2. Attaque (Boucle locale)
    Script->>Script: Chiffre les fichiers (XOR)
    Script->>Script: Ajoute extension .locked

    Note over User, Script: 3. Résolution (GUI)
    Script->>User: Affiche fenêtre + Clé de secours
    User->>Script: Entre la clé et valide
    Script->>Script: Déchiffre les fichiers
    Script-->>User: Fin du programme
