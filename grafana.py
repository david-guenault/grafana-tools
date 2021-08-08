#! /usr/bin/env python

import json
import os
import sys
import requests
import requests.auth
import urllib
from requests.models import Response
from requests.sessions import session
import time


class grafana(object):
    def __init__(self):
        self.session = requests.session()

    def __get_auth(self):
        return requests.auth.HTTPBasicAuth(username=self.user,password=self.password)    

    def __get_uri(self, path):
        uri = "%s%s" % (self.host, path,)
        return uri

    def __headers_json(self):
        return {
            "Content-Type": "application/json"
        }

    def auth(self):
        response = self.session.get(self.__get_uri("/login"), auth=self.__get_auth())
        if response.status_code != 200:
            print("Authentication failed")
            sys.exit(1)

    def get_orgs(self):
        response = self.session.get(self.__get_uri("/api/orgs"), headers=self.__headers_json(), auth=self.__get_auth())
        return response.json()

    def get_org_by_id(self, id):
        response = self.session.get(self.__get_uri("/api/orgs/%s" % id), headers=self.__headers_json(), auth=self.__get_auth())
        return response.json()

    def get_folders(self):
        response = self.session.get(self.__get_uri("/api/folders"), headers=self.__headers_json(), auth=self.__get_auth())
        return response.json()

    def search_dashboards(self):
        response = self.session.get(self.__get_uri("/api/search?query="), auth=self.__get_auth())
        return response.json()

    def set_current_org(self, org):
        response = self.session.post(self.__get_uri("/api/user/using/%s" % (org["id"],)), auth=self.__get_auth())
        return response.json()

    def get_dashboard_content(self, dashboard):
        response = self.session.get(self.__get_uri("/api/dashboards/uid/%s" % (dashboard["uid"])), auth=self.__get_auth())
        return response.json()

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

