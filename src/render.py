import json
import altair as alt
import pandas as pd
import matplotlib.pyplot as plt
from bokeh.plotting import figure, show
from bokeh.io import output_file
from bokeh.models import ColumnDataSource


def bokeh_visualise(data, target_filepath="court_cases.html"):
    """
    generates a HTML bar chart from the provided json data representing court cases
    """
    case_numbers = []
    paragraph_counts = []
    for case in data:
        for case_number, details in case.items():
            case_numbers.append(case_number)
            paragraph_counts.append(details["paragaph_count"])
    source = ColumnDataSource(
        data=dict(case_numbers=case_numbers, paragraph_counts=paragraph_counts)
    )
    output_file(target_filepath)
    p = figure(
        x_range=case_numbers,
        title="Paragraph Count by Court Case",
        toolbar_location=None,
        tools="",
    )
    p.vbar(x="case_numbers", top="paragraph_counts", width=0.9, source=source)
    p.xgrid.grid_line_color = None
    p.y_range.start = 0
    p.yaxis.axis_label = "Paragraph Count"
    p.xaxis.axis_label = "Court Case"
    p.xaxis.major_label_orientation = 45
    show(p)


def pychart_visualise(target_filepath):
    """
    reads a JSON and renders a pychart with pychart
    """
    try:
        with open(target_filepath, "r") as file:
            data = json.load(file)
        cases = []
        counts = []
        for case in data:
            for key, value in case.items():
                cases.append(key)
                counts.append(value["paragraph_count"])
        plt.figure(figsize=(10, 6))
        plt.bar(cases, counts, color="skyblue")
        plt.xlabel("Court Cases")
        plt.ylabel("Paragraph Count")
        plt.title("Paragraph Counts in Court Cases for 2024")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.show()
    except FileNotFoundError:
        print(f"Error: The file at filepath {target_filepath} was not found.")
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON. Please check the file format.")
    except Exception as e:
        print(f"Error: An unexpected error occurred: {e}")


def altair_visualise(target_filepath, output_filepath="court_cases.html"):
    """
    renders an altair chart from the provided JSON file
    """
    with open(target_filepath, "r") as file:
        data = json.load(file)["log_data"]
    cases = [{"name": key, "count": data[key]["paragaph_count"]} for key in data]
    df = pd.DataFrame(cases)
    chart = (
        alt.Chart(df)
        .mark_bar()
        .encode(x="name:O", y="count:Q", tooltip=["name", "count"])
        .properties(title="Paragraph Counts in Court Cases")
        .interactive()
    )
    chart.save(output_filepath)
    chart.show()
