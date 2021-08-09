#! /usr/bin/env python

import json
import os
import sys
import urllib
import requests
import requests.auth
import urllib.parse
from requests.models import Response
from requests.sessions import session
import time


class grafana(object):
    def __init__(self):
        self.session = requests.session()
        self.debug = True

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
            return False
        else:
            return True

    def import_folder(self, folder):
        response = self.session.post(self.__get_uri("/api/folders"), headers=self.__headers_json(), auth=self.__get_auth(), data=json.dumps(folder))
        if response.status_code != 200:
            return False
        else:
            return response.json()

    def import_org(self, org):
        response = self.session.post(self.__get_uri("/api/orgs"), headers=self.__headers_json(), auth=self.__get_auth(), data=json.dumps(org))
        if response.status_code != 200:
            return False
        else: 
            return response.json()

    def import_dashboard(self, dashboard, folder):
        dashboard["folderId"] = folder["id"]
        response = self.session.post(self.__get_uri("/api/dashboards"), headers=self.__headers_json(), auth=self.__get_auth(), data=json.dumps(dashboard))
        if response.status_code != 200:
            return False
        else: 
            return response.json()

    def delete_org(self, org):
        response = self.session.delete(self.__get_uri("/api/orgs/%s" % org["id"]), headers=self.__headers_json(), auth=self.__get_auth())
        if response.status_code != 200:
            return False
        else:
            return response.json()

    def get_orgs(self):
        response = self.session.get(self.__get_uri("/api/orgs"), headers=self.__headers_json(), auth=self.__get_auth())
        if response.status_code != 200:
            return False
        else:
            return response.json()

    def get_org_by_id(self, id):
        response = self.session.get(self.__get_uri("/api/orgs/%s" % id), headers=self.__headers_json(), auth=self.__get_auth())
        if response.status_code != 200:
            return False
        else:
            return response.json()

    def get_org_by_name(self, name):
        response = self.session.get(self.__get_uri("/api/orgs/name/%s" % urllib.parse.quote(name)), headers=self.__headers_json(), auth=self.__get_auth())
        if response.status_code != 200:
            return False
        else:
            return response.json()

    def get_dashboard_by_uid(self, uid):
        response = self.session.get(self.__get_uri("/api/dashboards/uid/%s" % id), headers=self.__headers_json(), auth=self.__get_auth())
        if response.status_code != 200:
            return False
        else:
            return response.json()

    def get_folders(self):
        response = self.session.get(self.__get_uri("/api/folders"), headers=self.__headers_json(), auth=self.__get_auth())
        if response.status_code != 200:
            return False
        else:
            return response.json()

    def search_dashboards(self):
        response = self.session.get(self.__get_uri("/api/search?query="), auth=self.__get_auth())
        if response.status_code != 200:
            return False
        else:
            return response.json()

    def set_current_org(self, org):
        response = self.session.post(self.__get_uri("/api/user/using/%s" % (org["id"],)), auth=self.__get_auth())
        if response.status_code != 200:
            if self.debug:
                print(response.json())
                print(org)
            return False
        else:
            return response.json()

    def get_dashboard_content(self, dashboard):
        response = self.session.get(self.__get_uri("/api/dashboards/uid/%s" % (dashboard["uid"])), auth=self.__get_auth())
        if response.status_code != 200:
            return False
        else:
            return response.json()

    def get_dashboards(self):
        dashboards_content = {}
        orgs = self.get_orgs()
        if not orgs:
            print("Failed to get org list")
        else:
            for org in orgs:
                if not self.set_current_org(org):
                    print("Unable to set org to %s" % org["name"])
                else:
                    dashboards_content[org["name"]] = {
                        "org": org,
                        "dashboards": [],
                        "folders": []
                    }
                    folders = self.get_folders()
                    if not isinstance(folders, list):
                        print("Unable to get folders")
                    else:
                        for folder in folders:
                            dashboards_content[org["name"]]["folders"].append(folder)
                        dashboards = self.search_dashboards()
                        if not dashboards:
                            print("unable to get dashboards")
                        else:
                            for dashboard in dashboards:
                                dashboard_data = self.get_dashboard_content(dashboard)
                                if not dashboard_data:
                                    print("unable to get dashboard data")
                                else:
                                    dashboards_content[org["name"]]["dashboards"].append(dashboard_data)
        return dashboards_content

