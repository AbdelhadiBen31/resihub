# RésiHub

Plateforme de préparation au **concours de résidanat de médecine**, destinée aux étudiants en médecine.
Révision intensive et **gamifiée** : banques de QCM, examens blancs, progression, séries, classement.
Modèle : **abonnement** (mensuel / annuel), contenu 100 % numérique.

> **État actuel : prototype.** L'interface et le moteur de QCM fonctionnent (démo jouable).
> Le contenu, l'authentification, les paiements réels et la base de données restent à construire (voir la roadmap).

## Ce qui est réel vs à construire

| Élément | État |
|---|---|
| Interface (dashboard, quiz, classement, paywall) | ✅ Prototype fonctionnel (`app.html`) |
| Moteur de QCM gamifié (XP, niveaux, séries, badges, progression) | ✅ Fonctionne, données en `localStorage` |
| Page vitrine | ✅ `index.html` (déployée) |
| Squelette d'API (Node/Express) | ✅ `server/` — endpoints de base + TODO |
| Schéma de données QCM | ✅ `data/questions.sample.json` |
| Intégration Stripe (paiement réel) | 🟠 Squelette prêt, à brancher avec vos clés |
| Authentification / comptes | ❌ À implémenter |
| Base de données + progression par utilisateur | ❌ À implémenter |
| **Contenu : 100 000 QCM validés** | ❌ À produire — **doit être rédigé/relu par des médecins** |

### Deux principes non négociables
- **Pas de QCM médicaux inventés en masse.** Des questions fausses mettraient en danger de futurs médecins. Le contenu doit venir de médecins / sources fiables et être relu.
- **Pas de scraping de contenu protégé.** Aspirer puis revendre du contenu payant est illégal. On agrège/renvoie vers des ressources **libres et licenciées**, ou on produit du contenu original.

## Structure

```
.
├── index.html                  # Page vitrine (déployée sur GitHub Pages)
├── app.html                    # Prototype de l'application (démo jouable)
├── data/
│   └── questions.sample.json   # Schéma + QCM de démonstration
├── server/
│   └── index.js                # API Express (statique + /api/questions + /api/checkout)
├── docs/
│   └── ROADMAP.md              # Feuille de route produit & technique
├── .env.example                # Variables d'environnement (Stripe, DB…)
├── package.json
└── .gitignore
```

## Lancer en local

Sans backend (juste le front) :
```bash
python -m http.server 8080      # puis ouvrir http://localhost:8080/app.html
```

Avec l'API (Stripe, questions servies par le serveur) :
```bash
npm install
cp .env.example .env            # renseigner les clés Stripe de TEST
npm run dev                     # http://localhost:8080
```

## Stratégie de contenu (les 100 000 QCM, légalement)
1. **Auteurs médecins / résidents** rémunérés pour rédiger et relire par lot.
2. **Licences** de banques existantes auprès d'éditeurs / facultés partenaires.
3. **Génération assistée + relecture experte obligatoire** (jamais publié sans validation médicale).
4. **Contributions** encadrées d'enseignants, avec workflow de revue.
5. **Import de banques ouvertes existantes** (voir ci-dessous) — le chemin le plus rapide vers le volume.

### Importer une banque existante (aller vers le volume)
Des datasets de QCM médicaux existent déjà en grand nombre, en accès ouvert :
- **MedQA** (licence MIT) — https://github.com/jind11/MedQA
- **MedMCQA** (~194k QCM ; licence à vérifier) — https://huggingface.co/datasets/openlifescienceai/medmcqa

Le convertisseur les transforme au format RésiHub :
```bash
python tools/import_dataset.py chemin/medmcqa.jsonl -o data/questions.imported.json --limit 2000
```
Puis dans l'app : onglet **Contribuer → Importer → Fichier JSON**.

**Avant tout usage réel :** (1) vérifier la **licence** (usage commercial), (2) ces QCM sont en **anglais** et calibrés pour d'autres concours → **traduire + réaligner** sur le programme algérien, (3) ils entrent en `draft` → **relecture médecin obligatoire**. Ne commite pas un dataset redistribué sur un dépôt public sans licence adaptée.

## Roadmap
Voir [`docs/ROADMAP.md`](docs/ROADMAP.md).

---
Prototype. Ne pas utiliser le contenu de démonstration pour réviser réellement.
