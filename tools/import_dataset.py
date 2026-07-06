#!/usr/bin/env python3
"""
RésiHub — Convertisseur de banques de QCM existantes -> format RésiHub.

Prend un dataset ouvert (MedMCQA, MedQA...) et produit un JSON importable dans RésiHub,
chaque question taguée `status: draft` + `src` (à faire valider par un médecin).

[!] AVANT USAGE :
  1. VÉRIFIE LA LICENCE du dataset (usage commercial autorisé ?).
       - MedQA   : licence MIT (permissif).  https://github.com/jind11/MedQA
       - MedMCQA : "open source" — vérifie la page HuggingFace avant tout produit payant.
                   https://huggingface.co/datasets/openlifescienceai/medmcqa
  2. Ces QCM sont en ANGLAIS et calibrés pour d'autres concours (Inde/USA) :
     il faut TRADUIRE et RÉALIGNER sur le programme du résidanat algérien.
  3. Ils entrent en `draft` : RELECTURE PAR UN MÉDECIN obligatoire avant révision réelle.

Usage :
  python tools/import_dataset.py entree.jsonl -o data/questions.imported.json --limit 2000
  # formats acceptés : .json (tableau) ou .jsonl (une ligne = un objet JSON)
"""
import argparse, json, hashlib

# MedMCQA subject_name (anglais) -> clé de matière RésiHub (approximatif, à affiner).
SUBJ_MAP = {
    'microbiology': 'infectio', 'psychiatry': 'neuro', 'ent': 'pneumo',
    # le reste tombe sur 'divers' (visible en session "mix", pas en carte matière).
}


def norm_subject(name):
    return SUBJ_MAP.get(str(name or '').strip().lower(), 'divers')


def load_rows(path):
    txt = open(path, encoding='utf-8').read().strip()
    if not txt:
        return []
    if path.endswith('.jsonl'):
        return [json.loads(l) for l in txt.splitlines() if l.strip()]
    data = json.loads(txt)
    return data if isinstance(data, list) else data.get('questions', data.get('data', []))


def conv_medmcqa(r, cop_base):
    opts = [str(o).strip() for o in (r.get('opa'), r.get('opb'), r.get('opc'), r.get('opd'))
            if o not in (None, '')]
    if len(opts) < 2:
        return None
    cop = r.get('cop')
    if cop is None:
        return None
    a = int(cop) - (1 if cop_base == 1 else 0)
    q = str(r.get('question', '')).strip()
    if not q or a < 0 or a >= len(opts):
        return None
    return {'s': norm_subject(r.get('subject_name')), 'd': 2, 'q': q, 'o': opts, 'a': a,
            'e': str(r.get('exp') or '—').strip(), 'src': 'MedMCQA', 'status': 'draft'}


def conv_medqa(r):
    q = str(r.get('question', '')).strip()
    opt = r.get('options')
    if isinstance(opt, dict):
        keys = sorted(opt.keys())
        opts = [str(opt[k]).strip() for k in keys]
        ans = r.get('answer_idx') or r.get('answer')
        a = keys.index(ans) if ans in keys else None
    elif isinstance(opt, list):
        opts = [str(o).strip() for o in opt]
        ans = r.get('answer_idx')
        a = int(ans) if str(ans).isdigit() else None
    else:
        return None
    if not q or a is None or a < 0 or a >= len(opts) or len(opts) < 2:
        return None
    return {'s': 'divers', 'd': 2, 'q': q, 'o': opts, 'a': a,
            'e': str(r.get('explanation') or '—').strip(), 'src': 'MedQA', 'status': 'draft'}


def detect(r):
    if 'opa' in r:
        return 'medmcqa'
    if 'options' in r:
        return 'medqa'
    return None


def main():
    ap = argparse.ArgumentParser(description='Convertit MedMCQA/MedQA -> format RésiHub.')
    ap.add_argument('input', help='fichier .json (tableau) ou .jsonl')
    ap.add_argument('-o', '--output', default='data/questions.imported.json')
    ap.add_argument('--format', choices=['auto', 'medmcqa', 'medqa'], default='auto')
    ap.add_argument('--limit', type=int, default=0, help='0 = tout')
    ap.add_argument('--cop-base', type=int, choices=[0, 1], default=0,
                    help='MedMCQA : bonne réponse indexée à partir de 0 ou de 1')
    args = ap.parse_args()

    rows, out, seen = load_rows(args.input), [], set()
    for r in rows:
        fmt = args.format if args.format != 'auto' else detect(r)
        item = (conv_medmcqa(r, args.cop_base) if fmt == 'medmcqa'
                else conv_medqa(r) if fmt == 'medqa' else None)
        if not item:
            continue
        item['id'] = 'imp' + hashlib.md5(item['q'].encode('utf-8')).hexdigest()[:10]
        if item['id'] in seen:
            continue
        seen.add(item['id'])
        out.append(item)
        if args.limit and len(out) >= args.limit:
            break

    payload = {'meta': {'note': 'Importé — statut draft. VÉRIFIER LA LICENCE, TRADUIRE, '
                                'FAIRE VALIDER PAR UN MÉDECIN avant usage réel.',
                        'count': len(out)},
               'questions': out}
    json.dump(payload, open(args.output, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'OK -> {args.output}  ({len(out)} QCM convertis, statut draft)')
    print('RAPPEL : licence à vérifier · anglais -> traduire · relecture médecin obligatoire.')


if __name__ == '__main__':
    main()
