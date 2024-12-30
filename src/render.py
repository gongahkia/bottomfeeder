from bokeh.plotting import figure, show
from bokeh.io import output_file
from bokeh.models import ColumnDataSource


def bokeh_visualise(data, target_filepath):
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
