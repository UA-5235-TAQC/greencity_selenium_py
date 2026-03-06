import json
import mimetypes
import os
from dataclasses import asdict
from typing import Optional, List

import allure
import requests
from requests import Response

from models.update_eco_news_request import UpdateEcoNewsRequest


class BaseClient:
    """Base API client similar to Java RestAssured implementation."""

    def __init__(self, base_api_url: str, access_token: Optional[str] = None):
        self.base_api_url = base_api_url
        self.access_token = access_token
        self.content_type = "application/json"

    def prepare_request(self, headers: Optional[dict] = None) -> dict:
        """ Prepare request headers. """
        request_headers = {
            "Accept": "*/*",
        }

        if self.content_type:
            request_headers["Content-Type"] = self.content_type

        if self.access_token:
            request_headers["Authorization"] = f"Bearer {self.access_token}"

        if headers:
            request_headers.update(headers)
            if request_headers.get("Content-Type") is None:
                request_headers.pop("Content-Type")

        return request_headers

    def prepare_multipart_request(self, update_request: UpdateEcoNewsRequest) -> dict:
        """ Prepare multipart request with EcoNews DTO. """
        dto_json = json.dumps(asdict(update_request), ensure_ascii=False)
        files = {
            "updateEcoNewsDto": ("updateEcoNewsDto", dto_json, "application/json")
        }
        return files

    def get(self, path: str, params: Optional[dict] = None, headers: Optional[dict] = None) -> Response:
        """Execute GET request."""
        request_headers = self.prepare_request(headers)
        url = f"{self.base_api_url}{path}"
        with allure.step(f"Execute GET request to {url} with params {params} and headers {request_headers}"):
            return requests.get(
                url,
                headers=request_headers,
                params=params
            )

    def post(self, path: str, json: Optional[dict] = None, data: Optional[dict] = None,
            files: Optional[dict] = None, params: Optional[dict] = None, headers: Optional[dict] = None
    ) -> Response:
        """ Execute POST request. """
        request_headers = self.prepare_request(headers)
        return requests.post(
            f"{self.base_api_url}{path}",
            headers=request_headers,
            json=json,
            data=data,
            files=files,
            params=params
        )

    def put(self, path: str, json_put: Optional[dict] = None, files: Optional[dict] = None,
            headers: Optional[dict] = None) -> Response:
        """Execute PUT request."""
        request_headers = self.prepare_request(headers)
        return requests.put(
            f"{self.base_api_url}{path}",
            headers=request_headers,
            json=json_put,
            files=files
        )
    def patch(self, path: str, json_patch = None, files: Optional[dict] = None,
            headers: Optional[dict] = None, params:dict=None) -> Response:
        """Execute PATCH request."""
        request_headers = self.prepare_request(headers)
        return requests.patch(
            f"{self.base_api_url}{path}",
            headers=request_headers,
            json=json_patch,
            files=files,
            params=params
        )

    def delete(self, path: str) -> Response:
        """  Execute DELETE request. """
        headers = self.prepare_request()
        response = requests.delete(
            f"{self.base_api_url}{path}",
            headers=headers
        )
        return response

    def attach_file_to_request(self, files: dict, image_path: Optional[str]) -> None:
        """ Attach single image to multipart request. """
        if not image_path:
            return
        mime_type, _ = mimetypes.guess_type(image_path)
        mime_type = mime_type or "application/octet-stream"
        with open(image_path, "rb") as fh:
            files["image"] = (image_path, fh.read(), mime_type)

    def attach_images_to_multipart(self, files: dict, control_name: str,
                                   image_paths: Optional[List[str]]) -> None:
        """ Attach several images to multipart request. """
        if not image_paths:
            files[control_name] = ("", "", "application/octet-stream")
            return
        for path in image_paths:
            if path:
                mime_type, _ = mimetypes.guess_type(path)
                mime_type = mime_type or "application/octet-stream"

                files.setdefault(control_name, [])

                with open(path, "rb") as fh:
                    files[control_name].append(
                        (path, fh.read(), mime_type)
                    )
