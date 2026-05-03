# 1. fetch data from bronze bucket GCS
# 2. for each offer, build the prompt and call the LLM to extract the tech stack
# 3. save the parsed offers in the silver bucket GCS

from datetime import date, datetime
from typing import Any

from skillgap.parsing.llm import LLMClient
from skillgap.parsing.prompt import build_prompt
from skillgap.parsing.schema import LLMExtraction, ParsedOffer


class ParsingPipeline:
    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client

    def parse_offer(self, offer: dict[str, Any]) -> ParsedOffer:
        prompt = build_prompt(offer)

        llm_response = self.llm_client.generate(prompt)

        # parse the LLM response into our schema
        extraction = LLMExtraction.model_validate_json(llm_response)
        parsed_offer = ParsedOffer(
            offer_id=offer["id"],
            title=offer["intitule"],
            created_at=datetime.fromisoformat(offer["dateCreation"].replace("Z", "+00:00")).date(),
            scrape_date=date.today(),
            location=offer.get("lieuTravail", {}).get("libelle"),
            seniority=offer.get("experienceLibelle"),
            contract_type=offer.get("typeContratLibelle"),
            rome_code=offer.get("romeCode"),
            tech_stack=extraction.tech_stack,
            company_name=offer.get("entreprise", {}).get("nom"),
        )
        return parsed_offer

    def parse_offers(self, offers: list[dict[str, Any]]) -> list[ParsedOffer]:
        return [self.parse_offer(offer) for offer in offers]
