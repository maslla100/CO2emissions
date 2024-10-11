from flask import Blueprint, render_template, jsonify
import pandas as pd
import logging
from sqlalchemy import create_engine
import plotly.express as px
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Create a blueprint for routes
routes_bp = Blueprint('routes_bp', __name__)

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

@routes_bp.route('/')
def index():
    try:
        logging.info("Loading data from the database")
        df = pd.read_sql("SELECT * FROM emissions_data", engine)
        logging.info(f"Data loaded: {df.shape} rows, columns: {df.columns.tolist()}")
        
        if df.empty:
            logging.warning("No data returned from the database.")
            return render_template('index.html')

        logging.info("Data loaded successfully from the database")
        df.columns = df.columns.str.strip().str.replace(' ', '_')

        # Visualization 1: Global CO2 Emissions Over Time
        years = df.columns[5:]
        global_emissions = df[years].sum()
        global_emissions_fig = px.line(
            x=years,
            y=global_emissions,
            labels={'x': 'Year', 'y': 'Global CO2 Emissions (kt)'},
            title='Global CO2 Emissions Over Time'
        )

        # Visualization 2: CO2 Emissions by Country (2020)
        df_2020 = df[['country_name', '2020']].dropna()
        country_emissions_fig = px.choropleth(
            df_2020,
            locations='country_name',
            locationmode='country names',
            color='2020',
            hover_name='country_name',
            title='CO2 Emissions by Country (2020)',
            color_continuous_scale=px.colors.sequential.Plasma
        )

        # Visualization 3: Top 10 CO2 Emitting Countries
        top_emitters = df[['country_name', '2020']].sort_values(by='2020', ascending=False).head(10)
        top_emitters_fig = px.bar(
            top_emitters,
            x='country_name',
            y='2020',
            title='Top 10 CO2 Emitting Countries (2020)',
            labels={'2020': 'CO2 Emissions (kt)', 'country_name': 'Country'}
        )

        # Visualization 4: CO2 Emissions Over Time for Selected Countries
        selected_countries = ['United States', 'China', 'India', 'Russia', 'Germany']
        df_selected = df[df['country_name'].isin(selected_countries)]
        df_selected = df_selected.melt(id_vars=['country_name'], value_vars=years, var_name='Year', value_name='CO2 Emissions (kt)')
        selected_countries_fig = px.line(
            df_selected,
            x='Year',
            y='CO2 Emissions (kt)',
            color='country_name',
            title='CO2 Emissions Over Time for Selected Countries'
        )

        # Debug logging: Output the JSON data for visualizations
        logging.debug(f"Global emissions JSON: {global_emissions_fig.to_json()}")
        logging.debug(f"Country emissions JSON: {country_emissions_fig.to_json()}")
        logging.debug(f"Top emitters JSON: {top_emitters_fig.to_json()}")
        logging.debug(f"Selected countries JSON: {selected_countries_fig.to_json()}")

        # Return rendered template
        return render_template(
            'index.html',
            global_emissions_data=global_emissions_fig.to_json() if global_emissions_fig else None,
            country_emissions_data=country_emissions_fig.to_json() if country_emissions_fig else None,
            top_emitters_data=top_emitters_fig.to_json() if top_emitters_fig else None,
            selected_countries_data=selected_countries_fig.to_json() if selected_countries_fig else None,
        )

    except Exception as e:
        logging.error(f"An error occurred during index processing: {str(e)}")
        return jsonify({'error': f"An error occurred: {str(e)}"}), 500

