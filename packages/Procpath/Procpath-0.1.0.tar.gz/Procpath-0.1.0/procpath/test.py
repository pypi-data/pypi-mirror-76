import io
import os
import re
import sys
import json
import time
import signal
import sqlite3
import datetime
import unittest
import tempfile
import multiprocessing
from contextlib import closing

from . import cli, command, procfile, procrec, proctree, utility


class TestUtility(unittest.TestCase):

    def test_evaluate(self):
        actual = utility.evaluate([
            ('A', 'date -I'),
            ('B', 'echo 42')
        ])
        self.assertEqual({'A': datetime.date.today().isoformat(), 'B': '42'}, actual)

    def test_get_meta(self):
        self.assertEqual(
            {'platform_node', 'platform_platform', 'page_size', 'clock_ticks'},
            utility.get_meta().keys(),
        )


class TestProctreeTree(unittest.TestCase):

    testee = None

    def setUp(self):
        self.testee = proctree.Tree(procfile.registry)

        node_list = get_chromium_node_list()
        proc_list = [{k: v for k, v in p.items() if k != 'children'} for p in node_list]
        proc_map = {proc['stat']['pid']: proc for proc in proc_list}
        proc_map[1] = {'stat': {'ppid': 0}}
        self.testee._read_process_dict = proc_map.__getitem__
        self.testee.get_pid_list = lambda: list(proc_map.keys()) + [os.getpid()]

    def test_get_pid_list(self):
        actual = proctree.Tree.get_pid_list()
        self.assertTrue(all(isinstance(v, int) for v in actual))
        self.assertEqual(actual, sorted(actual))

    def test_get_nodemap(self):
        expected = {p['stat']['pid']: p for p in get_chromium_node_list()}
        expected[1] = {'stat': {'ppid': 0}, 'children': [get_chromium_node_list()[0]]}
        actual = self.testee.get_nodemap()
        self.assertEqual(expected, actual)

    def test_get_root(self):
        expected = {'stat': {'ppid': 0}, 'children': [get_chromium_node_list()[0]]}
        actual = self.testee.get_root()
        self.assertEqual(expected, actual)

    def test_read_process_dict(self):
        testee = proctree.Tree(procfile.registry)
        actual = testee._read_process_dict(os.getpid())
        self.assertIn('stat', actual)
        self.assertIn('rss', actual['stat'])
        self.assertIn('cmdline', actual)
        self.assertIn('io', actual)
        self.assertIn('rchar', actual['io'])

        testee = proctree.Tree({'cmdline': procfile.registry['cmdline']})
        actual = testee._read_process_dict(os.getpid())
        self.assertEqual(['cmdline'], list(actual.keys()))

    def test_read_process_dict_permission_error(self):
        testee = proctree.Tree({'io': procfile.registry['io']})

        with self.assertLogs('procpath', 'WARNING') as ctx:
            actual = testee._read_process_dict(1)
        self.assertEqual(1, len(ctx.records))
        self.assertIn('Permission denied', ctx.records[0].message)

        self.assertEqual({'io': procfile.read_io.empty}, actual)  # @UndefinedVariable

    def test_get_root_do_not_skip_self(self):
        testee = proctree.Tree(procfile.registry, skip_self=False)
        proc_map = {
            1: {'stat': {'ppid': 0}},
            os.getpid(): {'stat': {'ppid': 1}}
        }
        testee._read_process_dict = proc_map.__getitem__
        testee.get_pid_list = lambda: list(proc_map.keys())

        expected = {'stat': {'ppid': 0}, 'children': [{'stat': {'ppid': 1}}]}
        self.assertEqual(expected, testee.get_root())

    def test_get_root_required_stat(self):
        testee = proctree.Tree({'io': procfile.registry['io']})
        with self.assertRaises(RuntimeError) as ctx:
            testee.get_root()
        self.assertEqual('stat file reader is required', str(ctx.exception))


