
import githubbot.urls
import os
class Organization(object):

    def __init__(self, classroom):
        self.classroom=classroom

    @property
    def name(self):
        """
        The github organization or grade such as "m2r"
        :return: grade
        """
        return self.classroom.grade

    @property
    def url(self):
        """
        The URL of github organization
        (e.g. "http://github.com/l3miage")
        :return: url
        """
        return githubbot.urls.gitHubURL(path=self.name)

    @property
    def dir(self):
        """
        The directory of the organization on the local disk
        (e.g. /media/jmfavre/Windows/DEV/l3miage)
        :return: directory path
        """
        return os.path.join(
            self.classroom.localTopDir,
            self.name)