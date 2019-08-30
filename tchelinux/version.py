"""System component versions."""


class Version(object):
    """Hold the version values of system components."""

    __CURRENT_VERSION = "0.1"

    __DB_REVISION = {
        "0.1": "61c21012b79d"
    }
    __DB_VERSION = {v: k for k, v in __DB_REVISION.items()}

    @classmethod
    def version_string(self, name="System"):
        """Retrieve the system string version."""
        return "{} version {}".format(name, Version.__CURRENT_VERSION)

    @classmethod
    def system(self):
        """Retrive system current version."""
        return Version.__CURRENT_VERSION

    @classmethod
    def db_revision(self, version=None):
        """Retrieve database revision for a specific version."""
        v = Version.system() if version is None else version
        return Version.__DB_REVISION.get(v, "invalid")

    @classmethod
    def db_version(self, revision=None):
        """Retrieve the system version for a database revision."""
        v = self.db_revision() if revision is None else revision
        return Version.__DB_VERSION.get(v, "invalid")

    @classmethod
    def version_match(self, revision, system_version=__CURRENT_VERSION):
        """Check if a database and system revision are in sync."""
        return Version.db_version(revision) == system_version
