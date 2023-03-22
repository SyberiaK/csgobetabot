import env

import logging
import time
from datetime import datetime

import config
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from addons import file_manager
from html_telegraph_poster.upload_images import upload_image


def graph_maker():
    while True:
        minutes = datetime.now().minute
        seconds = datetime.now().second
        microseconds = datetime.now().microsecond
        if minutes not in {0, 10, 20, 30, 40, 50}:
            snooze = ((10 - minutes % 10) * 60) - (seconds + microseconds / 1000000.0)
            time.sleep(snooze)
        else:
            try:
                cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
                player_count = cacheFile["online_players"]

                old_player_data = pd.read_csv(
                    config.PLAYER_CHART_FILE_PATH, parse_dates=["DateTime"]
                )

                old_player_data.drop(0, axis=0, inplace=True)

                temp_player_data = pd.DataFrame(
                    [[datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"), player_count]],
                    columns=["DateTime", "Players"],
                )
                temp_player_data["Players"] = temp_player_data["Players"].astype(
                    "int64"
                )

                new_player_data = pd.concat([old_player_data, temp_player_data])

                new_player_data.to_csv(config.PLAYER_CHART_FILE_PATH, index=False)

                player_data = pd.read_csv(
                    config.PLAYER_CHART_FILE_PATH, parse_dates=["DateTime"]
                )

                sns.set_style("whitegrid")

                fig, ax = plt.subplots(figsize=(10, 2.5))
                ax.plot(
                    "DateTime",
                    "Players",
                    data=player_data,
                    color="red",
                    linewidth=0.7,
                    marker="o",
                    markevery=[-1],
                )
                ax.fill_between(
                    player_data["DateTime"],
                    player_data["Players"],
                    0,
                    facecolor="red",
                    color="red",
                    alpha=0.4,
                )

                ax.margins(x=0)
                ax.grid(visible=True, axis="y", linestyle="--", alpha=0.3)
                ax.grid(visible=False, axis="x")
                ax.spines["bottom"].set_position("zero")
                ax.spines["bottom"].set_color("black")
                ax.set_ylabel("")
                ax.set_xlabel("")
                ax.xaxis.set_ticks_position("bottom")
                ax.xaxis.set_major_locator(mdates.DayLocator())
                ax.xaxis.set_major_formatter(mdates.DateFormatter("%d %b"))
                ax.legend(loc="upper left")
                ax.axhline(y=0, color="none")
                ax.axhline(y=1400000, color="none")

                plt.yticks(ticks=[0, 250000, 500000, 750000, 1000000, 1250000])
                plt.subplots_adjust(top=1, bottom=0.077, left=0, right=1)
                plt.text(0.989, 0.058, "0", transform=ax.transAxes, alpha=0.3)
                plt.text(0.965, 0.215, "250k", transform=ax.transAxes, alpha=0.3)
                plt.text(0.965, 0.377, "500k", transform=ax.transAxes, alpha=0.3)
                plt.text(0.965, 0.54, "700k", transform=ax.transAxes, alpha=0.3)
                plt.text(0.951, 0.705, "1 000k", transform=ax.transAxes, alpha=0.3)
                plt.text(0.951, 0.865, "1 250k", transform=ax.transAxes, alpha=0.3)
                plt.text(
                    0.156,
                    0.874,
                    "Made by @csgobeta\nupd every 10 min",
                    ha="center",
                    transform=ax.transAxes,
                    color="black",
                    size="6",
                )
                plt.close()

                fig.savefig(config.GRAPH_IMG_FILE_PATH)
                url = upload_image(config.GRAPH_IMG_FILE_PATH)

                cacheFile = file_manager.readJson(config.CACHE_FILE_PATH)
                if url != cacheFile["graph_url"]:
                    file_manager.updateJson(config.CACHE_FILE_PATH, url, "graph_url")

                time.sleep(120)
            except Exception as e:
                print(f" - Error:\n{e}\n")
                time.sleep(120)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(name)s: %(message)s",
        datefmt="%H:%M:%S — %d/%m/%Y",
    )
    graph_maker()
