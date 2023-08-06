# -*- coding: utf-8 -*-
"""Config utility functions for vcspull.
vcspull.config
~~~~~~~~~~~~~~

A lot of these items are todo.

"""
from __future__ import absolute_import, print_function, unicode_literals

import fnmatch
import glob
import logging
import os

import kaptan

from libvcs._compat import string_types

from . import exc
from .util import CONFIG_DIR, update_dict

log = logging.getLogger(__name__)


def expand_dir(_dir, cwd=os.getcwd()):
    """Return path with environmental variables and tilde ~ expanded.

    :param _dir:
    :type _dir: str
    :param cwd: current working dir (for deciphering relative _dir paths)
    :type cwd: str
    :rtype; str
    """
    _dir = os.path.expanduser(os.path.expandvars(_dir))
    if not os.path.isabs(_dir):
        _dir = os.path.normpath(os.path.join(cwd, _dir))
    return _dir


def extract_repos(config, cwd=os.getcwd()):
    """Return expanded configuration.

    end-user configuration permit inline configuration shortcuts, expand to
    identical format for parsing.

    :param config: the repo config in :py:class:`dict` format.
    :type config: dict
    :param cwd: current working dir (for deciphering relative paths)
    :type cwd: str
    :rtype: list

    """
    configs = []
    for directory, repos in config.items():
        for repo, repo_data in repos.items():

            conf = {}

            '''
            repo_name: http://myrepo.com/repo.git

            to

            repo_name: { url: 'http://myrepo.com/repo.git' }

            also assures the repo is a :py:class:`dict`.
            '''

            if isinstance(repo_data, string_types):
                conf['url'] = repo_data
            else:
                conf = update_dict(conf, repo_data)

            if 'repo' in conf:
                if 'url' not in conf:
                    conf['url'] = conf.pop('repo')
                else:
                    conf.pop('repo', None)

            '''
            ``shell_command_after``: if str, turn to list.
            '''
            if 'shell_command_after' in conf:
                if isinstance(conf['shell_command_after'], string_types):
                    conf['shell_command_after'] = [conf['shell_command_after']]

            if 'name' not in conf:
                conf['name'] = repo
            if 'parent_dir' not in conf:
                conf['parent_dir'] = expand_dir(directory, cwd)

            if 'repo_dir' not in conf:
                conf['repo_dir'] = expand_dir(
                    os.path.join(conf['parent_dir'], conf['name']), cwd
                )
            if 'remotes' in conf:
                remotes = []
                for remote_name, url in conf['remotes'].items():
                    remotes.append({'remote_name': remote_name, 'url': url})
                conf['remotes'] = sorted(
                    remotes, key=lambda x: sorted(x.get('remote_name'))
                )
            configs.append(conf)

    return configs


def find_home_config_files(filetype=['json', 'yaml']):
    """Return configs of ``.vcspull.{yaml,json}`` in user's home directory."""
    configs = []

    yaml_config = os.path.expanduser('~/.vcspull.yaml')
    has_yaml_config = os.path.exists(yaml_config)
    json_config = os.path.expanduser('~/.vcspull.json')
    has_json_config = os.path.exists(json_config)

    if not has_yaml_config and not has_json_config:
        log.debug(
            'No config file found. Create a .vcspull.yaml or .vcspull.json'
            ' in your $HOME directory. http://vcspull.git-pull.com for a'
            ' quickstart.'
        )
    else:
        if sum(filter(None, [has_json_config, has_yaml_config])) > int(1):
            raise exc.MultipleConfigWarning()
        if has_yaml_config:
            configs.append(yaml_config)
        if has_json_config:
            configs.append(json_config)

    return configs


def find_config_files(
    path=['~/.vcspull'], match=['*'], filetype=['json', 'yaml'], include_home=False
):
    """Return repos from a directory and match. Not recursive.

    :param path: list of paths to search
    :type path: list
    :param match: list of globs to search against
    :type match: list
    :param filetype: list of filetypes to search against
    :type filetype: list
    :param include_home: Include home configuration files
    :type include_home: bool
    :raises:
        - LoadConfigRepoConflict: There are two configs that have same path
          and name with different repo urls.
    :returns: list of absolute paths to config files.
    :rtype: list

    """
    configs = []

    if include_home is True:
        configs.extend(find_home_config_files())

    if isinstance(path, list):
        for p in path:
            configs.extend(find_config_files(p, match, filetype))
            return configs
    else:
        path = os.path.expanduser(path)
        if isinstance(match, list):
            for m in match:
                configs.extend(find_config_files(path, m, filetype))
        else:
            if isinstance(filetype, list):
                for f in filetype:
                    configs.extend(find_config_files(path, match, f))
            else:
                match = os.path.join(path, match)
                match += ".{filetype}".format(filetype=filetype)

                configs = glob.glob(match)

    return configs


