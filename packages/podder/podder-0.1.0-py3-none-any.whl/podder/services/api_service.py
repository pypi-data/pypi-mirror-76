import json
import os
from typing import List

import requests

from podder.exceptions import *


class APIService():
    CHUNK_SIZE = 1_048_576 # 1 MB (1024 * 1024)

    def __init__(self, domain, access_token):
        self.domain = domain
        self.access_token = access_token
        self.headers = {"Authorization": f"Bearer {access_token}"}

    def get_user(self):
        url = self.domain + "/api/user/me"
        res = requests.get(url, headers=self.headers)
        if res.status_code == 400:
            raise AuthorizationException(
                'Authorization failed. Please check your access token.')
        elif not res.ok:
            raise PodderApiException(
                f"Failed to get user. Response: {res.text}, URL: {url}")

        return json.loads(res.text)

    def create_job(self, file_path: str):
        url = self.domain + '/api/jobs'
        with open(file_path, mode='rb') as fp:
            file_data = fp.read()

        files = {'file[]': (os.path.basename(file_path), file_data)}
        res = requests.post(url, files=files, headers=self.headers)
        if not res.ok:
            raise PodderApiException(
                f"Failed to create a job. Response: {res.text}, URL: {url}")

        return json.loads(res.text)

    def get_job(self, job_id: str):
        url = f'{self.domain}/api/jobs/{job_id}'
        res = requests.get(url, headers=self.headers)
        if not res.ok:
            raise PodderApiException(
                f"Failed to get job. Response: {res.text}, URL: {url}")

        return json.loads(res.text)

    def get_jobs(self, job_ids: List[str], status: str = ''):
        jobs_data = []
        for job_id in job_ids:
            url = f'{self.domain}/api/jobs/{job_id}'
            res = requests.get(url, headers=self.headers)
            if not res.ok:
                raise PodderApiException(
                    f"Failed to get jobs. Response: {res.text}, URL: {url}")

            job_data = json.loads(res.text)
            if status == '' or job_data['status'] == status:
                jobs_data.append(job_data)

        return jobs_data

    def download_file(self, file_id: str, local_file_path: str):
        url = f'{self.domain}/api/job_files/{file_id}/data'
        res = requests.get(url, headers=self.headers)
        if not res.ok:
            raise PodderApiException(
                f"Failed to get file data. Response: {res.text}, URL: {url}")

        with open(local_file_path, 'wb') as fd:
            for chunk in res.iter_content(chunk_size=self.CHUNK_SIZE):
                fd.write(chunk)
