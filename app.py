from datetime import datetime, timedelta
from redis import Redis
from rq_scheduler import Scheduler
from flask import Flask, json, request, jsonify
from collections import defaultdict
from job import call_endpoint

REDIS_URL = 'redis://localhost:6379'

app = Flask(__name__)
scheduler = Scheduler(connection=Redis())
job_list = defaultdict(str)

@app.route("/add-job/<name>")
def add_job(name):
  if request.args.get('seconds'):
    seconds = int(request.args.get('seconds'), base=10)
  else:
    seconds = 10

  job = scheduler.schedule(
    scheduled_time=datetime.utcnow(),
    func=call_endpoint,
    kwargs={"params": { "name": name }},
    interval=seconds,
    repeat=10
  )
  job_list[f"{job.id}"] = name
  return jsonify({ "status": 200, "message": "success", "job_id": job.id })

@app.route("/list-jobs")
def list_jobs():
  result = []
  jobs = scheduler.get_jobs(with_times=True)
  for job, dt in jobs:
    result.append((job.id, job_list[job.id], dt))
  return jsonify(result)

@app.route("/cancel-job")
def cancel_job():
  job_id = request.args.get('id')
  scheduler.cancel(job_id)
  del job_list[job_id]
  return jsonify({ "status": 200, "message": "success" })
