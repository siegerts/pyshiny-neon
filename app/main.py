from shiny import App, reactive, render, ui
import seaborn as sns

from app import settings

import pandas as pd
import sqlalchemy
from sqlalchemy.exc import PendingRollbackError, OperationalError, ResourceClosedError

engine = sqlalchemy.create_engine(str(settings.DATABASE_URL), pool_pre_ping=True)

app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.h2("pyShiny + Neon 🚀"),
        ui.p("Select the number of rows from the Netflix dataset."),
        ui.input_slider("slider", "Number of rows to return", 0, 100, 50),
        ui.input_slider("n", "Number of bins", 1, 20, 10),
        ui.div(
         ui.input_action_button("action_button", "Search"),
        ),
    ),
    ui.div(
        ui.output_plot("plot"),
    ),
    ui.output_data_frame("get_df"), 
)



def server(input, output, session):
    app.starlette_app.conn = engine.connect()
    app.starlette_app.shows_df = None
   

    def cleanup():
        app.starlette_app.conn.close()
   
    
    session.on_ended(cleanup)

    @reactive.Calc
    def query_db():
        print("Querying db...")
        df = pd.read_sql(f"SELECT * FROM netflix_shows limit {input.slider()}", app.starlette_app.conn)
        app.starlette_app.shows_df = df
        return df


    
    @output
    @render.plot(alt="Chart of year released and number of shows") 
    @reactive.event(input.action_button, input.slider, input.n)
    def plot():
        if app.starlette_app.shows_df is None:
            query_db()

        shows_df = app.starlette_app.shows_df
        fig = sns.histplot(shows_df.release_year, bins=input.n())
        fig.set_title("Number of Netflix shows released by year")
        fig.set_xlabel("Year")
        fig.set_ylabel("Number of shows")
        fig.set_xticklabels(fig.get_xticklabels(), rotation=45)
        return fig


    @render.data_frame
    @reactive.event(input.action_button)
    def get_df():
        try:
            df = query_db()
        except PendingRollbackError:
            print("Rolling back...")
            app.starlette_app.conn.rollback()
            query_db()
        except (OperationalError, ResourceClosedError):
            print("Reconnecting...")
            app.starlette_app.conn.close()
            app.starlette_app.conn = engine.connect()
            df = query_db()
        return df

    


app = App(app_ui, server)



   






