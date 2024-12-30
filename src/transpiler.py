import json
import h5py
import pickle
import sqlite3
import xmltodict
import pandas as pd


def generate_latex(data, target_filepath):
    """
    generates a latex document from the provided json data
    """
    latex_document = r"""
\documentclass{article}
\usepackage{booktabs}
\begin{document}

\title{Court Cases Report}
\author{Generated from JSON Data}
\date{\today}
\maketitle

\section{Case Summary}

\begin{table}[h]
    \centering
    \begin{tabular}{@{}lllcc@{}}
        \toprule
        Case Number & Coram & Year & Court & Paragraph Count \\ \midrule
"""
    for case in data:
        for case_number, details in case.items():
            coram = ", ".join(details["coram"]) if details["coram"] else "N/A"
            year = details["year"]
            court = details["court"]
            paragraph_count = details["paragaph_count"]
            latex_document += f"        {case_number} & {coram} & {year} & {court} & {paragraph_count} \\\\ \n"
    latex_document += r"""
    \bottomrule
    \end{tabular}
    \caption{Summary of Court Cases}
\end{table}

\end{document}
"""
    with open(target_filepath, "w") as f:
        f.write(latex_document)
    print(f"Success: LaTeX document generated as {target_filepath}")


def generate_csv(data, target_filepath):
    """
    converts json data to a csv file
    """
    data_list = []
    for case in data:
        for case_number, details in case.items():
            data_list.append(
                {
                    "case_number": case_number,
                    "coram": ", ".join(details["coram"]),
                    "year": details["year"],
                    "court": details["court"],
                    "paragraph_count": details["paragaph_count"],
                }
            )
    df = pd.DataFrame(data_list)
    df.to_csv(target_filepath, index=False)
    print(f"Success: CSV file generated at the filepath {target_filepath}")


def generate_xml(data, target_filepath):
    """
    converts JSON data to XML format
    """
    xml_data = xmltodict.unparse({"root": data}, pretty=True)
    with open(target_filepath, "w") as xml_file:
        xml_file.write(xml_data)
    print(f"XML file generated: {target_filepath}")


def generate_hdf5(data, target_filepath):
    """
    converts JSON data to HDF5 format
    """
    with h5py.File(target_filepath, "w") as hdf:

        def add_data(name, obj):
            if isinstance(obj, dict):
                group = hdf.create_group(name)
                for key, value in obj.items():
                    add_data(f"{name}/{key}", value)
            else:
                hdf.create_dataset(name, data=obj)

        add_data("root", data)
    print(f"Success: HDF5 file generated: {target_filepath}")


def generate_pickle(data, target_filepath):
    """
    converts JSON data to Pickle format
    """
    with open(target_filepath, "wb") as pickle_file:
        pickle.dump(data, pickle_file)
    print(f"Success: Pickle file generated: {target_filepath}")


def generate_sql(data, target_db_name):
    """
    converts JSON data to SQL format
    """
    conn = sqlite3.connect(target_db_name)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS court_cases (
            case_number TEXT PRIMARY KEY,
            coram TEXT,
            year INTEGER,
            court TEXT,
            paragraph_count INTEGER
        )
    """
    )
    for case in data:
        for case_number, details in case.items():
            cursor.execute(
                """
                INSERT OR REPLACE INTO court_cases (case_number, coram, year, court, paragraph_count)
                VALUES (?, ?, ?, ?, ?)
            """,
                (
                    case_number,
                    ", ".join(details["coram"]),
                    details["year"],
                    details["court"],
                    details["paragaph_count"],
                ),
            )
    conn.commit()
    conn.close()
    print(f"Success: SQL database generated: {target_db_name}")


def generate_d3(target_filepath, output_file="index.html"):
    """
    generates a HTML file that uses a d3.js bar chart based on the specified json
    """
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>D3 Bar Chart</title>
    <script src="https://d3js.org/d3.v7.min.js"></script>
</head>
<body>
    <svg width="800" height="400"></svg>
    <script>
        async function renderD3Chart(jsonFile) {{
            const data = await d3.json(jsonFile);
            const cases = Object.keys(data).map(key => {{
                return {{
                    name: key,
                    count: data[key].paragraph_count
                }};
            }});

            const svg = d3.select("svg");
            const margin = {{ top: 20, right: 30, bottom: 40, left: 40 }};
            const width = +svg.attr("width") - margin.left - margin.right;
            const height = +svg.attr("height") - margin.top - margin.bottom;

            const x = d3.scaleBand()
                .domain(cases.map(d => d.name))
                .range([0, width])
                .padding(0.1);

            const y = d3.scaleLinear()
                .domain([0, d3.max(cases, d => d.count)])
                .nice()
                .range([height, 0]);

            const g = svg.append("g")
                .attr("transform", `translate(${{margin.left}},${{margin.top}})`);

            g.append("g")
                .selectAll(".bar")
                .data(cases)
                .enter().append("rect")
                .attr("class", "bar")
                .attr("x", d => x(d.name))
                .attr("y", d => y(d.count))
                .attr("width", x.bandwidth())
                .attr("height", d => height - y(d.count));

            g.append("g")
                .attr("class", "axis axis--x")
                .attr("transform", `translate(0,${{height}})`)
                .call(d3.axisBottom(x));

            g.append("g")
                .attr("class", "axis axis--y")
                .call(d3.axisLeft(y));
        }}
        renderD3Chart('{target_filepath}');
    </script>
</body>
</html>
"""
    with open(output_file, "w") as out_file:
        out_file.write(html_content)
