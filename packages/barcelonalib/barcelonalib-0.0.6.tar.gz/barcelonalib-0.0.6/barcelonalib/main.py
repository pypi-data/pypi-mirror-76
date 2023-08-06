import logging
from logging import LogRecord, Logger
from io import StringIO
import os
import sys
import datetime

from opentelemetry import trace
from opentelemetry.trace import Tracer
from opentelemetry.trace.span import DefaultSpan
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter
from opentelemetry.sdk.trace.export import BatchExportSpanProcessor

import json


# TODO: Think about moving logger to a library of some kind so that it can be reused with this signature across derivaed containers
class setupLogger:
    _rootLogger = None
    _buffer = None

    def __init__(self, debug=False):
        logLevel = logging.WARN
        if debug:
            logLevel = logging.DEBUG

        self._rootLogger = logging.getLogger()
        self._rootLogger.setLevel(logLevel)
        formatter = logging.Formatter("::%(levelname)s - %(message)s")

        if not self._rootLogger.hasHandlers():
            self._buffer = StringIO()
            bufferHandler = logging.StreamHandler(self._buffer)
            bufferHandler.setLevel(logLevel)
            bufferHandler.setFormatter(formatter)
            bufferHandler.set_name("buffer.logger")
            self._rootLogger.addHandler(bufferHandler)

            stdout_handler = logging.StreamHandler(sys.stdout)
            stdout_handler.setLevel(logLevel)
            stdout_handler.setFormatter(formatter)
            stdout_handler.set_name("stdout.logger")
            self._rootLogger.addHandler(stdout_handler)

            set_output_handler = logging.StreamHandler(sys.stdout)
            set_output_handler.setLevel(logging.NOTSET)
            set_output_handler.setFormatter(logging.Formatter("%(message)s"))
            set_output_handler.addFilter(self.filter_for_outputs)
            set_output_handler.set_name("setoutput.logger")
            self._rootLogger.addHandler(set_output_handler)
        else:
            for i, handler in enumerate(self._rootLogger.handlers):
                if handler.name == "buffer.logger":
                    self._buffer = self._rootLogger.handlers[i].stream
                    break

            if self._buffer is None:
                raise SystemError(
                    "Somehow, we've lost the 'buffer' logger, meaning nothing will be printed. Exiting now."
                )

    def get_loggers(self):
        return (self._rootLogger, self._buffer)

    def get_root_logger(self):
        return self._rootLogger

    def get_buffer(self):
        return self._buffer

    def print_and_log(self, variable_name, variable_value):
        # echo "::set-output name=time::$time"
        output_message = f"::set-output name={variable_name}::{variable_value}"
        print(output_message)
        print(f"{variable_name} - Length: {len(variable_value)}")
        self._rootLogger.debug(output_message)

        return output_message

    @staticmethod
    def filter_for_outputs(record: LogRecord):
        if str(record.msg).startswith("::set-output"):
            return True
        return False


