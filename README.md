# Higher Education Flow Indicators in Brazil

This project aims to analyze the flow indicators of higher education in Brazil using data from INEP. The project includes scripts to download, process, and visualize the data.

## Scope of Analysis

The analysis focuses on tracking higher education entrants from the year 2014 over 10 years, until 2023. The data includes information on retention rates, completion rates, dropout rates, and other relevant indicators to understand the flow of students in Brazilian higher education.

The data is public and available on the INEP website: https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/indicadores-educacionais/indicadores-de-fluxo-da-educacao-superior

## Streamlit Application

If you do not want to run the project locally on your machine, you can access the Streamlit application and interact with it, making your own analyses through the link below:

https://indicadores-fluxo-educacao-superior-brasil.streamlit.app/

## Project Structure

- `app/`
  - `streamlit_dashboard.py`: Data visualization interface using Streamlit.
  - `data_loader.py`: Loads and maps the data for better understanding.
- `assets/`
  - `inep.png`: Image used in the Streamlit application.
- `data/`
  - `raw/`: Contains the downloaded raw data.
  - `processed/`: Contains the processed data ready for analysis.
  - `database.db`: Database created in SQLite for analyses and processing.
- `scripts/`
  - `db_manager.py`: Manages the connection and operations with the SQLite database.
  - `data_processor.py`: Processes the raw data and saves it to the database.
  - `data_downloader.py`: Downloads and extracts data from INEP.
- `main.py`: Main script to execute the complete flow of downloading, processing, and storing the data.

# Project Notes

The idea of building a database in SQLite is to analyze possible trends in the data and apply machine learning algorithms in the future. This will allow for deeper and more efficient analysis, as well as the creation of predictive models based on higher education flow indicators.

Additionally, building the database in SQLite allows us to run the Streamlit app in the cloud without needing to consume a heavy local file.

## Requirements

- Python 3.8+
- Python Libraries:
  - `pandas`
  - `sqlalchemy`
  - `requests`
  - `zipfile`
  - `streamlit`
  - `plotly`
  - `openpyxl`

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/LeviJesus/indicadores_fluxo_educacao_superior_brasil.git
   cd indicadores-fluxo-educacao-superior-brasil
   ```

2. Create a virtual environment and install the dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

## Usage

1. Run the main script to download, process, and store the data:
   ```bash
   python main.py
   ```

2. Start the Streamlit dashboard to visualize the data:
   ```bash
   streamlit run app/streamlit_dashboard.py
   ```

## Contribution

Contributions are welcome! Feel free to open issues and pull requests.
