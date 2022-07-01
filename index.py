from flask import Flask, request, abort
from flask import jsonify
from rq import Queue
from rq.job import Job
from worker import conn
from main import output_news


app = Flask(__name__)

q = Queue(connection=conn)


@app.errorhandler(404)
def resource_not_found(exception):
    """Returns exceptions as part of a json."""
    return jsonify(error=str(exception)), 404


@app.route("/")
def home():
    """Show the app is working."""
    return "Running!"


@app.route("/enqueue/", methods=["GET"])
def enqueue():
    """Enqueues a task into redis queue to be processes.
    Returns the job_id."""

    ## Args
    keywords = request.args.getlist('keywords')
    timeframe = request.args.get('timeframe', type=str)
    translate_title = request.args.get('translate_title', default=True, type=lambda v: v.lower() == 'true')
    translate_search = request.args.get('translate_search', default=False, type=lambda v: v.lower() == 'true')

    ## Kwargs
    # lists: we check if they are empty, if they are we return none
    labels = request.args.getlist('labels')

    if labels:
        pass
    else:
        labels = None

    languages = request.args.getlist('languages')

    if languages:
         pass
    else:
        languages = None

    countries = request.args.getlist('countries')

    if countries:
        pass
    else:
        countries = None

    # int
    limit = request.args.get('limit', default=None, type=int)

    # bool
    rank = request.args.get('rank', default=False, type=lambda v: v.lower() == 'true')
    ner = request.args.get('ner', default=False, type=lambda v: v.lower() == 'true')
    weak = request.args.get('weak', default=True, type=lambda v: v.lower() == 'true')

    job = q.enqueue_call(output_news,
                              args=(keywords,
                                    timeframe,
                                    translate_title,
                                    translate_search),
                              kwargs={
                                  "weak": weak,
                                  "labels": labels,
                                  "languages": languages,
                                  "countries": countries,
                                  "limit": limit,
                                  "rank": rank,
                                  "ner": ner
                              },
                              timeout=3600)

    return jsonify({"job_id": job.id})


@app.route("/check_status")
def check_status():
    """Takes a job_id and checks its status in redis queue."""
    job_id = request.args["job_id"]

    try:
        job = Job.fetch(job_id, connection=conn)
    except Exception as exception:
        abort(404, description=exception)

    return jsonify({"job_id": job.id, "job_status": job.get_status()})


@app.route("/get_result")
def get_result():
    """Takes a job_id and returns the job's result."""
    job_id = request.args["job_id"]

    try:
        job = Job.fetch(job_id, connection=conn)
    except Exception as exception:
        abort(404, description=exception)

    if not job.result:
        abort(
            404,
            description=f"No result found for job_id {job.id}. Try checking the job's status.",
        )
    return jsonify(job.result)



if __name__ == '__main__':
    app.run(threaded=True, debug=False)