class Barcelona:
    _logger: Logger = None
    _tracer: Tracer = None
    _root_span: DefaultSpan = None
    _curernt_span: DefaultSpan = None

    _project: str = None
    _run_id: str = None
    _root_step_id: str = None
    _current_step_id: str = None
    _current_parent_span = None

    def __init__(
        self,
        directory="/tmp/barcelona",
        debug=False,
        repo_id=None,
        project=None,
        run_id=None,
        step_id=None,
        tracer_name=None,
    ):
        self._repo_id = repo_id
        if self._repo_id is None:
            self._repo_id = os.environ.get("GITHUB_REPO", "FAKE_REPO")

        self._project = project
        if self._project is None:
            self._project = os.environ.get("INPUT_OCTOSTORE_PROJECT", "FAKE_PROJECT")

        self._run_id = run_id
        if self._run_id is None:
            self._run_id = os.environ.get("INPUT_OCTOSTORE_RUN_ID", "FAKE_RUN_ID")

        self._root_step_id = step_id
        if self._root_step_id is None:
            self._root_step_id = os.environ.get("GITHUB_ACTION", "Root Step")

        trace.set_tracer_provider(TracerProvider())
        self._tracer = trace.get_tracer(__name__)
        # span_processor = BatchExportSpanProcessor(ConsoleSpanExporter())
        # trace.get_tracer_provider().add_span_processor(span_processor)

    def start_root_span(self, attributes: dict = {}):
        self._current_step_id = self._root_step_id
        self._tracer.start_as_current_span(self._root_step_id)
        self._current_span = self._tracer.CURRENT_SPAN
        for attrib_key in attributes:
            self._current_span.set_attribute(attrib_key, attributes[attrib_key])

        self._current_span.set_attribute("project", self._project)
        self._current_span.set_attribute("run_id", self._run_id)
        self._current_span.set_attribute("step_id", self._current_step_id)

        self._root_span = self._current_span

        return self._root_span

    def end_root_span(self):
        # TODO: Doesn't check to see if all children span are closed
        self._root_span.end()

    def start_child_span(self, name, attributes: dict = {}):
        self._current_parent_span = self._tracer.CURRENT_SPAN
        self._tracer.start_as_current_span(name, attributes=attributes)
        self._curernt_span = self._tracer.CURRENT_SPAN
        self._current_span.set_attribute("project", self._project)
        self._current_span.set_attribute("run_id", self._run_id)

        self._current_step_id = name
        self._current_span.set_attribute("step_id", self._current_step_id)

    def end_child_span(self):
        """ Ends current span and sets the current span as the parent span """

        # The below works because opentelemetry auto assigns the parent span to be the current
        # span if a child span is closed.
        self._current_span.end()
        self._current_span = self._tracer.CURRENT_SPAN

        # TODO: Because the below just assigns root step_id to current, it means we
        # can't support multiple children spans (yet) - need to figure out opentelemetry
        # objects and just use them, instead of tracking myself
        self._current_step_id = self._root_step_id
        self._current_parent_span = None

    def log_info(self, value):
        self._add_event("info", "log_info", value)

    def log_value(self, key, value):
        self._add_event("value", key, value)

    def log_param(self, key, value):
        self._add_event("parameter", key, value)

    def log_metric(self, key, value):
        self._add_event("metric", key, value)

    def log_error(self, key, value):
        self._add_event("error", key, value)

    def log_bool(self, key, value: bool):
        self._add_event("bool", key, value)

    def log_return_code(self, label, value):
        self._add_event("return_code", label, value)

    def log_artifact(self, label, value):
        self._add_event("artifact", label, value)

    def log_assert(self, label, value):
        self._add_event("assert", label, value)

    def log_model(self, label, value):
        self._add_event("model", label, value)

    def _add_event(self, event_type, key, value):
        repo_id = self._repo_id
        project = self._project
        run_id = self._run_id
        step_id = self._current_step_id
        parent_span = self._current_parent_span
        parent_id = None
        if parent_span is not None:
            parent_id = parent_span.get_context().span_id

        commit_hash = os.environ.get(
            "GITHUB_SHA", "0000000000000000000000000000000000000000"
        )
        log_dict = {
            "repo_id": repo_id,
            "project": project,
            "run_id": run_id,
            "step_id": step_id,
            "parent_id": parent_id,
            "commit_hash": commit_hash,
            "event_type": event_type,
            "metadata_key": str(key),
            "metadata_value": str(value),
        }

        if self._current_span is None:
            raise AttributeError(
                'You have not started your root span. Please make sure to do so with start_root_span("NAME")'
            )

        # TODO: Not doing anything interesting with these events on the span, but could easily (soon)
        self._current_span.add_event(event_type, log_dict)

        log_string = ""
        log_string += f"{datetime.datetime.now().isoformat()} ##[debug]"
        log_string += "[barcelona]"
        log_string += "%s" % json.dumps(log_dict)

        print(log_string)
