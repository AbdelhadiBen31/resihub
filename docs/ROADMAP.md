# RésiHub — Feuille de route

## Architecture cible
- **Front** : app statique (le prototype actuel peut évoluer en React/Vite si besoin), hébergée sur GitHub Pages / Vercel.
- **API** : Node/Express (dossier `server/`) sur Railway / Render.
- **Base de données** : Postgres (Supabase) — `users`, `subscriptions`, `questions`, `attempts`, `progress`.
- **Paiement** : Stripe (abonnements) + webhook pour activer/désactiver l'accès.
- **Auth** : email + mot de passe ou lien magique ; sessions/JWT.

## Phase 1 — Fondations (MVP payant)
- [ ] Authentification (inscription / connexion) + comptes utilisateurs.
- [ ] Brancher Stripe Checkout (clés live) + webhook → activer l'abonnement.
- [ ] Gate d'abonnement : `/api/questions` ne sert le contenu qu'aux abonnés.
- [ ] Progression persistée côté serveur (remplacer `localStorage`).
- [ ] Un premier lot de **QCM validés par des médecins** (une matière complète).

## Phase 2 — Contenu & expérience
- [ ] Montée en volume du contenu (auteurs / licences / relecture experte).
- [ ] Examens blancs chronométrés, corrigés détaillés, illustrations.
- [ ] Statistiques fines (points faibles, révision espacée / spaced repetition).
- [ ] Classements et objectifs hebdomadaires réels.

## Phase 3 — Croissance
- [ ] Application mobile (PWA puis natif).
- [ ] Moyens de paiement adaptés à l'Algérie (CIB / EDAHABIA + cartes internationales).
- [ ] Programme d'affiliation étudiants, offres facultés.
- [ ] Modération et contributions encadrées.

## Points de vigilance
- **Exactitude médicale** : aucun QCM publié sans relecture d'un médecin. C'est la valeur (et la responsabilité) du produit.
- **Droit d'auteur** : contenu original ou licencié uniquement — pas de scraping.
- **Données** : les données de santé/étudiants imposent une politique de confidentialité claire et un hébergement conforme.
- **Structure juridique** : la micro-entreprise convient au démarrage ; passer en société (SASU/SAS) dès qu'il y a des associés ou des revenus significatifs.
