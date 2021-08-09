#! /usr/bin/env python

import json
import sys
import os
from grafana import grafana


class grafana_backup(grafana):
    def __init__(self):
        self.host = os.environ["grafana_uri"] if "grafana_uri" in os.environ else ""
        self.backup_file = os.environ["grafana_backup_file"] if "grafana_backup_file" in os.environ else ""
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

        if self.backup_file == "":
            print("you must define environment variable grafana_backup_file")
            sys.exit(1)


        grafana.__init__(self)

    def write_backup(self, data):
        path = self.backup_file
        print(path)
        print("Write backup to %s" % path)
        h = open(path, "w")
        h.write(json.dumps(data, indent=4))
        h.close()

    def backup_dashboards(self):
        dashboards = self.get_dashboards()
        self.write_backup(dashboards)

if __name__ == '__main__':
    gb = grafana_backup()
    gb.auth()
    gb.backup_dashboards()


