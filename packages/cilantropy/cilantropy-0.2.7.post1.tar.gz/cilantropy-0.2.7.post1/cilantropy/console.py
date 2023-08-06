"""
.. module:: console
   :platform: Unix, Windows
   :synopsis: Cilantropy entry-point for console commands

:mod:`console` -- Cilantropy entry-point for console commands
==================================================================
"""
from .helpers import get_shared_data
from .helpers import get_pkg_res
from .helpers import get_pypi_search
from .helpers import get_pypi_releases
from .helpers import parse_dict
from .helpers import get_kv_colored
from .helpers import get_field_formatted
from .helpers import create_paste_template
from . import metadata
from .settings import __version__
from .settings import __author__
from .settings import __author_url__
from .settings import TEKNIK_PASTE_API

from flask import json

from docopt import docopt
import urllib
import urllib.request

from colorama import init
from colorama import Fore
from colorama import Back
from colorama import Style

import pkg_resources


def cmd_show(args, short=False):
    """This function implements the package show command.

    :param args: the docopt parsed arguments
    """
    proj_name = args["<project_name>"]

    try:
        pkg_dist = get_pkg_res().get_distribution(proj_name)
    except:
        print(
            Fore.RED + Style.BRIGHT
        ) + "Error: unable to locate the project '%s' !" % proj_name
        raise RuntimeError("Project not found !")

    try:
        pkg_metadata = pkg_dist.get_metadata(metadata.METADATA_NAME[0])
    except FileNotFoundError:
        pkg_metadata = pkg_dist.get_metadata(metadata.METADATA_NAME[1])
    except FileNotFoundError:
        pass
    parsed, key_known = metadata.parse_metadata(pkg_metadata)
    distinfo = metadata.metadata_to_dict(parsed, key_known)

    proj_head = Fore.GREEN + Style.BRIGHT + pkg_dist.project_name
    proj_head += Fore.YELLOW + Style.BRIGHT + " " + pkg_dist.version
    print(proj_head),

    proj_sum = Fore.WHITE + Style.DIM
    proj_sum += "- " + parse_dict(distinfo, "summary", True)
    print(proj_sum)

    # Remove long fields and used fields
    if "description" in distinfo:
        del distinfo["description"]

    if "summary" in distinfo:
        del distinfo["summary"]

    if "name" in distinfo:
        del distinfo["name"]

    if "version" in distinfo:
        del distinfo["version"]

    classifier = None
    if "classifier" in distinfo:
        classifier = distinfo["classifier"]
        del distinfo["classifier"]

    for key in distinfo:
        print(get_field_formatted(distinfo, key))

    if short:
        return

    print()
    print(get_kv_colored("location", pkg_dist.location))
    requires = pkg_dist.requires()

    if len(requires) == 0:
        print(get_kv_colored("requires", "none"))
    else:
        req_text = "\n"
        for req in requires:
            req_text += " " * 4 + str(req) + "\n"
        print(get_kv_colored("requires", req_text))

    entry_points = pkg_dist.get_entry_map()
    console_scripts = entry_points.get("console_scripts")
    if console_scripts:
        console_scr_text = Fore.WHITE + Style.BRIGHT + "  Console Scripts:" + "\n"

        for name, entry in console_scripts.items():
            console_scr_text += (
                Fore.YELLOW + Style.BRIGHT + " " * 4 + name + Fore.WHITE + Style.BRIGHT
            )

            console_scr_text += (
                " -> "
                + Fore.GREEN
                + Style.BRIGHT
                + entry.module_name
                + ":"
                + ",".join(entry.attrs)
                + "\n"
            )

        print(console_scr_text)

    if classifier:
        distinfo["classifier"] = classifier
        print(get_field_formatted(distinfo, "classifier"))


def cmd_list_detail(dist, distinfo):
    proj_head = Fore.GREEN + Style.BRIGHT + dist.project_name
    proj_head += Fore.YELLOW + Style.BRIGHT + " " + dist.version
    print(proj_head)

    proj_sum = Fore.WHITE + Style.DIM
    proj_sum += "- " + parse_dict(distinfo, "summary", True)
    print(proj_sum)

    print(get_field_formatted(distinfo, "Author"))
    author_email = distinfo.get("author-email")
    if author_email:
        print("<%s>" % author_email)
    else:
        print()

    print(get_field_formatted(distinfo, "Home-page"))
    print(get_field_formatted(distinfo, "License"))
    print(get_field_formatted(distinfo, "Platform"))


def cmd_list_compact(dist, distinfo):
    proj_head = Fore.GREEN + Style.BRIGHT + dist.project_name.ljust(25)
    proj_head += Fore.WHITE + Style.BRIGHT + " " + dist.version.ljust(12)
    print(proj_head, end="")

    proj_sum = Fore.WHITE + Style.DIM
    proj_sum += " " + parse_dict(distinfo, "summary", True)
    print(proj_sum.ljust(100))


