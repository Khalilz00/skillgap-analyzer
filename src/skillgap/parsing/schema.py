from datetime import date

from pydantic import BaseModel


class LLMExtraction(BaseModel):
    tech_stack: list[str]


class ParsedOffer(BaseModel):
    # Identifiants & métadonnées
    offer_id: str  # "id"
    title: str  # "intitule"
    created_at: date  # "dateCreation" (date de création de l'offre)
    scrape_date: date  # aujourd'hui (quand tu as parsé)

    # Axes d'analyse du dashboard
    location: str | None = None  # "lieuTravail.libelle"
    seniority: str | None = None  # "experienceLibelle"
    contract_type: str | None = None  # "typeContratLibelle"
    rome_code: str | None = None  # "romeCode"

    # Le cœur du projet
    tech_stack: list[str]  # extrait par le LLM

    # Traçabilité (utile pour du debug plus tard)
    company_name: str | None = None  # "entreprise.nom"
