/**
 * RésiHub — squelette d'API (prototype).
 * Sert le frontend statique + endpoints de base.
 * Les blocs « TODO » sont à implémenter avec une vraie base de données + authentification.
 *
 * Démarrer :  npm install  &&  npm run dev   →   http://localhost:8080
 */
const path = require('path');
const express = require('express');
const cors = require('cors');
require('dotenv').config();

const app = express();
app.use(cors());
app.use(express.json());

// Frontend statique (landing index.html + prototype app.html)
app.use(express.static(path.join(__dirname, '..')));

// Santé
app.get('/api/health', (_req, res) => res.json({ ok: true, service: 'resihub-api' }));

// Banque de QCM (démo : lit le fichier JSON ; en prod → base de données)
const bank = require('../data/questions.sample.json');
app.get('/api/questions', (req, res) => {
  // TODO(auth): vérifier l'utilisateur + son abonnement avant de servir le contenu réel.
  const { subject } = req.query;
  let items = bank.questions;
  if (subject) items = items.filter(q => q.subject === subject);
  // TODO(sécurité): ne pas renvoyer `answer`/`explanation` avant que l'utilisateur ait répondu.
  res.json({ meta: bank.meta, count: items.length, questions: items });
});

// Abonnement : crée une session Stripe Checkout (clé secrète côté serveur uniquement)
app.post('/api/checkout', async (req, res) => {
  if (!process.env.STRIPE_SECRET_KEY) {
    return res.status(501).json({ error: 'STRIPE_SECRET_KEY manquant — renseignez .env (voir .env.example).' });
  }
  const plan = req.body && req.body.plan === 'mensuel' ? 'mensuel' : 'annuel';
  const price = plan === 'mensuel' ? process.env.STRIPE_PRICE_MONTHLY : process.env.STRIPE_PRICE_ANNUAL;
  if (!price) return res.status(501).json({ error: `Price ID Stripe manquant pour le plan « ${plan} ».` });
  try {
    const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);
    const base = process.env.PUBLIC_URL || `http://localhost:${process.env.PORT || 8080}`;
    const session = await stripe.checkout.sessions.create({
      mode: 'subscription',
      line_items: [{ price, quantity: 1 }],
      success_url: `${base}/app.html?paid=1`,
      cancel_url: `${base}/app.html?canceled=1`,
    });
    res.json({ url: session.url });
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
});

// TODO(webhook): app.post('/api/stripe/webhook', express.raw({type:'application/json'}), ...)
//   → activer l'abonnement de l'utilisateur à la réception de checkout.session.completed.
// TODO(auth): inscription / connexion (email + mot de passe ou lien magique), sessions/JWT,
//   table `users`, progression par utilisateur, gate d'abonnement sur /api/questions.

const PORT = process.env.PORT || 8080;
app.listen(PORT, () => console.log(`RésiHub → http://localhost:${PORT}`));
