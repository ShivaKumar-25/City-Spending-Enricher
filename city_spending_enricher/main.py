import logging
from city_spending_enricher.enricher import enrich

logging.basicConfig(level=logging.INFO, filename="logs/enrichment.log", filemode="a")

if __name__ == "__main__":
    enrich()
