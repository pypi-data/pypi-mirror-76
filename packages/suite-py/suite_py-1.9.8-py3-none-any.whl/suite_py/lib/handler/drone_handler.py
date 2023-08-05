# -*- encoding: utf-8 -*-
from distutils.version import StrictVersion
import os
import time
import subprocess
from subprocess import CalledProcessError
import sys
import requests

from halo import Halo
from suite_py.lib import logger


BASEURL = os.environ["DRONE_SERVER"] = "https://drone-1.prima.it"


class DroneHandler:
    def __init__(self, config, tokens, repo=None):
        self._token = tokens.drone
        os.environ["DRONE_TOKEN"] = self._token
        self._repo = repo
        if repo:
            self._path = os.path.join(config.user["projects_home"], repo)

    def get_last_build_url(self, prefix=None):
        with Halo(text="Contacting drone...", spinner="dots", color="magenta"):
            # necessario per far comparire la build che abbiamo appena pushato
            time.sleep(2)
            try:
                builds = requests.get(
                    f"{BASEURL}/api/repos/primait/{self._repo}/builds",
                    headers={"Authorization": f"Bearer {self._token}"},
                ).json()

                if prefix:
                    builds = [b for b in builds if b["target"].startswith(prefix)]

                return f"{BASEURL}/primait/{self._repo}/{builds[0]['number']}"
            except Exception:
                return ""

    def get_pr_build_number(self, commit_sha):
        with Halo(text="Contacting drone...", spinner="dots", color="magenta"):
            tries = 10
            while tries > 0:
                tries -= 1
                try:
                    builds = requests.get(
                        f"{BASEURL}/api/repos/primait/{self._repo}/builds?per_page=100",
                        headers={"Authorization": f"Bearer {self._token}"},
                    ).json()
                    builds = [b for b in builds if b["after"] == commit_sha]
                    return builds[0]["number"]
                except Exception:
                    time.sleep(1)

            return None

    def get_user(self):
        try:
            user = requests.get(
                f"{BASEURL}/api/user",
                headers={"Authorization": f"Bearer {self._token}"},
            ).json()
            return user
        except Exception:
            return None

    def get_build_url(self, build_number):
        if build_number:
            return f"{BASEURL}/primait/{self._repo}/{build_number}"
        return None

    def get_tags_from_builds(self):
        tags = []
        builds = requests.get(
            f"{BASEURL}/api/repos/primait/{self._repo}/builds?per_page=100",
            headers={"Authorization": f"Bearer {self._token}"},
        ).json()

        for build in builds:
            if build["event"] == "tag":
                tags.append(build["ref"].replace("refs/tags/", ""))

        tags = list(dict.fromkeys(tags))
        tags.sort(key=StrictVersion, reverse=True)
        return tags

    def get_build_from_tag(self, tag):
        attempts = 0
        while attempts < 3:

            try:
                builds = requests.get(
                    f"{BASEURL}/api/repos/primait/{self._repo}/builds?per_page=100",
                    headers={"Authorization": f"Bearer {self._token}"},
                ).json()

                for build in builds:
                    if build["event"] == "tag":
                        if build["ref"].replace("refs/tags/", "") == tag:
                            return build["number"]
            except Exception:
                pass

            time.sleep(2)
            attempts += 1

        return None

    def launch_build(self, build):
        return requests.post(
            f"{BASEURL}/api/repos/primait/{self._repo}/builds/{build}",
            headers={"Authorization": f"Bearer {self._token}"},
        ).json()

    def prestart_success(self, build_number):
        with Halo(text="Contacting drone...", spinner="dots", color="magenta"):
            tries = 10
            while build_number and tries > 0:
                tries -= 1
                build_status = requests.get(
                    f"{BASEURL}/api/repos/primait/{self._repo}/builds/{build_number}",
                    headers={"Authorization": f"Bearer {self._token}"},
                ).json()

                steps = build_status["stages"][0]["steps"]

                for step in steps:
                    if step["name"] == "pre-start":
                        if step["status"] == "success":
                            return True
                        break
                time.sleep(3)
            return False

    def fmt(self):
        try:
            subprocess.run(
                ["drone", "fmt", "--save", ".drone.yml"], cwd=self._path, check=True
            )
        except (CalledProcessError) as e:
            logger.error(
                f"{self._repo}: non sono riuscito a formattare il .drone.yml {e}"
            )
            sys.exit(-1)

    def validate(self):
        try:
            subprocess.run(
                ["drone", "lint", "--trusted", ".drone.yml"], cwd=self._path, check=True
            )
        except (CalledProcessError) as e:
            logger.error(f"{self._path}: il .drone.yml non è valido {e}")
            sys.exit(-1)

    def sign(self):
        try:
            subprocess.run(
                ["drone", "sign", f"primait/{self._repo}", "--save"],
                cwd=self._path,
                check=True,
            )
        except (CalledProcessError) as e:
            logger.error(f"{self._repo}: non sono riuscito a firmare il .drone.yml {e}")
            sys.exit(-1)
