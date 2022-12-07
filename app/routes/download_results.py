import json
from flask import *
from .classifications_id import *

config = Configuration()


@app.route("/download_results", methods=['GET', 'POST'])
def download_results():
    """API for returning a JSON file with the results."""
    if request.method == 'POST':
        jobId = request.form.get('jobid')
        jsonFIle_raw = classifications_id(jobId)

        return Response(json.dumps(jsonFIle_raw["data"], indent=4),
                        mimetype="text/json",
                        headers={"Content-disposition":
                                     "attachment; filename={}.json".format(jobId)})

    elif request.method == 'GET':
        return
