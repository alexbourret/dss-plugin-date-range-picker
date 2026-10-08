from html import escape

import dataiku
from dataiku.runnables import Runnable

from date_range_common import get_date_range, get_output_names


class MyRunnable(Runnable):
    def __init__(self, project_key, config, plugin_config):
        self.project_key = project_key
        self.config = config

    def get_progress_target(self):
        return None

    def run(self, progress_callback):
        start_name, end_name = get_output_names(self.config, "variable")
        start_date, end_date = get_date_range(self.config)
        project = dataiku.api_client().get_project(self.project_key)
        variables = project.get_variables()
        variables.setdefault("standard", {}).update({
            start_name: start_date,
            end_name: end_date,
        })
        project.set_variables(variables)
        return (
            "<p>Updated standard project variables:</p>"
            "<ul><li><code>{}</code>: <code>{}</code></li>"
            "<li><code>{}</code>: <code>{}</code></li></ul>"
        ).format(
            escape(start_name), escape(start_date), escape(end_name), escape(end_date)
        )
