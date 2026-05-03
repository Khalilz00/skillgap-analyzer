PROMPT_TEMPLATE = """Tu es un extracteur de technologies pour des offres d'emploi.
TÂCHE : lis la description de l'offre d'emploi ci-dessous et renvoie la liste de toutes les technologies, outils, langages, frameworks, plateformes et méthodologies mentionnés.
RÈGLES :
- Renvoie UNIQUEMENT un objet JSON avec une clé "tech_stack" contenant une liste de chaînes.
- Inclus les noms de produits (ex: "Tableau", "JIRA"), langages (ex: "SQL", "Python"), concepts techniques (ex: "NoSQL", "Cloud"), méthodologies (ex: "SCRUM", "Agile").
- N'inclus PAS les soft skills, les diplômes, les métiers, les noms d'entreprises, les secteurs.
- Conserve les noms tels qu'ils apparaissent dans l'offre (respecte la casse et l'orthographe).
- Si aucune technologie n'est mentionnée, renvoie {{"tech_stack": []}}.
- Ne répète pas un même élément.

EXEMPLE 1:
Description : "Développeur back-end. Maîtrise de Python, Django et PostgreSQL. Expérience avec Docker appréciée. Méthodes agiles (Scrum)."
Réponse : {{"tech_stack": ["Python", "Django", "PostgreSQL", "Docker", "Scrum"]}}

EXEMPLE 2 :
Description : "Développeur back-end sur Python et PostgreSQL. Environnement AWS. Méthodes agiles (Scrum, Kanban). Outils : JIRA, Confluence. Notions de NoSQL appréciées."
Réponse : {{"tech_stack": ["Python", "PostgreSQL", "AWS", "Scrum", "Kanban", "JIRA", "Confluence", "NoSQL"]}}

EXEMPLE 3 :
Description : "Data Analyst junior, Bac+3 minimum. Maîtrise de Excel et Power BI. Qualités : rigueur, autonomie."
Réponse : {{"tech_stack": ["Excel", "Power BI"]}}

Offre à traiter :
"Description": {offer_text},
Réponse :

"""  # noqa: E501


def _extract_offer_description(offer: dict) -> str:
    return offer.get("description", "")


def build_prompt(offer: dict) -> str:
    """Construit le prompt complet à envoyer au LLM."""
    text = _extract_offer_description(offer)
    return PROMPT_TEMPLATE.format(offer_text=text)
