import taipy as tp
import taipy.gui.builder as tgb
from taipy.gui import Icon
from taipy import Config

# create page
with tgb.Page() as page:
    with tgb.part("text-center"):
        tgb.image("images/icons/logo.png", width="10vw")
        tgb.text(
            "Stocker",
            mode="md"
        )

if __name__ == "__main__":
    gui = tp.Gui(page)
    gui.run(title = "Data Sceince Dashboard")