def load_configs(files, cwd=os.getcwd()):
    """Return repos from a list of files.

    :todo: Validate scheme, check for duplciate destinations, VCS urls

    :param files: paths to config file
    :type files: list
    :param cwd: current path (pass down for :func:`extract_repos`
    :type cwd: str
    :returns: expanded config dict item
    :rtype: list of dict
    """
    repos = []
    for f in files:
        _, ext = os.path.splitext(f)
        conf = kaptan.Kaptan(handler=ext.lstrip('.')).import_config(f)

        newrepos = extract_repos(conf.export('dict'), cwd)

        if not repos:
            repos.extend(newrepos)
            continue

        dupes = detect_duplicate_repos(repos, newrepos)

        if dupes:
            msg = ('repos with same path + different VCS detected!', dupes)
            raise exc.VCSPullException(msg)
        repos.extend(newrepos)

    return repos


def detect_duplicate_repos(repos1, repos2):
    """Return duplicate repos dict if repo_dir same and vcs different.

    :param repos1: list of repo expanded dicts
    :type repos1: list of :py:dict
    :param repos2: list of repo expanded dicts
    :type repos2: list of :py:dict
    :rtype: list of dicts or None
    :returns: Duplicate lists
    """
    dupes = []
    path_dupe_repos = []

    curpaths = [r['repo_dir'] for r in repos1]
    newpaths = [r['repo_dir'] for r in repos2]
    path_duplicates = list(set(curpaths).intersection(newpaths))

    if not path_duplicates:
        return None

    path_dupe_repos.extend(
        [r for r in repos2 if any(r['repo_dir'] == p for p in path_duplicates)]
    )

    if not path_dupe_repos:
        return None

    for n in path_dupe_repos:
        currepo = next((r for r in repos1 if r['repo_dir'] == n['repo_dir']), None)
        if n['url'] != currepo['url']:
            dupes += (n, currepo)
    return dupes


def in_dir(config_dir=CONFIG_DIR, extensions=['.yml', '.yaml', '.json']):
    """Return a list of configs in ``config_dir``.

    :param config_dir: directory to search
    :type config_dir: str
    :param extensions: filetypes to check (e.g. ``['.yaml', '.json']``).
    :type extensions: list
    :rtype: list

    """
    configs = []

    for filename in os.listdir(config_dir):
        if is_config_file(filename, extensions) and not filename.startswith('.'):
            configs.append(filename)

    return configs


def filter_repos(config, repo_dir=None, vcs_url=None, name=None):
    """Return a :py:obj:`list` list of repos from (expanded) config file.

    repo_dir, vcs_url and name all support fnmatch.

    :param config: the expanded repo config in :py:class:`dict` format.
    :type config: dict
    :param repo_dir: directory of checkout location, fnmatch pattern supported
    :type repo_dir: str or None
    :param vcs_url: url of vcs remote, fn match pattern supported
    :type vcs_url: str or None
    :param name: project name, fnmatch pattern supported
    :type name: str or None
    :rtype: list

    """
    repo_list = []

    if repo_dir:
        repo_list.extend(
            [r for r in config if fnmatch.fnmatch(r['parent_dir'], repo_dir)]
        )

    if vcs_url:
        repo_list.extend(
            r for r in config if fnmatch.fnmatch(r.get('url', r.get('repo')), vcs_url)
        )

    if name:
        repo_list.extend([r for r in config if fnmatch.fnmatch(r.get('name'), name)])

    return repo_list


def is_config_file(filename, extensions=['.yml', '.yaml', '.json']):
    """Return True if file has a valid config file type.

    :param filename: filename to check (e.g. ``mysession.json``).
    :type filename: str
    :param extensions: filetypes to check (e.g. ``['.yaml', '.json']``).
    :type extensions: list or str
    :rtype: bool

    """
    extensions = [extensions] if isinstance(extensions, string_types) else extensions
    return any(filename.endswith(e) for e in extensions)
