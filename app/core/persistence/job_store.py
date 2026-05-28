import json

from pathlib import Path


JOB_FILE = Path("data/jobs.json")


def save_jobs(jobs):

    JOB_FILE.parent.mkdir(
        exist_ok=True
    )

    with open(JOB_FILE, "w") as file:

        json.dump(
            jobs,
            file,
            indent=4
        )


def load_jobs():

    if not JOB_FILE.exists():

        return []

    with open(JOB_FILE, "r") as file:

        return json.load(file)