class TestProctree(unittest.TestCase):

    def test_flatten(self):
        actual = proctree.flatten(get_chromium_node_list(), ['stat'])

        # trim for brevity
        for d in actual:
            for k in list(d.keys()):
                if k not in ('stat_pid', 'stat_rss', 'stat_state'):
                    d.pop(k)

        expected = [
            {'stat_pid': 18467, 'stat_rss': 53306, 'stat_state': 'S'},
            {'stat_pid': 18482, 'stat_rss': 13765, 'stat_state': 'S'},
            {'stat_pid': 18503, 'stat_rss': 27219, 'stat_state': 'S'},
            {'stat_pid': 18508, 'stat_rss': 20059, 'stat_state': 'S'},
            {'stat_pid': 18484, 'stat_rss': 3651, 'stat_state': 'S'},
            {'stat_pid': 18517, 'stat_rss': 4368, 'stat_state': 'S'},
            {'stat_pid': 18529, 'stat_rss': 19849, 'stat_state': 'S'},
            {'stat_pid': 18531, 'stat_rss': 26117, 'stat_state': 'S'},
            {'stat_pid': 18555, 'stat_rss': 63235, 'stat_state': 'S'},
            {'stat_pid': 18569, 'stat_rss': 18979, 'stat_state': 'S'},
            {'stat_pid': 18571, 'stat_rss': 8825, 'stat_state': 'S'},
            {'stat_pid': 18593, 'stat_rss': 22280, 'stat_state': 'S'},
            {'stat_pid': 18757, 'stat_rss': 12882, 'stat_state': 'S'},
            {'stat_pid': 18769, 'stat_rss': 54376, 'stat_state': 'S'},
            {'stat_pid': 18770, 'stat_rss': 31106, 'stat_state': 'S'},
            {'stat_pid': 18942, 'stat_rss': 27106, 'stat_state': 'S'},
        ]
        self.assertEqual(expected, actual)

    def test_flatten_single_value(self):
        actual = proctree.flatten(get_chromium_node_list(), ['cmdline'])

        renderer = {'cmdline': '/usr/lib/chromium-browser/chromium-browser --type=renderer ...'}
        expected = [
            {'cmdline': '/usr/lib/chromium-browser/chromium-browser ...'},
            {'cmdline': '/usr/lib/chromium-browser/chromium-browser --type=zygote'},
            {'cmdline': '/usr/lib/chromium-browser/chromium-browser --type=gpu-process ...'},
            {'cmdline': '/usr/lib/chromium-browser/chromium-browser --type=utility ...'},
            {'cmdline': '/usr/lib/chromium-browser/chromium-browser --type=zygote'},
            {'cmdline': '/usr/lib/chromium-browser/chromium-browser --type=broker'},
            renderer, renderer, renderer, renderer,
            {'cmdline': '/usr/lib/chromium-browser/chromium-browser --type=utility ...'},
            renderer, renderer, renderer, renderer, renderer,
        ]
        self.assertEqual(expected, actual)

    def test_attr_dict(self):
        ad = proctree.AttrDict({'a': 'b'})
        self.assertEqual('b', ad.a)


class TestProcrecSqliteStorage(unittest.TestCase):

    testeee = None

    def setUp(self):
        self.testee = procrec.SqliteStorage(':memory:', ['stat', 'cmdline'], {})

    def test_create_schema_all(self):
        testee = procrec.SqliteStorage(':memory:', ['stat', 'cmdline', 'io'], utility.get_meta())
        testee.create_schema()

        cursor = testee._conn.execute('''
            SELECT name
            FROM sqlite_master
            WHERE type = 'table' AND name NOT LIKE 'sqlite%'
        ''')
        self.assertEqual([('record',), ('meta',)], cursor.fetchall())

        cursor = testee._conn.execute('''
            SELECT sql
            FROM sqlite_master
            WHERE name  = 'record'
        ''')
        expected = '''
            CREATE TABLE record (
                record_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                ts        REAL NOT NULL,
                cmdline TEXT,
                io_rchar INTEGER,
                io_wchar INTEGER,
                io_syscr INTEGER,
                io_syscw INTEGER,
                io_read_bytes INTEGER,
                io_write_bytes INTEGER,
                io_cancelled_write_bytes INTEGER,
                stat_pid INTEGER,
                stat_comm TEXT,
                stat_state TEXT,
                stat_ppid INTEGER,
                stat_pgrp INTEGER,
                stat_session INTEGER,
                stat_tty_nr INTEGER,
                stat_tpgid INTEGER,
                stat_flags INTEGER,
                stat_minflt INTEGER,
                stat_cminflt INTEGER,
                stat_majflt INTEGER,
                stat_cmajflt INTEGER,
                stat_utime INTEGER,
                stat_stime INTEGER,
                stat_cutime INTEGER,
                stat_cstime INTEGER,
                stat_priority INTEGER,
                stat_nice INTEGER,
                stat_num_threads INTEGER,
                stat_itrealvalue INTEGER,
                stat_starttime INTEGER,
                stat_vsize INTEGER,
                stat_rss INTEGER
            )
        '''
        self.assertEqual(re.sub(r'\s+', '', expected), re.sub(r'\s+', '', cursor.fetchone()[0]))

        cursor = testee._conn.execute('''
            SELECT sql
            FROM sqlite_master
            WHERE name  = 'meta'
        ''')
        expected = '''
            CREATE TABLE meta (
                key   TEXT PRIMARY KEY NOT NULL,
                value TEXT NOT NULL
            )
        '''
        self.assertEqual(re.sub(r'\s+', '', expected), re.sub(r'\s+', '', cursor.fetchone()[0]))

        cursor = testee._conn.execute('SELECT * FROM meta')
        actual = dict(list(cursor))
        actual['page_size'] = int(actual['page_size'])
        actual['clock_ticks'] = int(actual['clock_ticks'])
        self.assertEqual(utility.get_meta(), actual)

    def test_create_schema_one(self):
        testee = procrec.SqliteStorage(':memory:', ['cmdline'], {})
        testee.create_schema()

        cursor = testee._conn.execute('''
            SELECT name
            FROM sqlite_master
            WHERE type = 'table' AND name NOT LIKE 'sqlite%'
        ''')
        self.assertEqual([('record',), ('meta',)], cursor.fetchall())

        cursor = testee._conn.execute('''
            SELECT sql
            FROM sqlite_master
            WHERE name  = 'record'
        ''')
        expected = '''
            CREATE TABLE record (
                record_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                ts        REAL NOT NULL,
                cmdline   TEXT
            )
        '''
        self.assertEqual(re.sub(r'\s+', '', expected), re.sub(r'\s+', '', cursor.fetchone()[0]))

    def test_record(self):
        ts = 1594483603.109486
        data = proctree.flatten(get_chromium_node_list(), self.testee._procfile_list)
        with self.testee:
            self.testee.record(ts, data)

            self.testee._conn.row_factory = sqlite3.Row
            cursor = self.testee._conn.execute('SELECT * FROM record')
            expected = [dict(d, record_id=i + 1, ts=ts) for i, d in enumerate(data)]
            self.assertEqual(expected, list(map(dict, cursor)))

        with self.assertRaises(sqlite3.ProgrammingError) as ctx:
            self.testee._conn.execute('SELECT * FROM record')
        self.assertEqual('Cannot operate on a closed database.', str(ctx.exception))

    def test_record_empty(self):
        ts = 1594483603.109486
        with self.testee:
            self.testee.record(ts, [])
            cursor = self.testee._conn.execute('SELECT * FROM record')
            self.assertEqual([], cursor.fetchall())


