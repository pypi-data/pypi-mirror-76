# Copyright 2012-2020 CERN for the benefit of the ATLAS collaboration.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Authors:
# - Aristeidis Fkiaras <aristeidis.fkiaras@cern.ch>, 2019 - 2020
#
# PY3K COMPATIBLE

import importlib

from rucio.common import config
from rucio.common.exception import PolicyPackageNotFound
from rucio.db.sqla.session import read_session

# from . import hardcoded as hardcoded_handler

try:
    from ConfigParser import NoOptionError, NoSectionError
except ImportError:
    from configparser import NoOptionError, NoSectionError

HARDCODED_METADATA_HANDLER_MODULE = "rucio.core.did_meta_plugins.did_column_meta.DidColumnMeta"
FALLBACK_METADATA_HANDLER_MODULE = "rucio.core.did_meta_plugins.json_meta.JSONDidMeta"

if config.config_has_section('metadata'):
    try:
        METADATA_HANDLER_MODULES = config.config_get('metadata', 'plugins')
    except (NoOptionError, NoSectionError) as error:
        METADATA_HANDLER_MODULES = FALLBACK_METADATA_HANDLER_MODULE
else:
    METADATA_HANDLER_MODULES = FALLBACK_METADATA_HANDLER_MODULE

META_MODULE_PATHS = [HARDCODED_METADATA_HANDLER_MODULE] + METADATA_HANDLER_MODULES.split(",")

METADATA_HANDLERS = []
for meta_module_path in META_MODULE_PATHS:
    try:
        base_module = ".".join(meta_module_path.split(".")[:-1])
        base_class = meta_module_path.split(".")[-1]
        meta_handler_module = getattr(importlib.import_module(base_module), base_class)()
        METADATA_HANDLERS.append(meta_handler_module)
    except (ImportError) as error:
        raise PolicyPackageNotFound('Module ' + meta_module_path + ' not found')


def get_metadata(scope, name, plugin="DID_COLUMN", session=None):
    """
    Gets the metadata for given did.
    This method has been adapted to bring the metadata from diffrent metadata storages. (HARDCODED or GENERIC for now)
    If the filter is "ALL", will return the metadata from all available metadata storages. Else filter can be used to
    only return the metadata of a particular storage.

    :param scope: The scope of the did.
    :param name: The name of the did.
    :param filter: (optional) Filter down to specific metadata storages [ALL|HARDCODED|GENERIC]

    :returns: List of metadata for did.
    """
    if plugin == "ALL":
        all_meta = {}

        for meta_handler in METADATA_HANDLERS:
            metadata = meta_handler.get_metadata(scope, name, session=session)
            all_meta.update(metadata)

        return all_meta
    else:
        for meta_handler in METADATA_HANDLERS:
            if meta_handler.get_plugin_name().lower() == plugin.lower():
                return meta_handler.get_metadata(scope, name, session=session)

        raise NotImplementedError('Metadata plugin %s is not enabled on the server.' % plugin)


def set_metadata(scope, name, key, value, recursive=False, session=None):
    """
    Sets the metadata for a given did.

    To decide which metadata store to use, it is checking the configuration of the server and wether the key exists
    as hardcoded.

    :param scope: The scope of the did.
    :param name: The name of the did.
    :param key: Key of the metadata.
    :param value: Value of the metadata.
    :param did: (Optional) The data identifier info.
    :param recursive: (Optional) Option to propagate the metadata change to content.
    :param session: (Optional)  The database session in use.
    """
    for meta_handler in METADATA_HANDLERS:
        if meta_handler.manages_key(key):
            meta_handler.set_metadata(scope, name, key, value, recursive, session=session)
            break


def delete_metadata(scope, name, key, session=None):
    """
    Deletes the metadata stored for the given key. Currently only works for JSON metadata store

    :param scope: The scope of the did.
    :param name: The name of the did.
    :param key: Key of the metadata.
    """
    for meta_handler in METADATA_HANDLERS:
        if meta_handler.manages_key(key):
            meta_handler.delete_metadata(scope, name, key, session=session)


@read_session
def list_dids(scope=None, filters=None, type='collection', ignore_case=False, limit=None,
              offset=None, long=False, recursive=False, session=None):
    """
    List dids according to metadata.
    Either all of the metadata in the query should belong in the hardcoded ones, or none at all.
    A mixture of hardcoded and generic metadata is not supported at the moment.

    :param scope: the scope name.
    :param filters: dictionary of attributes by which the results should be filtered.
    :param type: the type of the did: all(container, dataset, file), collection(dataset or container), dataset, container, file.
    :param ignore_case: ignore case distinctions.
    :param limit: limit number.
    :param offset: offset number.
    :param long: Long format option to display more information for each DID.
    :param recursive: Recursively list DIDs content.
    :param session: The database session in use.

    :returns: List of dids.
    """
    meta_handler_to_use = None

    # Ensure that a single handler manages all the keys of the query
    for key in filters:
        if key == 'name':
            continue
        if meta_handler_to_use is None:
            for meta_handler in METADATA_HANDLERS:
                if meta_handler.manages_key(key):
                    meta_handler_to_use = meta_handler
                    break
        else:
            if not meta_handler_to_use.manages_key(key):
                # Mix case, difficult, slow and will probably blow up memory
                raise NotImplementedError('Filter keys used do not all belong on the same metadata plugin.')

    if meta_handler_to_use:
        return meta_handler_to_use.list_dids(scope=scope, filters=filters, type=type,
                                             ignore_case=ignore_case, limit=limit,
                                             offset=offset, long=long, recursive=recursive, session=session)
    else:
        raise NotImplementedError('There is no metadata plugin that manages the filter you used.')
