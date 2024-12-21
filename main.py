import taipy as tp
import taipy.gui.builder as tgb
from taipy.gui import Icon
from taipy import Config
import datetime
import pandas as pd
import plotly.graph_objects as go

stock_data = pd.read_csv("data/sp500_stocks.csv")
company_data = pd.read_csv("data/sp500_companies.csv")
country_names = company_data["Country"].unique().tolist()
country_names = [(name, Icon("images/flags/" + name + ".png", name))
                 for name in country_names]
company_names = company_data[
                    ["Symbol", "Shortname"]
                ].sort_values("Shortname").values.tolist()

dates = [
    stock_data["Date"].min(),
    stock_data["Date"].max()
]

country = "Canada"
company = ["LULU"]

lin_pred = 0
knn_pred = 0
rnn_pred = 0

graph_data = None
figure = None

# create page
with tgb.Page() as page:
    with tgb.part("text-center"):
        tgb.image("images/icons/logo.png", width="10vw")
        tgb.text("Stocker", mode="md")
        tgb.date_range(
            "{dates}",
            label_start="Start Date",
            label_end="End Date"
        )

        with tgb.layout("20 80"):
            tgb.selector(
                label="country",
                class_name="fullwidth",
                value="{country}",
                lov="{country_names}",
                dropdown=True,
                value_by_id=True
            )
            tgb.selector(
                label="company",
                class_name="fullwidth",
                value="{company}",
                lov="{company_names}",
                dropdown=True,
                value_by_id=True,
                multiple=True
            )

        tgb.chart(figure="{figure}")
        with tgb.part("text-left"):
            with tgb.layout("4 72 4 4 4 4 4 4"):
                tgb.image(
                    "images/icons/id-card.png",
                    width="3vw")
                tgb.text("{company[-1]}")
                tgb.image(
                    "images/icons/lin.png",
                    width="3vw")
                tgb.text("{lin_pred}")
                tgb.image(
                    "images/icons/knn.png",
                    width="3vw")
                tgb.text("{knn_pred}")

                tgb.image(
                    "images/icons/rnn.png",
                    width="3vw")
                tgb.text("{rnn_pred}")


def build_company_names(country):
    comp_names = company_data[
        ["Symbol", "Shortname"]][
            company_data["Country"] == country
        ].sort_values("Shortname").values.tolist()
    return comp_names


def build_graph_data(dates, company):
    tmp_data = stock_data[["Date", "Adj Close", "Symbol"]][
        # (stock_data["Symbol"] == company) &
        (stock_data["Date"] > str(dates[0])) &
        (stock_data["Date"] < str(dates[1]))  # сравнивать строки?
    ]
    gr_data = pd.DataFrame()
    gr_data["Date"] = tmp_data["Date"].unique()

    for c in company:
        gr_data[c] = tmp_data["Adj Close"][
            tmp_data["Symbol"] == c
        ].values

    # gr_data = gr_data.rename(columns={"Adj Close": company})
    return gr_data


def display_graph(gr_data):
    fig = go.Figure()
    symbols = gr_data.columns[1:]

    for s in symbols:
        fig.add_trace(go.Scatter(
            x=gr_data["Date"],
            # y=gr_data[gr_data.columns[-1]],
            y=gr_data[s],
            # name=gr_data.columns[-1],
            name=s,
            showlegend=True
            ))
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Stock Value"
    )
    return fig


country_cfg = Config.configure_data_node(
    id="country")
company_names_cfg = Config.configure_data_node(
    id="company_names")
dates_cfg = Config.configure_data_node(
    id="dates")
company_cfg = Config.configure_data_node(
    id="company")
graph_data_cfg = Config.configure_data_node(
    id="graph_data")

build_graph_data_cfg = Config.configure_task(
    input=[dates_cfg, company_cfg],
    output=graph_data_cfg,
    function=build_graph_data,
    id="build_graph_data",
    skippable=True)

build_company_names_cfg = Config.configure_task(
    input=country_cfg,
    output=company_names_cfg,
    function=build_company_names,
    id="build_company_names",
    skippable=True)

scenario_cfg = Config.configure_scenario(
    task_configs=[build_company_names_cfg, build_graph_data_cfg],
    id="scenario")


def on_change(state, name, value):
    if name == "country":
        print(name, value)
        state.scenario.country.write(state.country)
        state.scenario.submit(wait=True)
        state.company_names = state.scenario.company_names.read()
    if name == "company" or name == "dates":
        print(name, value)
        state.scenario.dates.write(state.dates)
        state.scenario.company.write(state.company)
        state.scenario.submit(wait=True)
        state.graph_data = state.scenario.graph_data.read()
    if name == "graph_data":
        state.figure = display_graph(state.graph_data)


if __name__ == "__main__":
    tp.Orchestrator().run()
    scenario = tp.create_scenario(scenario_cfg)
    gui = tp.Gui(page)
    gui.run(title = "Data Sceince Dashboard",
            use_reloader=True)
