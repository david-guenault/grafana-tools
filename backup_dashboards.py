#! /usr/bin/env python

import json
import sys
import os
from grafana import grafana


class grafana_backup(grafana):
    def __init__(self):
        self.host = os.environ["grafana_uri"] if "grafana_uri" in os.environ else ""
        self.backup_file = os.environ["grafana_backup_file"] if "grafana_backup_folder" in os.environ else ""
        self.user = os.environ["grafana_user"] if "grafana_user" in os.environ else ""
        self.password = os.environ["grafana_password"] if "grafana_password" in os.environ else ""

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

    def write_backup(self, data):
        path = self.backup_file
        print("Write backup to %s" % path)
        h = open(path, "w")
        h.write(json.dumps(data, indent=4))
        h.close()

    def get_dashboards(self):
        dashboards = {}
        for org in self.get_orgs():
            self.set_current_org(org)
            dashboards[org["name"]] = {
                "org": org,
                "dashboards": [],
                "folders": []
            }
            for folder in self.get_folders():
                dashboards[org["name"]]["folders"].append(folder)
            for dashboard in self.search_dashboards():
                dashboards[org["name"]]["dashboards"].append(dashboard)
        return dashboards

if __name__ == '__main__':
    gb = grafana_backup()
    gb.auth()
    dashboards = gb.get_dashboards()
    gb.write_backup(dashboards)


