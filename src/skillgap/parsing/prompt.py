from typing import Any

PROMPT_TEMPLATE = """Tu es un extracteur de technologies pour des offres d'emploi.

TÂCHE : lis la description de l'offre ci-dessous et renvoie UNIQUEMENT les technologies concrètes mentionnées (outils, logiciels, langages, frameworks, plateformes nommées).

RÈGLES STRICTES :
- Renvoie UNIQUEMENT un objet JSON avec une clé "tech_stack" contenant une liste de chaînes.
- INCLURE :
  * Langages de programmation (Python, Java, SQL, TypeScript, ...)
  * Frameworks et librairies (Django, React, Spark, LangChain, ...)
  * Bases de données nommées (PostgreSQL, MongoDB, BigQuery, Snowflake, ...)
  * Outils nommés (Docker, Kubernetes, Git, JIRA, Tableau, Power BI, ...)
  * Plateformes cloud nommées (AWS, GCP, Azure, ...)
  * Services cloud nommés (S3, Lambda, BigQuery, Vertex AI, ...)
- EXCLURE ABSOLUMENT :
  * Méthodologies et processus (Agile, Scrum, Kanban, DevOps, MLOps, DataOps, CI/CD, TDD, BDD)
  * Concepts génériques (Cloud, Big Data, Machine Learning, IA, Data Science, NoSQL, ETL, Data Warehouse, Data Lake)
  * Pratiques et architectures (Architecture Hexagonale, Domain Driven Design, microservices, REST, API)
  * Domaines fonctionnels (BackOffice, FrontOffice, BI, Data Quality, Data Privacy, Data Security, Data Integration)
  * Soft skills, diplômes, métiers, secteurs, noms d'entreprises
  * Sigles trop génériques (SI, IT, R&D)
- Conserve la casse standard (ex: "PostgreSQL" pas "PostGres", "GitLab" pas "Gitlab", "JIRA" pas "Jira").
- Pas de doublons, pas de variantes du même outil (choisis la plus standard).
- Si aucune technologie concrète, renvoie {{"tech_stack": []}}.

EXEMPLE 1 :
Description : "Développeur back-end. Maîtrise de Python, Django et PostgreSQL. Expérience avec Docker appréciée. Méthodes agiles (Scrum)."
Réponse : {{"tech_stack": ["Python", "Django", "PostgreSQL", "Docker"]}}

EXEMPLE 2 :
Description : "Data engineer sur GCP. Stack: Python, BigQuery, dbt, Airflow. Connaissance Spark un plus. Pratiques DevOps et CI/CD via GitLab. Architecture microservices."
Réponse : {{"tech_stack": ["Python", "BigQuery", "dbt", "Airflow", "Spark", "GitLab", "GCP"]}}

EXEMPLE 3 :
Description : "Data Analyst junior, Bac+3 minimum. Maîtrise de Excel et Power BI. Connaissance SQL. Qualités : rigueur, autonomie. Méthode agile."
Réponse : {{"tech_stack": ["Excel", "Power BI", "SQL"]}}

EXEMPLE 4 :
Description : "Chef de projet IT, animation d'équipe agile, sécurité et qualité des données. Diplômé Bac+5."
Réponse : {{"tech_stack": []}}

Offre à traiter :
"Description": {offer_text}
Réponse :
"""  # noqa: E501


def _extract_offer_description(offer: dict[str, Any]) -> str:
    description = offer.get("description", "")
    if not isinstance(description, str):
        return ""
    return description


def build_prompt(offer: dict[str, Any]) -> str:
    """Construit le prompt complet à envoyer au LLM."""
    text = _extract_offer_description(offer)
    return PROMPT_TEMPLATE.format(offer_text=text)
