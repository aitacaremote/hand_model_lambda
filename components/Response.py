import datetime
import enum
import json
import requests
import os


class Status(str, enum.Enum):
    CREATED = "CREATED"
    BUSY = "BUSY"
    READY = "READY"
    PARTIAL = "PARTIAL"
    ERROR = "ERROR"


class Response:
    status: Status
    version: int
    measurement_id: int
    _results: dict
    _params: dict

    def __init__(self, version: int, params: dict, measurement_id: int):
        self.status = Status.CREATED
        self.version = version
        self._params = params
        self.measurement_id = measurement_id
        self._params["dateMeasurement"] = str(datetime.datetime.now())
        self.results = {}

    def json(self):
        return json.dumps(
            {"model_version": {"id": self.version}, "status": self.status.value, "data": self._results})

    def connect(self):
        if self.status == Status.CREATED:
            self.status = Status.BUSY
        request = requests.patch(
            os.getenv("MEASUREMENT_SERVICE_URL",
                      "http://127.0.0.1:5000/measurement_service") + f'/measurement/{self.measurement_id}',
            data=self.json())
        if request.status_code == 200:
            return request.json()
        else:
            raise ConnectionError()

    @property
    def results(self):
        return self._results

    @results.setter
    def results(self, value: dict):
        self._results = self._params.copy() | value

    def set_status(self, status: Status):
        self.status = status

