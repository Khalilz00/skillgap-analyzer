import os
from datetime import date

from skillgap.parsing.llm import LLMClient
from skillgap.parsing.pipeline import ParsingPipeline
from skillgap.storage.bronze import GCSBronzeStorage
from skillgap.storage.silver import GCSSilverStorage

# 1. Récupérer les buckets depuis env
bucket_bronze = os.environ["GCS_BUCKET_BRONZE"]
bucket_silver = os.environ["GCS_BUCKET_SILVER"]


bronze = GCSBronzeStorage(bucket_bronze)

silver = GCSSilverStorage(bucket_silver)

# 2. Lire les offres depuis bronze
offers = bronze.read("france_travail", date(2026, 4, 18))  # adapte la date

# 3. Parser
llm = LLMClient("/home/kzanzouri/skillgap-analyzer/models/qwen2.5-3b-instruct-q4_k_m.gguf")
pipeline = ParsingPipeline(llm)


# boucle
parsed_offers = []
errors = 0
for i, one_offer in enumerate(offers):
    try:
        parsed = pipeline.parse_offer(one_offer)
        parsed_offers.append(parsed)
        print(f"[{i + 1}/{len(offers)}] OK: {one_offer['id']}")
    except Exception as e:
        errors += 1
        print(f"[{i + 1}/{len(offers)}] FAIL: {one_offer['id']} — {e}")

silver.write(parsed_offers, "france_travail", date.today())
print(f"Terminé: {len(parsed_offers)} succès, {errors} échecs")