def cmd_list(args):
    """This function implements the package list command.

    :param args: the docopt parsed arguments
    """
    compact = args["--compact"]
    filt = args["<filter>"]
    distributions = get_shared_data()["distributions"]

    if compact:
        print(
            Fore.YELLOW
            + Style.BRIGHT
            + "Project Name".ljust(26)
            + "Version".ljust(14)
            + "Summary"
        )
        print("-" * 80)

    for dist in distributions:
        if filt:
            if filt.lower() not in dist.project_name.lower():
                continue

        pkg_dist = get_pkg_res().get_distribution(dist.key)
        try:
            pkg_metadata = pkg_dist.get_metadata(metadata.METADATA_NAME[0])
        except FileNotFoundError:
            pkg_metadata = pkg_dist.get_metadata(metadata.METADATA_NAME[1])
        except FileNotFoundError:
            pass
        parsed, key_known = metadata.parse_metadata(pkg_metadata)
        distinfo = metadata.metadata_to_dict(parsed, key_known)

        if compact:
            cmd_list_compact(dist, distinfo)
        else:
            cmd_list_detail(dist, distinfo)


def cmd_check(args):
    proj_name = args["<project_name>"]
    cmd_show(args, short=True)

    print()
    print(Fore.GREEN + Style.BRIGHT + "Searching for updates on PyPI...")
    print()

    pkg_dist_version = get_pkg_res().get_distribution(proj_name).version
    pypi_rel = get_pypi_releases(proj_name)

    if pypi_rel:
        pypi_last_version = get_pkg_res().parse_version(pypi_rel[0])
        current_version = get_pkg_res().parse_version(pkg_dist_version)

        try:
            version_index = pypi_rel.index(pkg_dist_version)
        except:
            version_index = len(pypi_rel)

        for version in pypi_rel[0 : version_index + 3]:
            print(Fore.WHITE + Style.BRIGHT + "  Version %s" % version, end=" ")
            if version == pypi_rel[0]:
                print(Fore.BLUE + Style.BRIGHT + "[last version]", end=" ")

            if version == pkg_dist_version:
                print(Fore.GREEN + Style.BRIGHT + "[your version]", end="")

            print()

        print()

        if pypi_last_version > current_version:
            print(
                Fore.RED
                + Style.BRIGHT
                + "  Your version is outdated, you're using "
                + Fore.WHITE
                + Style.BRIGHT
                + "v.%s," % pkg_dist_version
                + Fore.RED
                + Style.BRIGHT
                + " but the last version is "
                + Fore.WHITE
                + Style.BRIGHT
                + "v.%s !" % pypi_rel[0]
            )

        if pypi_last_version == current_version:
            print(Fore.GREEN + Style.BRIGHT + "  Your version is updated !")

        if pypi_last_version < current_version:
            print(
                Fore.YELLOW
                + Style.BRIGHT
                + "  Your version newer than the version available at PyPI !"
            )

            print(
                Fore.YELLOW
                + Style.BRIGHT
                + "  You're using "
                + Fore.WHITE
                + Style.BRIGHT
                + "v.%s," % pkg_dist_version
                + Fore.YELLOW
                + Style.BRIGHT
                + " but the last version in PyPI "
                + Fore.WHITE
                + Style.BRIGHT
                + "v.%s !" % pypi_rel[0]
            )

    else:
        print("No versions found on PyPI !")


def cmd_scripts(args):
    filt = args["<filter>"]

    print(
        Fore.YELLOW
        + Style.BRIGHT
        + "Script Name".ljust(23)
        + "Project Name".ljust(21)
        + "Module Name"
    )
    print("-" * 80)
    for entry in pkg_resources.iter_entry_points("console_scripts"):
        if filt:
            if filt.lower() not in entry.name.lower():
                continue

        print(Fore.GREEN + Style.BRIGHT + entry.name.ljust(22), end="")
        print(Fore.WHITE + Style.NORMAL + str(entry.dist).ljust(20), end="")
        print(Fore.BLUE + Style.BRIGHT + entry.module_name, end="")
        print(Fore.BLUE + Style.NORMAL + "(" + entry.attrs[0] + ")", end="\n")


def cmd_paste(args):
    template_data = create_paste_template()

    data = urllib.parse.urlencode({"code": template_data})
    res = urllib.request.urlopen(TEKNIK_PASTE_API, bytes(data, encoding="utf-8"))
    result = json.loads(res.read().decode("utf-8"))

    if "result" in result:
        print(
            Fore.GREEN + Style.BRIGHT + "Paste url: {}".format(result["result"]["url"])
        )
    else:
        print(Fore.RED + Style.BRIGHT + "ERROR PASTE!")


def run_main():
    """Cilantropy - Python List Packages (PLP)

    Usage:
      plp list [--compact] [<filter>]
      plp show <project_name>
      plp check <project_name>
      plp scripts [<filter>]
      plp paste [list your packages to pastebin service]

      plp (-h | --help)
      plp --version

    Options:
      --compact     Compact list format
      -h --help     Show this screen.
      --version     Show version.
    """
    init(autoreset=True)

    arguments = docopt(
        run_main.__doc__,
        version="Cilantropy v.%s - Python List Packages (PLP)" % __version__,
    )

    if arguments["list"]:
        cmd_list(arguments)

    if arguments["show"]:
        cmd_show(arguments)

    if arguments["check"]:
        cmd_check(arguments)

    if arguments["scripts"]:
        cmd_scripts(arguments)

    if arguments["paste"]:
        cmd_paste(arguments)


if __name__ == "__main__":
    run_main()
