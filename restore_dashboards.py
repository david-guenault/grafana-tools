#! /usr/bin/env python

import json
import sys
import os
from grafana import grafana


class grafana_restore(grafana):
    def __init__(self):
        self.host = os.environ["grafana_uri"] if "grafana_uri" in os.environ else ""
        self.backup_file = os.environ["grafana_backup_file"] if "grafana_backup_folder" in os.environ else ""
        self.user = os.environ["grafana_user"] if "grafana_user" in os.environ else ""
        self.password = os.environ["grafana_password"] if "grafana_password" in os.environ else ""
        self.data = []

        if self.host == "":
            print("you must define environment variable grafana_uri")
            sys.exit(1)

        if self.user == "":
            print("you must define environment variable grafana_user")
            sys.exit(1)

        if self.password == "":
            print("you must define environment variable grafana_password")
            sys.exit(1)

        grafana.__init__(self)

    def open_backup(self):
        path = self.backup_file
        print("Open backup file %s" % path)
        h = open(path, "r")
        self.data = json.loads(h.read())
        h.close()

    def restore_dashboards(self):
        for org, data_org in self.data.items():
            print("Check org %s" % org)

            result = self.get_org_by_id(data_org["org"]["id"])
            if "message" in result.keys():
                print("Organisation not found")
            else:
                print("Organisation found")

if __name__ == '__main__':
    gr = grafana_restore()
    gr.auth()
    gr.open_backup()
    gr.restore_dashboards()


