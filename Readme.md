# City Expenses Enricher

This project reads a CSV file of expenses and enriches each row with:
- Latitude & Longitude
- Current Weather (temperature & wind speed)
- FX rate conversion to USD

The enriched data is saved as a JSON file. Logs are stored in the logs/ folder.

Setup:

git clone https://github.com/YourUsername/City-Spending-Enricher.git
cd City-Spending-Enricher
python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate # macOS/Linux
pip install -r requirements.txt

Example Input (expenses.csv):

city,country_code,local_currency,amount
Berlin,DE,EUR,89.9
Paris,FR,EUR,120.5
Tokyo,JP,JPY,10500
New York,US,USD,89.9

.env format:

GEOCODE_URL=***********
WEATHER_URL=********
FX_URL=*******
TIMEOUT=10
INPUT_CSV=input_file.csv
OUTPUT_JSON=output_file.json

Run Command:

python -m city_spending_enricher.main

Output:

- Enriched data will be saved to the JSON file specified in OUTPUT_JSON
- Logs will be saved to logs/enrichment.log