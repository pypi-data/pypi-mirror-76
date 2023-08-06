#!/usr/bin/env python3
# Copyright 2020-present NAVER Corp. Under BSD 3-clause license

"""
script to easily  download kapture datasets.
"""

import argparse
import logging
import sys
import os
import os.path as path
import requests
import yaml
import fnmatch
from typing import Dict, Optional, List
from tqdm import tqdm
import tarfile
import hashlib
from shutil import rmtree
from subprocess import call
import path_to_kapture
# import kapture
import kapture.utils.logging
from kapture.converter.downloader.download import download_file
from kapture.converter.downloader.archives import untar_file

logger = logging.getLogger('downloader')
logging.basicConfig(format='%(levelname)-8s::%(name)s: %(message)s')

INDEX_FILENAME = 'kapture_dataset_index.yaml'
DEFAULT_DATASET_PATH = path.normpath(path.abspath('.'))
DEFAULT_REPOSITORY_URL = 'https://github.com/naver/kapture/raw/master/dataset'
# DEFAULT_REPOSITORY_URL = 'https://download.europe.naverlabs.com/kapture/'
datasets = {}


def ask_confirmation(question):
    """
    ask "question" to the user.
    The "answer" return value is True for "yes" or False for "no".
    """
    validate = ['yes', 'y', 'ye']
    prompt = ' [y/N]\n'
    sys.stdout.write(question + prompt)
    user_choice = input().lower()
    return user_choice in validate


class Dataset:
    def __init__(
            self,
            name: str,
            install_dirpath: str,
            archive_url: str,
            archive_sha256sum: str,
            install_script_filename: Optional[str] = None
    ):
        """
        :param name: name of the archive (dataset or part of a dataset)
        :param install_dirpath: input absolute path to root directory where all datasets are installed.
        :param archive_url: remote url of the dataset archive (tar).
        :param archive_sha256sum: expected sha256 sum of the archive file.
        :param install_script_filename: if given, this script is to be called to finish installation (eg. dl 3rd party).
        """
        self._name = name

        self._install_local_path = install_dirpath
        self._archive_filepath = path.join(install_dirpath, name + '.tar.gz')
        self._dataset_index_filepath = path.join(install_dirpath, 'kapture_dataset_index.yaml')
        self._dataset_install_list_filepath = path.join(install_dirpath, 'kapture_dataset_installed.yaml')
        self._archive_url = archive_url
        self._archive_sha256sum_remote = archive_sha256sum
        self._install_script_filename = install_script_filename
        self._status = None

    def save_as_installed(self):
        # load previous version
        if path.isfile(self._dataset_install_list_filepath):
            with open(self._dataset_install_list_filepath, 'rt') as f:
                datasets_list = set(yaml.safe_load(f))
        else:
            datasets_list = set()
        datasets_list.add(self._name)
        # update with current dataset status
        # write updated version
        with open(self._dataset_install_list_filepath, 'wt') as f:
            yaml.dump(list(datasets_list), f)

    def is_installed(self, installation_list_cache=None):
        """
        :param installation_list_cache: spare the read of the yaml file if already loaded before.
        """
        if installation_list_cache is not None:
            installation_list = installation_list_cache
        elif path.isfile(self._dataset_install_list_filepath):
            with open(self._dataset_install_list_filepath, 'rt') as f:
                installation_list = yaml.safe_load(f)
        else:
            installation_list = []

        assert isinstance(installation_list, list)
        return self._name in installation_list

    def is_archive_valid(self):
        """ check sha256 of the archive against the expected sha256. Returns true if they are the same. """
        if not path.isfile(self._archive_filepath):
            return False
        # size is consistent, check sha256
        sha256_hash = hashlib.sha256()
        with open(self._archive_filepath, 'rb') as f:
            # Read and update hash string value in blocks of 4K
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        sha256sum_archive_local = sha256_hash.hexdigest()
        if sha256sum_archive_local != self._archive_sha256sum_remote:
            logger.warning(f'sha256sum discrepancy for {self._archive_filepath} :\n'
                           f'\tlocal :{sha256sum_archive_local}\n'
                           f'\tremote:{self._archive_sha256sum_remote}')
            return False

        return True

    @property
    def status(self):
        if self._status is None:
            return self.prob_status()
        else:
            return self._status

    @property
    def url(self):
        return self._archive_url

    def set_status(self, new_status=None):
        if self._status != new_status:
            self._status = new_status
            if new_status == 'installed':
                self.save_as_installed()

    def prob_status(self, check_online=False):
        """
        gives the actual dataset status
         - not installed: means is not installed (wo info about the server)
         - online: means not installed, not downloaded, but reachable.
         - not reachable: means not installed, not downloaded, but NOT reachable.
         - installed: means has been downloaded and installed (extracted).
         - downloaded: means has been downloaded (tar) but not installed (extracted) yet.
         - incomplete: means partially downloaded
         - corrupted: means that the downloaded archive is curropted (inconsistent size or sh256).
         - unknown: should not happen

        :param check_online: If true, will ping the url to check its actually online
        """

        probing_status = None
        if self.is_installed():
            # yaml file says its installed, trust it (no other choices).
            probing_status = 'installed'

        if probing_status is None and not path.isfile(self._archive_filepath):
            # not installed, no archive there, check its online
            if not check_online:
                probing_status = 'not installed'
            elif requests.head(self._archive_url).status_code == 200:
                probing_status = 'online'
            else:
                probing_status = 'not reachable'

        # not installed, but archive there, check 1) its incomplete or 2) corrupted. If neither, is just downloaded.
        if probing_status is None:
            assert path.isfile(self._archive_filepath)
            # 1) check its incomplete: has it proper size ?
            r = requests.head(self._archive_url)
            size_archive_online = int(r.headers.get('content-length', 0))
            size_archive_local = int(path.getsize(self._archive_filepath))
            if size_archive_local < size_archive_online:
                logger.debug(f'file_size_online={size_archive_online} != file_size_local={size_archive_local}')
                probing_status = 'incomplete'
            elif size_archive_local > size_archive_online:
                logger.critical(f'inconsistent file size ({size_archive_online} vs {size_archive_local})')
                probing_status = 'corrupted'

        if probing_status is None:
            # 2) size is consistent, check sha256
            assert size_archive_local == size_archive_online
            if not self.is_archive_valid():
                probing_status = 'corrupted'

        if probing_status is None:
            # archive is there, not installed, not incomplete, not corrupted, then it must be just downloaded
            probing_status = 'downloaded'

        self.set_status(probing_status)
        return probing_status

    def __repr__(self):
        return f'{self.status:10} | {self._name:30} | {self._archive_url}'

    def download(self):
        if self.status != 'downloaded':
            download_file(self._archive_url, self._archive_filepath)
            self.set_status('downloaded')

    def install(self, force_overwrite: bool = False):
        """ Install handle download and untar """
        # test the dataset presence
        self.set_status()
        # make sure self._status is up to date.
        if self.status == 'installed' and not force_overwrite:
            logger.info(f'{self._install_local_path} already exists: skipped')
            return

        # 1) download
        if self.status != 'downloaded':
            # check archive file integrity
            if self._status == 'corrupted':
                logger.warning(f'archive {path.basename(self._archive_filepath)} is corrupted. '
                               f'It will be downloaded again.')
                # if corrupted: remove the archive and start over
                os.remove(self._archive_filepath)
            download_file(self._archive_url, self._archive_filepath)
            self.set_status('downloaded')

        # 2) untar
        logger.info(f'deflating {path.basename(self._archive_filepath)} to {self._install_local_path}')
        untar_file(self._archive_filepath, self._install_local_path)

        # 3) possible post-untar script ?
        logger.debug(f'checking for installation script in {self._install_script_filename}')
        if self._install_script_filename is not None:
            install_script_filepath = path.join(self._install_local_path, self._install_script_filename)
            logger.info(f'applying installation script {install_script_filepath}')
            ret = os.system(install_script_filepath)

        # done
        self.set_status('installed')
        logger.info(f'done installing {self._name}')


