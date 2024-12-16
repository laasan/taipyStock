import taipy as tp
import taipy.gui.builder as tgb
from taipy.gui import Icon
from taipy import Config
import datetime
import pandas as pd

stock_data = pd.read_csv("data/sp500_stocks.csv")
company_data = pd.read_csv("data/sp500_companies.csv")
country_names = company_data["Country"].unique().tolist()
company_names = company_data[
                    ["Symbol", "Shortname"]
                ].sort_values("Shortname").values.tolist()

dates = [
    datetime.date(2023, 1, 1),
    datetime.date(2024, 1, 1)
]

country = "Canada"
company = "LULU"

lin_pred = 0
knn_pred = 0
rnn_pred = 0

# create page
with tgb.Page() as page:
    with tgb.part("text-center"):
        tgb.image("images/icons/logo.png", width="10vw")
        tgb.text(
            "Stocker",
            mode="md"
        )
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
                dropdown=True
            )
            tgb.selector(
                label="company",
                class_name="fullwidth",
                value="{company}",
                lov="{company_names}",
                dropdown=True
            )

        tgb.chart()
        with tgb.part("text-left"):
            with tgb.layout("4 72 4 4 4 4 4 4"):
                tgb.image(
                    "images/icons/id-card.png",
                    width="3vw"
                )
                tgb.text(f"{company}", mode="md")

                tgb.image(
                    "images/icons/lin.png",
                    width="3vw"
                )
                tgb.text(f"{lin_pred}", mode="md")

                tgb.image(
                    "images/icons/knn.png",
                    width="3vw"
                )
                tgb.text(f"{knn_pred}", mode="md")

                tgb.image(
                    "images/icons/rnn.png",
                    width="3vw"
                )
                tgb.text(f"{rnn_pred}", mode="md")

if __name__ == "__main__":
    gui = tp.Gui(page)
    gui.run(title = "Data Sceince Dashboard",
            use_reloader=True)
