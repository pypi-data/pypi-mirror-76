import json
import string
import time

import jsonpyth

from . import proctree, procfile, procrec, utility


__all__ = 'CommandError', 'query', 'record'


class CommandError(Exception):
    """Generic command error."""


def query(procfile_list, output_file, delimiter=None, indent=None, query=None):
    readers = {k: v for k, v in procfile.registry.items() if k in procfile_list}
    tree = proctree.Tree(readers)
    result = tree.get_root()

    if query:
        try:
            result = jsonpyth.jsonpath(result, query, always_return_list=True)
        except jsonpyth.JsonPathSyntaxError as ex:
            raise CommandError(str(ex)) from ex

    if delimiter:
        result = delimiter.join(map(str, result))
    else:
        result = json.dumps(result, indent=indent, sort_keys=True, ensure_ascii=False)

    output_file.write(result)
    output_file.write('\n')


def record(
    procfile_list,
    database_file,
    interval,
    environment=None,
    query=None,
    recnum=None,
    reevalnum=None,
):
    readers = {k: v for k, v in procfile.registry.items() if k in procfile_list}
    tree = proctree.Tree(readers)

    count = 1
    query_tpl = string.Template(query)
    with procrec.SqliteStorage(database_file, procfile_list, utility.get_meta()) as store:
        while True:
            if (
                query_tpl.template
                and environment
                and (count == 1 or reevalnum and (count + 1) % reevalnum == 0)
            ):
                query = query_tpl.safe_substitute(utility.evaluate(environment))

            start = time.time()
            result = tree.get_root()
            if query:
                try:
                    result = jsonpyth.jsonpath(result, query, always_return_list=True)
                except jsonpyth.JsonPathSyntaxError as ex:
                    raise CommandError(str(ex)) from ex

            store.record(start, proctree.flatten(result, procfile_list))

            count += 1
            if recnum and count > recnum:
                break

            latency = time.time() - start
            time.sleep(max(0, interval - latency))
