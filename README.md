# Trip Planner

`Trip_Planner` is a small AI-powered travel planning project. It takes a free-form trip request, figures out the destination, pulls city and sightseeing details from Wikivoyage, checks hotel options through RapidAPI, and generates a city-wise trip summary.

## What It Does

- takes trip details and an arrival date from the terminal
- extracts the destination using a Groq LLM
- scrapes top cities and places to visit from Wikivoyage
- ranks the most relevant cities based on the user's travel intent
- fetches hotel options for those cities
- writes the final travel plan to a text file

## How It Works

The project follows a simple pipeline:

1. `src/main.py` collects the user input and runs the full flow.
2. `src/agents.py` handles LLM-based tasks like destination extraction, city ranking, hotel selection, and final summarization.
3. `src/web_scrapper.py` scrapes cities and attractions from Wikivoyage.
4. `src/api_caller.py` fetches hotel data using Booking.com RapidAPI endpoints.
5. `src/utilis/city_selector.py` matches the LLM output with scraped city data.

## Project Structure

```text
Trip_Planner/
├── README.md
├── .gitignore
├── src/
│   ├── main.py
│   ├── agents.py
│   ├── api_caller.py
│   ├── web_scrapper.py
│   └── utilis/
│       └── city_selector.py
└── tests/
    └── Trip_to_India.txt
```

## Setup

Create a virtual environment, install the required packages, and add your API keys in a `.env` file.

```bash
python -m venv .venv
source .venv/bin/activate
pip install groq python-dotenv requests beautifulsoup4
```

`.env`

```env
GROQ_API_KEY=your_groq_api_key
RAPID_API_KEY=your_rapidapi_key
```

## Run

Run the project from inside the `src` folder:

```bash
cd src
python main.py
```

Example input:

```text
Enter your trip information:- Plan a budget-friendly cultural trip to India
Enter arrival date:- 2025-08-15
```

The generated output is saved as:

```text
tests/Trip_to_<Country>.txt
```
