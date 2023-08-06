from typing import List

from podder.helpers import client_exception_handler

from .job import Job


class Client():
    @client_exception_handler
    def __init__(self, api_service):
        self.api_service = api_service
        self.api_service.get_user()

    @client_exception_handler
    def start_job(self, file_path: str):
        return Job(self.api_service.create_job(file_path))

    @client_exception_handler
    def start_jobs(self, file_paths: List[str]):
        return [Job(self.api_service.create_job(path)) for path in file_paths]

    @client_exception_handler
    def get_job(self, job_id: str):
        return Job(self.api_service.get_job(job_id))

    @client_exception_handler
    def get_jobs(self, job_ids: List[str], status: str = ''):
        jobs_data = self.api_service.get_jobs(job_ids, status)
        return [Job(data) for data in jobs_data]

    @client_exception_handler
    def download_file(self, file_id: str, local_file_path: str):
        self.api_service.download_file(file_id, local_file_path)