class TestCli(unittest.TestCase):

    def test_build_parser_record(self):
        parser = cli.build_parser()
        actual = vars(parser.parse_args([
            'record',
            '-f',
            'stat,cmdline',
            '-e',
            'N=\'docker inspect -f "{{.State.Pid}}" project_nginx_1\'',
            '-i',
            '10',
            '-r',
            '100',
            '-v'
            '25',
            '-d'
            'db.sqlite',
            '$..children[?(@.stat.pid == $N)]',
        ]))
        expected = {
            'command': 'record',
            'procfile_list': ['stat', 'cmdline'],
            'environment': [['N', '\'docker inspect -f "{{.State.Pid}}" project_nginx_1\'']],
            'interval': 10.0,
            'recnum': 100,
            'reevalnum': 25,
            'database_file': 'db.sqlite',
            'query': '$..children[?(@.stat.pid == $N)]',
        }
        self.assertEqual(expected, actual)

    def test_build_parser_query(self):
        parser = cli.build_parser()
        actual = vars(parser.parse_args([
            'query',
            '-f',
            'stat',
            '-d',
            ',',
            '$..children[?(@.stat.pid == 666)]..pid',
        ]))
        expected = {
            'command': 'query',
            'procfile_list': ['stat'],
            'delimiter': ',',
            'indent': None,
            'query': '$..children[?(@.stat.pid == 666)]..pid',
            'output_file': sys.stdout,
        }
        self.assertEqual(expected, actual)

        parser = cli.build_parser()
        actual = vars(parser.parse_args([
            'query',
            '-f',
            'stat',
            '-i',
            '2',
            '$..children[?(@.stat.pid == 666)]..pid',
        ]))
        expected = {
            'command': 'query',
            'procfile_list': ['stat'],
            'delimiter': None,
            'indent': 2,
            'query': '$..children[?(@.stat.pid == 666)]..pid',
            'output_file': sys.stdout,
        }
        self.assertEqual(expected, actual)


