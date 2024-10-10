from flask import Flask, render_template, jsonify, request, abort
import pandas as pd
import logging
from sqlalchemy import create_engine
import plotly.express as px
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)


app = Flask(__name__)

# Load database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    logging.error("No DATABASE_URL set for PostgreSQL connection")
    raise ValueError("No DATABASE_URL set for PostgreSQL connection")

# Connect to PostgreSQL using SQLAlchemy
try:
    engine = create_engine(DATABASE_URL)
    logging.info("Connected to PostgreSQL successfully")
except Exception as e:
    logging.error(f"Error connecting to PostgreSQL: {e}")
    raise

@app.route('/')
def index():
    try:
        logging.info("Loading data from the database")
        # Load data from the database
        df = pd.read_sql("SELECT * FROM emissions_data", engine)
        logging.info(f"Data loaded: {df.shape} rows, columns: {df.columns.tolist()}")
        
        # Check if the dataframe is empty
        if df.empty:
            logging.warning("No data returned from the database.")
            return render_template('index.html')

        logging.info("Data loaded successfully from the database")

        # Clean up column names
        df.columns = df.columns.str.strip().str.replace(' ', '_')

        # Visualization 1: Global CO2 Emissions Over Time
        years = df.columns[5:]
        global_emissions = df[years].sum()
        logging.info(f"Global emissions data: {global_emissions}")  # Log global emissions
        global_emissions_fig = px.line(
            x=years,
            y=global_emissions,
            labels={'x': 'Year', 'y': 'Global CO2 Emissions (kt)'},
            title='Global CO2 Emissions Over Time'
        )
        logging.info("Global CO2 Emissions visualization created")
        logging.info(global_emissions_fig.to_json())  # Log the figure JSON

        # Visualization 2: CO2 Emissions by Country (2020)
        df_2020 = df[['country_name', '2020']]
        logging.info(f"2020 emissions data: {df_2020.head()}")  # Log a sample of the data
        country_emissions_fig = px.choropleth(
            df_2020,
            locations='country_name',
            locationmode='country names',
            color='2020',
            hover_name='country_name',
            title='CO2 Emissions by Country (2020)',
            color_continuous_scale=px.colors.sequential.Plasma
        )
        logging.info("CO2 Emissions by Country visualization created")
        logging.info(country_emissions_fig.to_json())  # Log the figure JSON

        # Visualization 3: Top 10 CO2 Emitting Countries
        top_emitters = df[['country_name', '2020']].sort_values(by='2020', ascending=False).head(10)
        logging.info(f"Top 10 CO2 emitters: {top_emitters}")  # Log top 10 emitters
        top_emitters_fig = px.bar(
            top_emitters,
            x='country_name',
            y='2020',
            title='Top 10 CO2 Emitting Countries (2020)',
            labels={'2020': 'CO2 Emissions (kt)', 'country_name': 'Country'}
        )
        logging.info("Top 10 CO2 Emitting Countries visualization created")
        logging.info(top_emitters_fig.to_json())  # Log the figure JSON

        # Visualization 4: CO2 Emissions Over Time for Selected Countries
        selected_countries = ['United States', 'China', 'India', 'Russia', 'Germany']
        df_selected = df[df['country_name'].isin(selected_countries)]
        logging.info(f"Data for selected countries: {df_selected.head()}")  # Log a sample
        df_selected = df_selected.melt(id_vars=['country_name'], value_vars=years, var_name='Year', value_name='CO2 Emissions (kt)')
        selected_countries_fig = px.line(
            df_selected,
            x='Year',
            y='CO2 Emissions (kt)',
            color='country_name',
            title='CO2 Emissions Over Time for Selected Countries'
        )
        logging.info("CO2 Emissions Over Time for Selected Countries visualization created")
        logging.info(selected_countries_fig.to_json())  # Log the figure JSON

        # Visualization 5: CO2 Emissions vs Population (if population data is available)
        if 'population' in df.columns:
            logging.info(f"Population data exists, creating scatter plot.")
            emissions_vs_population_fig = px.scatter(
                df,
                x='population',
                y='2020',
                size='2020',
                hover_name='country_name',
                title='CO2 Emissions vs Population (2020)',
                labels={'2020': 'CO2 Emissions (kt)', 'population': 'Population'}
            )
            logging.info("CO2 Emissions vs Population visualization created")
            logging.info(emissions_vs_population_fig.to_json())  # Log the figure JSON
        else:
            emissions_vs_population_fig = None
            logging.warning("Population data not available for CO2 Emissions vs Population visualization")

        # Render all visualizations on the main page
        logging.info("Rendering visualizations on index.html")
        return render_template(
            'index.html',
            global_emissions_data=global_emissions_fig.to_json(),
            country_emissions_data=country_emissions_fig.to_json(),
            top_emitters_data=top_emitters_fig.to_json(),
            selected_countries_data=selected_countries_fig.to_json(),
            emissions_vs_population_data=emissions_vs_population_fig.to_json() if emissions_vs_population_fig else ''
        )

    except Exception as e:
        logging.error(f"An error occurred during index processing: {str(e)}")
        return jsonify({'error': f"An error occurred: {str(e)}"}), 500

