import os

import matplotlib.pyplot as plt
from flask import *

from .classifications_id import *

config = Configuration()

SAVEPRIV = 'app/static/plots'

app.config['SAVEPRIV'] = SAVEPRIV


@app.route("/download_plot", methods=['GET', 'POST'])
def download_plot():
    """API for returning the plot as an image."""
    if request.method == 'POST':
        jobId = request.form.get('jobid')
        jsonFIle = classifications_id(jobId)

        data = jsonFIle["data"]

        names = []
        values = []

        for i in data:
            a = i[0]
            b = i[1]
            names.append(a)
            values.append(b)

        plt.figure(figsize=(10, 5))
        plt.bar(names, values, color=['red', 'beige', 'orange', 'green', 'yellow'],
                width=0.4)

        plt.xlabel("Classes")
        plt.ylabel("Percentage")
        plt.title("Results of classification")

        filename = str(jobId) + ".png"

        plt.savefig(os.path.join(app.config['SAVEPRIV'], filename))

        stripped = os.path.relpath(app.config['SAVEPRIV'], "app/")

        print("{}".format(stripped))

        return send_from_directory(stripped, filename, as_attachment=True)

    elif request.method == 'GET':
        return