class TestProcfile(unittest.TestCase):

    def test_read_stat(self):
        content = (
            b'32222 (python3.7) R 29884 337 337 0 -1 4194304 3765 0 1 0 19 3 0 '
            b'0 20 0 2 0 89851404 150605824 5255 18446744073709551615 4194304 '
            b'8590100 140727866261328 0 0 0 4 553652224 2 0 0 0 17 2 0 0 1 0 0 '
            b'10689968 11363916 15265792 140727866270452 140727866270792 '
            b'140727866270792 140727866273727 0\n'
        )
        expected = {
            'pid': 32222,
            'comm': 'python3.7',
            'state': 'R',
            'ppid': 29884,
            'pgrp': 337,
            'session': 337,
            'tty_nr': 0,
            'tpgid': -1,
            'flags': 4194304,
            'minflt': 3765,
            'cminflt': 0,
            'majflt': 1,
            'cmajflt': 0,
            'utime': 19,
            'stime': 3,
            'cutime': 0,
            'cstime': 0,
            'priority': 20,
            'nice': 0,
            'num_threads': 2,
            'itrealvalue': 0,
            'starttime': 89851404,
            'vsize': 150605824,
            'rss': 5255
        }
        actual = procfile.read_stat(content)
        self.assertEqual(expected, actual)

    def test_read_cmdline(self):
        content = b'python3.7\x00-Wa\x00-u\x00'
        expected = 'python3.7 -Wa -u'
        actual = procfile.read_cmdline(content)
        self.assertEqual(expected, actual)

    def test_read_io(self):
        content = (
            b'rchar: 2274068\nwchar: 15681\nsyscr: 377\nsyscw: 10\nread_bytes: '
            b'0\nwrite_bytes: 20480\ncancelled_write_bytes: 0\n'
        )
        expected = {
            'rchar': 2274068,
            'wchar': 15681,
            'syscr': 377,
            'syscw': 10,
            'read_bytes': 0,
            'write_bytes': 20480,
            'cancelled_write_bytes': 0
        }
        actual = procfile.read_io(content)
        self.assertEqual(expected, actual)


