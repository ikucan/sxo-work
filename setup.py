# -*- coding: utf-8 -*-
from pathlib import Path

from pkg_resources import parse_version
from setuptools import Command
from setuptools import find_namespace_packages
from setuptools import setup
from setuptools_scm import get_version


"""
   name: name of the package (e.g. conda install abc-def)
   package: module location but converted to path by setup (eg abc.def)
   url: ...optional
   docs: optional. location of the documentation
   python: ...
"""
package = {
    "name": "sxo",
    "package": "sxo",
    "url": "https://github.com",
    "docs": "README.md",
    "python": ">=3.10",
}


def include_scripts(*script_files):
    scripts = list(script_files)
    print(f"INCLUDE SCRIPTS called with {scripts}")
    return scripts


def _version():
    """
    Define the version tag for this build from git taggs
    """

    pkg_path = Path("src") / package["package"].replace(".", "/")
    if not pkg_path.is_dir():
        raise OSError("Package namespace directory '{pkg_path}' does not exist. Can't build it for you.")

    return get_version(version_scheme="guess-next-dev", local_scheme="node-and-timestamp", write_to=pkg_path / "version.py")


class TagVersionCommand(Command):
    description = "Get the next version by component: major, minor, patch, build(default), release"

    user_options = [
        ("build", None, "Increment the build version number"),
        ("major", None, "Increment the major version number"),
        ("minor", None, "Increment the minor version number"),
        ("patch", None, "Increment the patch version number"),
        ("release", None, "Strip the release-candidate number"),
    ]

    boolean_options = ["build", "major", "minor", "patch", "release"]

    def initialize_options(self):
        self.build = False
        self.major = False
        self.minor = False
        self.patch = False
        self.release = False

    def finalize_options(self):
        pass

    def run(self):
        ver = parse_version(_version())
        if self.major:
            vtag = f"{ver.major + 1}.0.0"
        elif self.minor:
            vtag = f"{ver.major}.{ver.minor + 1}.0"
        elif self.patch and ver.pre is not None:
            vtag = f"{ver.major}.{ver.minor}.{ver.micro + 1}"
        elif self.build or self.release or (self.patch and ver.pre is None):
            vtag = f"{ver.major}.{ver.minor}.{ver.micro}"
        else:
            vtag = str(ver)

        if not self.release:
            vtag += f"rc{1 if ver.pre is None or ver.base_version != vtag else ver.pre[1]}"


setup(
    name=package["name"],
    include_package_data=True,
    include_scripts=True,
    version=_version(),
    author_email="kardenal.mendoza@gmail.com",
    url=package["url"],
    long_description=(Path(package["docs"]).read_text() if not Path(package["docs"]).is_file() else f"## {package['name']}"),
    long_description_content_type="text/markdown",
    package_dir={"": "src"},
    packages=find_namespace_packages(
        where="src",
        include=[package["package"].rsplit(".", 1)[0] + ".*"],
    ),
    python_requires=package["python"],
    setup_requires="setuptools_scm",
    cmdclass={"tag": TagVersionCommand},
)


if __name__ == "__main__":
    ver = parse_version(_version())
    print(parse_version(_version()))