def load_datasets_from_index(
        index_filepath: str,
        install_path: str,
        filter_patterns: Optional[List[str]] = None
) -> Dict[str, Dataset]:
    """
    Parses and load data from the index files, under yaml format.
    the yaml file looks like :
    ----
    robotcar_seasons_02:
      url: http://download.europe.naverlabs.com//kapture/robotcar_seasons_02.tar.gz
      sha256sum: 542ef47c00d5e387cfb0dcadb2459ae2fb17d59010cc51bae0c49403b4fa6a18
    ----

    :param index_filepath: input absolute path to index file
    :param install_path: input absolute path to install directory
    :param filter_patterns: optional input list of unix-like patterns (e.g. SiLDa*) to filter datasets
    :return: dict name -> [url, sub_path, sha256sum]
    """
    if not path.isfile(index_filepath):
        raise FileNotFoundError('no index file: do an update.')
    with open(index_filepath, 'rt') as f:
        datasets_yaml = yaml.safe_load(f)

    if len(datasets_yaml) == 0:
        raise FileNotFoundError('invalid index file: do an update.')

    nb_total = len(datasets_yaml)
    # filter only dataset matching filter_patterns
    if filter_patterns:
        datasets_yaml = {dataset_name: data_yaml
                         for dataset_name, data_yaml in datasets_yaml.items()
                         if any(fnmatch.fnmatch(dataset_name, pattern) for pattern in filter_patterns)}

    logger.debug(f'will prob status for {len(datasets_yaml)}/{nb_total} datasets ...')
    datasets = {}

    hide_progress_bar = True or logger.getEffectiveLevel() > logging.INFO
    for dataset_name, data_yaml in tqdm(datasets_yaml.items(), disable=hide_progress_bar):
        datasets[dataset_name] = Dataset(name=dataset_name,
                                         install_dirpath=install_path,
                                         archive_url=data_yaml['url'],
                                         archive_sha256sum=data_yaml['sha256sum'],
                                         install_script_filename=data_yaml.get('install_script'))

    return datasets