class TestCommand(unittest.TestCase):

    def test_query_query_node_list_json_output(self):
        output_file = io.StringIO()
        command.query(
            procfile_list=['stat'],
            output_file=output_file,
            indent=2,
            query='$..children[?(@.stat.pid == {})]'.format(os.getppid()),
        )
        data = json.loads(output_file.getvalue())
        self.assertEqual(1, len(data))

    def test_query_no_query_root_output(self):
        output_file = io.StringIO()
        command.query(
            procfile_list=['stat'],
            output_file=output_file,
        )
        root = json.loads(output_file.getvalue())
        self.assertEqual(1, root['stat']['pid'])

    def test_query_delimited(self):
        output_file = io.StringIO()
        command.query(
            procfile_list=['stat'],
            output_file=output_file,
            delimiter=',',
            query='$..children[?(@.stat.pid == {})]..pid'.format(os.getppid()),
        )
        pids = output_file.getvalue().split(',')
        self.assertGreaterEqual(len(pids), 1)
        self.assertEqual(os.getppid(), int(pids[0]))

    def test_query_syntax_error(self):
        with self.assertRaises(command.CommandError):
            command.query(procfile_list=['stat'], output_file=io.StringIO(), query='$!#')

    def test_record_query(self):
        with tempfile.NamedTemporaryFile() as f:
            start = time.time()
            command.record(
                procfile_list=['stat'],
                database_file=f.name,
                interval=1,
                recnum=1,
                query='$..children[?(@.stat.pid == {})]'.format(os.getppid()),
            )
            with closing(sqlite3.connect(f.name)) as conn:
                conn.row_factory = sqlite3.Row

                cursor = conn.execute('SELECT * FROM record')
                rows = list(map(dict, cursor))
                self.assertGreaterEqual(len(rows), 1)

        actual = rows[0]
        self.assertEqual(1, actual.pop('record_id'))
        self.assertAlmostEqual(start, actual.pop('ts'), delta=0.1)

        self.assertEqual(os.getppid(), actual['stat_pid'])
        self.assertEqual(
            list(procfile.read_stat.empty.keys()),  # @UndefinedVariable
            [k.replace('stat_', '') for k in actual.keys()],
        )

    def test_record_all(self):
        with tempfile.NamedTemporaryFile() as f:
            start = time.time()
            command.record(
                procfile_list=['stat', 'cmdline'],
                database_file=f.name,
                interval=1,
                recnum=1,
            )
            with closing(sqlite3.connect(f.name)) as conn:
                conn.row_factory = sqlite3.Row

                cursor = conn.execute('SELECT * FROM record')
                rows = list(map(dict, cursor))
                self.assertGreaterEqual(len(rows), 1)

        root = rows[0]
        self.assertEqual(1, root.pop('record_id'))
        self.assertAlmostEqual(start, root.pop('ts'), delta=0.1)

        self.assertEqual(1, root['stat_pid'])
        self.assertEqual(
            ['cmdline'] + list(procfile.read_stat.empty.keys()),  # @UndefinedVariable
            [k.replace('stat_', '') for k in root.keys()],
        )

    @classmethod
    def record_forever(cls, database_file, pid):
        try:
            command.record(
                procfile_list=['stat'],
                database_file=database_file,
                interval=0.1,
                query=f'$..children[?(@.stat.pid == {pid})]',
            )
        except KeyboardInterrupt:
            pass

    def test_record_forever(self):
        with tempfile.NamedTemporaryFile() as f:
            p = multiprocessing.Process(target=self.record_forever, args=(f.name, os.getppid()))
            start = time.time()
            p.start()

            time.sleep(0.55)
            os.kill(p.pid, signal.SIGINT)
            p.join()

            with closing(sqlite3.connect(f.name)) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.execute('SELECT * FROM record')
                rows = list(map(dict, cursor))

        self.assertGreaterEqual(sum(1 for r in rows if r['stat_pid'] == os.getppid()), 5)
        for i, row in enumerate(rows):
            self.assertEqual(i + 1, row.pop('record_id'))
            self.assertAlmostEqual(start, row.pop('ts'), delta=1)
            self.assertEqual(
                list(procfile.read_stat.empty.keys()),  # @UndefinedVariable
                [k.replace('stat_', '') for k in row.keys()],
            )

    def test_record_n_times(self):
        with tempfile.NamedTemporaryFile() as f:
            start = time.time()
            command.record(
                procfile_list=['stat'],
                database_file=f.name,
                interval=0.01,
                recnum=4,
                query='$..children[?(@.stat.pid == {})]'.format(os.getppid()),
            )
            with closing(sqlite3.connect(f.name)) as conn:
                conn.row_factory = sqlite3.Row

                cursor = conn.execute('SELECT * FROM record')
                rows = list(map(dict, cursor))

        self.assertEqual(4, sum(1 for r in rows if r['stat_pid'] == os.getppid()))
        for i, row in enumerate(rows):
            self.assertEqual(i + 1, row.pop('record_id'))
            self.assertAlmostEqual(start, row.pop('ts'), delta=1)
            self.assertEqual(
                list(procfile.read_stat.empty.keys()),  # @UndefinedVariable
                [k.replace('stat_', '') for k in row.keys()],
            )

    def test_record_environment(self):
        with tempfile.NamedTemporaryFile() as f:
            with tempfile.NamedTemporaryFile() as f_log:
                start = time.time()
                command.record(
                    procfile_list=['stat'],
                    database_file=f.name,
                    interval=0.01,
                    recnum=4,
                    reevalnum=2,
                    environment=[['P', 'echo {} | tee -a {}'.format(os.getppid(), f_log.name)]],
                    query='$..children[?(@.stat.pid == $P)]',
                )
                self.assertEqual(''.join(['{}\n'.format(os.getppid())] * 2).encode(), f_log.read())

                with closing(sqlite3.connect(f.name)) as conn:
                    conn.row_factory = sqlite3.Row

                    cursor = conn.execute('SELECT * FROM record')
                    rows = list(map(dict, cursor))

        self.assertEqual(4, sum(1 for r in rows if r['stat_pid'] == os.getppid()))
        for i, row in enumerate(rows):
            self.assertEqual(i + 1, row.pop('record_id'))
            self.assertAlmostEqual(start, row.pop('ts'), delta=1)
            self.assertEqual(
                list(procfile.read_stat.empty.keys()),  # @UndefinedVariable
                [k.replace('stat_', '') for k in row.keys()],
            )

    def test_record_syntax_error(self):
        with self.assertRaises(command.CommandError):
            command.record(
                procfile_list=['stat'], database_file=':memory:', interval=1, query='$!#'
            )


