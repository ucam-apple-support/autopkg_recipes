#!/usr/local/autopkg/python
#
# Copyright 2020 James Nairn
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import requests

from autopkglib import Processor, ProcessorError

# Set the webhook_url to the one provided by Teams when you create the webhook

__all__ = ["TeamsPostJSS"]


class TeamsPostJSS(Processor):
    description = """Posts to Teams via webhook based on output of JSSImporter.
        Heavily based on https://github.com/autopkg/asemak-recipes/blob/master/PostProcessors/TeamsPost.py
        Tweaked by jwrn3 for JSSImporter output and updated to py3
        Teams alternative to the post processor provided by Ben Reilly
        (@notverypc)
        Based on Graham Pugh's slacker.py -
        https://github.com/grahampugh/recipes/blob/master/PostProcessors/slacker.py
        and
        @thehill idea on macadmin slack -
        https://macadmins.slack.com/archives/CBF6D0B97/p1542379199001400
        Takes elements from
        https://gist.github.com/devStepsize/b1b795309a217d24566dcc0ad136f784
        and
        https://github.com/autopkg/nmcspadden-recipes/blob/master/PostProcessors/Yo.py"""

    input_variables = {
        "jss_importer_summary_result": {
            "required": False,
            "description": ("JSSImporter info dictionary to use to summary."),
        },
        "jss_package_updated": {
            "required": False,
            "description": ("Whether or not item was imported into JSS."),
        },
        "webhook_url": {"required": False, "description": ("Teams webhook.")},
    }
    output_variables = {}

    __doc__ = description

    def main(self):
        was_imported = self.env.get("jss_package_updated")
        jss_info = self.env.get("jss_importer_summary_result")
        webhook_url = self.env.get("webhook_url")

        name = self.env.get("jss_importer_summary_result")["data"]["Name"]
        version = self.env.get("jss_importer_summary_result")["data"]["Version"]
        groups = self.env.get("jss_importer_summary_result")["data"]["Groups"]
        policy = self.env.get("jss_importer_summary_result")["data"]["Policy"]
        jss_server = self.env.get("JSS_URL")

        if not was_imported:
            if name:
                teams_text = f"Title: **{name}**\
                              \nVersion: **{version}**  \nPolicy: **{policy}**  \nGroups:\
                              **{groups}**"
                teams_data = {
                    "text": teams_text,
                    "textformat": "markdown",
                    "title": f"{name} updated on {jss_server}",
                }

            response = requests.post(webhook_url, json=teams_data)
            if response.status_code != 200:
                raise ValueError(
                    f"Request to Teams returned an error {response.status_code}, the response is:\n{response.text}"
                )


if __name__ == "__main__":
    processor = TeamsPostJSS()
    processor.execute_shell()