def kapture_download_dataset_cli():
    """
    Parse the kapture_download_dataset command line .
    """
    parser = argparse.ArgumentParser(description='download kapture datasets.')
    parser_verbosity = parser.add_mutually_exclusive_group()
    parser_verbosity = parser.add_mutually_exclusive_group()
    parser_verbosity.add_argument(
        '-v', '--verbose', nargs='?', default=logging.WARNING, const=logging.INFO,
        action=kapture.utils.logging.VerbosityParser,
        help='verbosity level (debug, info, warning, critical, ... or int value) [warning]')
    parser_verbosity.add_argument(
        '-q', '--silent', '--quiet', action='store_const', dest='verbose', const=logging.CRITICAL)
    parser.add_argument('--install_path', default=path.normpath(path.join(DEFAULT_DATASET_PATH)),
                        help=f'path to index files listing all datasets'
                             f' [{path.normpath(path.join(DEFAULT_DATASET_PATH))}]')
    subparsers = parser.add_subparsers(help='sub-command help')
    ####################################################################################################################
    # create the parser for the "update" command
    parser_update = subparsers.add_parser('update', help='update dataset index')
    parser_update.set_defaults(cmd='update')
    parser_update.add_argument('--repo', default=DEFAULT_REPOSITORY_URL,
                               help='url of the repository.')
    ####################################################################################################################
    parser_list = subparsers.add_parser('list', help='display dataset index')
    parser_list.set_defaults(cmd='list')
    parser_list.add_argument('dataset', nargs='*', default=[])
    parser_list.add_argument('--check', action='store_true', default=False,
                             help='Check the online version is reachable.')
    ####################################################################################################################
    parser_install = subparsers.add_parser('install', help='install dataset')
    parser_install.set_defaults(cmd='install')
    parser_install.add_argument('-f', '--force', action='store_true', default=False,
                                help='Force installation even if dataset has already been installed.')
    parser_install.add_argument('dataset', nargs='*', default=[],
                                help='name of the dataset to download. Can use unix-like wildcard.')
    ####################################################################################################################
    parser_download = subparsers.add_parser('download', help='dowload dataset, without installing it')
    parser_download.set_defaults(cmd='download')
    parser_download.add_argument('dataset', nargs='*', default=[],
                                 help='name of the dataset to download. Can use unix-like wildcard.')
    ####################################################################################################################
    args = parser.parse_args()

    logger.setLevel(args.verbose or logging.INFO)
    logger.debug(f'{sys.argv[0]} \\\n' + '  \\\n'.join(
        '--{:20} {:100}'.format(k, str(v))
        for k, v in vars(args).items()))

    try:
        index_filepath = path.join(args.install_path, INDEX_FILENAME)
        if not hasattr(args, 'cmd'):
            # check user did not forgot the command
            logger.critical(f'Choose command among [ {" | ".join(subparsers.choices)} ]')
            exit(-1)

        if args.cmd == 'update':
            logger.info(f'updating dataset list from {args.repo} ...')
            index_remote_url = path.join(args.repo, INDEX_FILENAME)
            logger.debug(f'retrieving index at {index_remote_url}')
            r = requests.get(index_remote_url, allow_redirects=True)
            if r.status_code != requests.codes.ok:
                raise ConnectionError(f'unable to grab {index_remote_url} (code:{r.status_code})')
            with open(index_filepath, 'wt') as f:
                f.write(r.text)
            datasets = load_datasets_from_index(index_filepath=index_filepath,
                                                install_path=args.install_path)
            logger.info(f'dataset index retrieved successfully: {len(datasets)} datasets')

        if args.cmd == 'list':
            logger.info(f'listing dataset {index_filepath} ...')
            datasets = load_datasets_from_index(index_filepath=index_filepath,
                                                install_path=args.install_path,
                                                filter_patterns=args.dataset)
            for name, dataset in datasets.items():
                print(f'{dataset.prob_status(check_online=args.check):^10}| {name:40} | {dataset.url}')

        if args.cmd == 'install':
            logger.info(f'installing dataset {args.dataset} ...')
            dataset_index = load_datasets_from_index(index_filepath=index_filepath,
                                                     install_path=args.install_path,
                                                     filter_patterns=args.dataset)
            if len(dataset_index) == 0:
                raise ValueError('no matching dataset')
            logger.info(f'{len(dataset_index)} dataset will be installed.')
            for name, dataset in dataset_index.items():
                logger.info(f'downloading {name} ...')
                dataset.install(force_overwrite=args.force)

        if args.cmd == 'download':
            logger.info(f'downloading dataset {args.dataset} ...')
            dataset_index = load_datasets_from_index(index_filepath=index_filepath,
                                                     install_path=args.install_path,
                                                     filter_patterns=args.dataset)
            if len(dataset_index) == 0:
                raise ValueError('no matching dataset')
            logger.info(f'{len(dataset_index)} dataset will be downloaded.')
            for name, dataset in dataset_index.items():
                logger.info(f'downloading {name} ...')
                dataset.download()

    except Exception as e:
        raise e
        logger.critical(e)


if __name__ == '__main__':
    kapture_download_dataset_cli()