def get_chromium_node_list():
    """
    Get procpath search sample of Chromium browser process tree.

    ::

        chromium-browser ...
        ├─ chromium-browser --type=utility ...
        ├─ chromium-browser --type=gpu-process ...
        │  └─ chromium-browser --type=broker
        └─ chromium-browser --type=zygote
           └─ chromium-browser --type=zygote
              ├─ chromium-browser --type=renderer ...
              ├─ chromium-browser --type=renderer ...
              ├─ chromium-browser --type=renderer ...
              ├─ chromium-browser --type=renderer ...
              ├─ chromium-browser --type=utility ...
              ├─ chromium-browser --type=renderer ...
              ├─ chromium-browser --type=renderer ...
              ├─ chromium-browser --type=renderer ...
              ├─ chromium-browser --type=renderer ...
              └─ chromium-browser --type=renderer ...

    """

    pid_18467 = {
        'stat': {
            'pid': 18467,
            'comm': 'chromium-browse',
            'state': 'S',
            'ppid': 1,
            'pgrp': 337,
            'session': 337,
            'tty_nr': 0,
            'tpgid': -1,
            'flags': 4194560,
            'minflt': 51931,
            'cminflt': 24741,
            'majflt': 721,
            'cmajflt': 13,
            'utime': 455,
            'stime': 123,
            'cutime': 16,
            'cstime': 17,
            'priority': 20,
            'nice': 0,
            'num_threads': 40,
            'itrealvalue': 0,
            'starttime': 62870630,
            'vsize': 2981761024,
            'rss': 53306,
        },
        'cmdline': '/usr/lib/chromium-browser/chromium-browser ...',
    }
    pid_18482 = {
        'stat': {
            'pid': 18482,
            'comm': 'chromium-browse',
            'state': 'S',
            'ppid': 18467,
            'pgrp': 337,
            'session': 337,
            'tty_nr': 0,
            'tpgid': -1,
            'flags': 4194560,
            'minflt': 3572,
            'cminflt': 0,
            'majflt': 49,
            'cmajflt': 0,
            'utime': 3,
            'stime': 2,
            'cutime': 0,
            'cstime': 0,
            'priority': 20,
            'nice': 0,
            'num_threads': 1,
            'itrealvalue': 0,
            'starttime': 62870663,
            'vsize': 460001280,
            'rss': 13765,
        },
        'cmdline': '/usr/lib/chromium-browser/chromium-browser --type=zygote',
    }
    pid_18484 = {
        'stat': {
            'pid': 18484,
            'comm': 'chromium-browse',
            'state': 'S',
            'ppid': 18482,
            'pgrp': 337,
            'session': 337,
            'tty_nr': 0,
            'tpgid': -1,
            'flags': 4194624,
            'minflt': 278,
            'cminflt': 4862,
            'majflt': 0,
            'cmajflt': 15,
            'utime': 0,
            'stime': 1,
            'cutime': 27,
            'cstime': 4,
            'priority': 20,
            'nice': 0,
            'num_threads': 1,
            'itrealvalue': 0,
            'starttime': 62870674,
            'vsize': 460001280,
            'rss': 3651,
        },
        'cmdline': '/usr/lib/chromium-browser/chromium-browser --type=zygote',
    }
    pid_18529 = {
        'stat': {
            'pid': 18529,
            'comm': 'chromium-browse',
            'state': 'S',
            'ppid': 18484,
            'pgrp': 337,
            'session': 337,
            'tty_nr': 0,
            'tpgid': -1,
            'flags': 1077936192,
            'minflt': 3285,
            'cminflt': 0,
            'majflt': 78,
            'cmajflt': 0,
            'utime': 16,
            'stime': 3,
            'cutime': 0,
            'cstime': 0,
            'priority': 20,
            'nice': 0,
            'num_threads': 12,
            'itrealvalue': 0,
            'starttime': 62870743,
            'vsize': 5411180544,
            'rss': 19849,
        },
        'cmdline': '/usr/lib/chromium-browser/chromium-browser --type=renderer ...',
    }
    pid_18531 = {
        'stat': {
            'pid': 18531,
            'comm': 'chromium-browse',
            'state': 'S',
            'ppid': 18484,
            'pgrp': 337,
            'session': 337,
            'tty_nr': 0,
            'tpgid': -1,
            'flags': 1077936192,
            'minflt': 18231,
            'cminflt': 0,
            'majflt': 183,
            'cmajflt': 0,
            'utime': 118,
            'stime': 18,
            'cutime': 0,
            'cstime': 0,
            'priority': 20,
            'nice': 0,
            'num_threads': 12,
            'itrealvalue': 0,
            'starttime': 62870744,
            'vsize': 16164175872,
            'rss': 26117,
        },
        'cmdline': '/usr/lib/chromium-browser/chromium-browser --type=renderer ...',
    }
    pid_18555 = {
        'stat': {
            'pid': 18555,
            'comm': 'chromium-browse',
            'state': 'S',
            'ppid': 18484,
            'pgrp': 337,
            'session': 337,
            'tty_nr': 0,
            'tpgid': -1,
            'flags': 1077936192,
            'minflt': 62472,
            'cminflt': 0,
            'majflt': 136,
            'cmajflt': 0,
            'utime': 1166,
            'stime': 59,
            'cutime': 0,
            'cstime': 0,
            'priority': 20,
            'nice': 0,
            'num_threads': 14,
            'itrealvalue': 0,
            'starttime': 62870769,
            'vsize': 14124892160,
            'rss': 63235,
        },
        'cmdline': '/usr/lib/chromium-browser/chromium-browser --type=renderer ...',
    }
    pid_18569 = {
        'stat': {
            'pid': 18569,
            'comm': 'chromium-browse',
            'state': 'S',
            'ppid': 18484,
            'pgrp': 337,
            'session': 337,
            'tty_nr': 0,
            'tpgid': -1,
            'flags': 1077936192,
            'minflt': 2695,
            'cminflt': 0,
            'majflt': 8,
            'cmajflt': 0,
            'utime': 7,
            'stime': 3,
            'cutime': 0,
            'cstime': 0,
            'priority': 20,
            'nice': 0,
            'num_threads': 11,
            'itrealvalue': 0,
            'starttime': 62870779,
            'vsize': 5407739904,
            'rss': 18979,
        },
        'cmdline': '/usr/lib/chromium-browser/chromium-browser --type=renderer ...',
    }
    pid_18571 = {
        'stat': {
            'pid': 18571,
            'comm': 'chromium-browse',
            'state': 'S',
            'ppid': 18484,
            'pgrp': 337,
            'session': 337,
            'tty_nr': 0,
            'tpgid': -1,
            'flags': 1077936192,
            'minflt': 930,
            'cminflt': 0,
            'majflt': 20,
            'cmajflt': 0,
            'utime': 6,
            'stime': 3,
            'cutime': 0,
            'cstime': 0,
            'priority': 20,
            'nice': 0,
            'num_threads': 5,
            'itrealvalue': 0,
            'starttime': 62870781,
            'vsize': 5057503232,
            'rss': 8825,
        },
        'cmdline': '/usr/lib/chromium-browser/chromium-browser --type=utility ...',
    }
    pid_18593 = {
        'stat': {
            'pid': 18593,
            'comm': 'chromium-browse',
            'state': 'S',
            'ppid': 18484,
            'pgrp': 337,
            'session': 337,
            'tty_nr': 0,
            'tpgid': -1,
            'flags': 1077936192,
            'minflt': 12212,
            'cminflt': 0,
            'majflt': 2,
            'cmajflt': 0,
            'utime': 171,
            'stime': 11,
            'cutime': 0,
            'cstime': 0,
            'priority': 20,
            'nice': 0,
            'num_threads': 12,
            'itrealvalue': 0,
            'starttime': 62870786,
            'vsize': 5419442176,
            'rss': 22280,
        },
        'cmdline': '/usr/lib/chromium-browser/chromium-browser --type=renderer ...',
    }
    pid_18757 = {
        'stat': {
            'pid': 18757,
            'comm': 'chromium-browse',
            'state': 'S',
            'ppid': 18484,
            'pgrp': 337,
            'session': 337,
            'tty_nr': 0,
            'tpgid': -1,
            'flags': 1077936192,
            'minflt': 1624,
            'cminflt': 0,
            'majflt': 0,
            'cmajflt': 0,
            'utime': 2,
            'stime': 0,
            'cutime': 0,
            'cstime': 0,
            'priority': 20,
            'nice': 0,
            'num_threads': 11,
            'itrealvalue': 0,
            'starttime': 62871186,
            'vsize': 5389012992,
            'rss': 12882
        },
        'cmdline': '/usr/lib/chromium-browser/chromium-browser --type=renderer ...'
    }
    pid_18769 = {
        'stat': {
            'pid': 18769,
            'comm': 'chromium-browse',
            'state': 'S',
            'ppid': 18484,
            'pgrp': 337,
            'session': 337,
            'tty_nr': 0,
            'tpgid': -1,
            'flags': 1077936192,
            'minflt': 78483,
            'cminflt': 0,
            'majflt': 3,
            'cmajflt': 0,
            'utime': 906,
            'stime': 34,
            'cutime': 0,
            'cstime': 0,
            'priority': 20,
            'nice': 0,
            'num_threads': 12,
            'itrealvalue': 0,
            'starttime': 62871227,
            'vsize': 5497511936,
            'rss': 54376,
        },
        'cmdline': '/usr/lib/chromium-browser/chromium-browser --type=renderer ...',
    }
    pid_18770 = {
        'stat': {
            'pid': 18770,
            'comm': 'chromium-browse',
            'state': 'S',
            'ppid': 18484,
            'pgrp': 337,
            'session': 337,
            'tty_nr': 0,
            'tpgid': -1,
            'flags': 1077936192,
            'minflt': 24759,
            'cminflt': 0,
            'majflt': 2,
            'cmajflt': 0,
            'utime': 260,
            'stime': 15,
            'cutime': 0,
            'cstime': 0,
            'priority': 20,
            'nice': 0,
            'num_threads': 12,
            'itrealvalue': 0,
            'starttime': 62871228,
            'vsize': 5438599168,
            'rss': 31106,
        },
        'cmdline': '/usr/lib/chromium-browser/chromium-browser --type=renderer ...',
    }
    pid_18942 = {
        'stat': {
            'pid': 18942,
            'comm': 'chromium-browse',
            'state': 'S',
            'ppid': 18484,
            'pgrp': 337,
            'session': 337,
            'tty_nr': 0,
            'tpgid': -1,
            'flags': 1077936192,
            'minflt': 12989,
            'cminflt': 0,
            'majflt': 16,
            'cmajflt': 0,
            'utime': 77,
            'stime': 5,
            'cutime': 0,
            'cstime': 0,
            'priority': 20,
            'nice': 0,
            'num_threads': 12,
            'itrealvalue': 0,
            'starttime': 62871410,
            'vsize': 5436309504,
            'rss': 27106,
        },
        'cmdline': '/usr/lib/chromium-browser/chromium-browser --type=renderer ...',
    }
    pid_18503 = {
        'stat': {
            'pid': 18503,
            'comm': 'chromium-browse',
            'state': 'S',
            'ppid': 18467,
            'pgrp': 337,
            'session': 337,
            'tty_nr': 0,
            'tpgid': -1,
            'flags': 4194304,
            'minflt': 14361,
            'cminflt': 0,
            'majflt': 46,
            'cmajflt': 0,
            'utime': 112,
            'stime': 21,
            'cutime': 0,
            'cstime': 0,
            'priority': 20,
            'nice': 0,
            'num_threads': 6,
            'itrealvalue': 0,
            'starttime': 62870711,
            'vsize': 877408256,
            'rss': 27219,
        },
        'cmdline': '/usr/lib/chromium-browser/chromium-browser --type=gpu-process ...',
    }
    pid_18517 = {
        'stat': {
            'pid': 18517,
            'comm': 'chromium-browse',
            'state': 'S',
            'ppid': 18503,
            'pgrp': 337,
            'session': 337,
            'tty_nr': 0,
            'tpgid': -1,
            'flags': 4194368,
            'minflt': 86,
            'cminflt': 0,
            'majflt': 0,
            'cmajflt': 0,
            'utime': 0,
            'stime': 0,
            'cutime': 0,
            'cstime': 0,
            'priority': 20,
            'nice': 0,
            'num_threads': 1,
            'itrealvalue': 0,
            'starttime': 62870723,
            'vsize': 524230656,
            'rss': 4368,
        },
        'cmdline': '/usr/lib/chromium-browser/chromium-browser --type=broker',
    }
    pid_18508 = {
        'stat': {
            'pid': 18508,
            'comm': 'chromium-browse',
            'state': 'S',
            'ppid': 18467,
            'pgrp': 337,
            'session': 337,
            'tty_nr': 0,
            'tpgid': -1,
            'flags': 1077936128,
            'minflt': 9993,
            'cminflt': 0,
            'majflt': 55,
            'cmajflt': 0,
            'utime': 151,
            'stime': 47,
            'cutime': 0,
            'cstime': 0,
            'priority': 20,
            'nice': 0,
            'num_threads': 12,
            'itrealvalue': 0,
            'starttime': 62870714,
            'vsize': 1302757376,
            'rss': 20059,
        },
        'cmdline': '/usr/lib/chromium-browser/chromium-browser --type=utility ...',
    }

    return [
        {
            **pid_18467,
            'children': [
                {
                    **pid_18482,
                    'children': [
                        {
                            **pid_18484,
                            'children': [
                                pid_18529, pid_18531, pid_18555, pid_18569, pid_18571,
                                pid_18593, pid_18757, pid_18769, pid_18770, pid_18942,
                            ]
                        }
                    ]
                },
                {
                    **pid_18503,
                    'children': [pid_18517]
                },
                pid_18508
            ]
        },
        {
            **pid_18482,
            'children': [
                {
                    **pid_18484,
                    'children': [
                        pid_18529, pid_18531, pid_18555, pid_18569, pid_18571,
                        pid_18593, pid_18757, pid_18769, pid_18770, pid_18942,
                    ]
                }
            ]
        },
        {
            **pid_18503,
            'children': [pid_18517]
        },
        pid_18508,
        {
            **pid_18484,
            'children': [
                pid_18529, pid_18531, pid_18555, pid_18569, pid_18571,
                pid_18593, pid_18757, pid_18769, pid_18770, pid_18942,
            ]
        },
        pid_18517,
        pid_18529, pid_18531, pid_18555, pid_18569, pid_18571,
        pid_18593, pid_18757, pid_18769, pid_18770, pid_18942,
    ]
