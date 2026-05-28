from core.persistence.job_store import (
    save_jobs,
    load_jobs
)


class DurableQueue:

    def __init__(self):

        self.jobs = load_jobs()

    def add(self, job):

        self.jobs.append(job)

        save_jobs(self.jobs)

    def remove(self, job):

        self.jobs.remove(job)

        save_jobs(self.jobs)

    def all(self):

        return self.jobs

    def clear(self):

        self.jobs = []

        save_jobs(self.jobs)