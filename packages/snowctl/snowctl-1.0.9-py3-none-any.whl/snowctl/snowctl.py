import sys
import signal
import logging
import pkg_resources
from snowctl.utils import *
from snowctl.config import Config
from snowctl.logger import logger_options
from snowctl.connect import snowflake_connect
from snowctl.arguments import arg_parser, cmd_parser

VERSION = pkg_resources.require('snowctl')[0].version
LOG = logging.getLogger(__name__)
BANNER = """\
 __        __        __  ___      
/__` |\ | /  \ |  | /  `  |  |    
.__/ | \| \__/ |/\| \__,  |  |___ 
                                 
"""

def print_usage():
    print(
    '''
    snowctl usage:
        copy [-d, --derive] [-f, --filter] [-r, --rename] - copy view(s) to other schemas
             [-d] - create new view by selecting all cols from source view instead of copying ddl
             [-f] - filter out columns of target view when copying
             [-r] - rename target views
        use <db|schema|warehouse> <name>
        list <filter> - list views in current context with an optional filter
        peek <view> - show first row of data from the view
        sql <query> - execute sql query
        exit / ctrl+C
    '''
    )


class Controller:
    def __init__(self, conn, engine, safe):
        self.connection = conn
        self.engine = engine
        self.safe_mode = safe
        self.run = True
        self.prompt = 'snowctl> '
        self.curr_db = None
        self.curr_schema = None

    def run_console(self):
        self.listen_signals()
        print_usage()
        try:
            while self.run:
                self.get_prompt()
                print(self.prompt, end='', flush=True)
                user_input = sys.stdin.readline()
                cmd = parser(user_input)
                if cmd != None:
                    self.operation(cmd)  
        except Exception as e:
            LOG.error(e)
        finally:
            self.exit_console()

    def operation(self, cmd: list):
        try:
            if cmd[0] == 'help':
                print_usage()
            elif cmd[0] == 'copy':
                args = cmd_parser(cmd[1:])
                if args != None:
                    self.copy_views(derive=args.derive, filter_cols=args.filter, rename=args.rename)
            elif cmd[0] == 'list':
                self.list_views(cmd)
            elif cmd[0] == 'peek':
                self.peek(cmd[1])
            elif cmd[0] == 'use':
                self.use(cmd)
            elif cmd[0] == 'sql':
                self.user_query(cmd)
            elif cmd[0] == 'exit':
                self.exit_console()
        except Exception as e:
            print(f'Execution error: {e}')

    def use(self, cmd: list):
        results = self.connection.execute(f"use {cmd[1]} {cmd[2]}")
        response = results.fetchone()
        print(response[0])        

    def user_query(self, cmd: list):
        cmd.pop(0)
        query = ' '.join(cmd)
        response = self.execute_query(query)
        for row in response:
            print(row)

    def peek(self, view):
        row = self.execute_query(f'select * from {self.curr_db}.{self.curr_schema}.{view} limit 1')
        print(row)

    def list_views(self, cmd):
        filter = False
        if len(cmd) == 2:
            filter = cmd[1]
        rows = self.execute_query('show views')
        for i, row in enumerate(rows):
            if filter:
                if filter.lower() in row[1].lower():
                    print(f'{i} - {row[1]}')
            else:
                print(f'{i} - {row[1]}')

    def copy_views(self, derive=False, filter_cols=False, rename=False):
        from snowctl.copy import Copycat
        cp = Copycat(self.connection, self.engine, self.safe_mode)
        cp.copy(self.curr_db, self.curr_schema, derive=derive, filter_cols=filter_cols, rename=rename)

    def execute_query(self, query):
        LOG.debug(f'executing:\n{query}')
        ret = []
        results = self.connection.execute(query)
        while True:
            row = results.fetchone()
            if not row:
                break
            ret.append(row)
        return ret

    def get_prompt(self):
        prompt = ''
        response = self.execute_query('select current_warehouse(), current_database(), current_schema()')
        wh = response[0][0]
        db = response[0][1]
        schema = response[0][2]
        if wh is not None:
            prompt += f'{wh}:'
        if db is not None:
            prompt += f'{db}:'
            self.curr_db = db
        if schema is not None:
            prompt += f'{schema}:'
            self.curr_schema = schema
        if not len(prompt):
            self.prompt = 'snowctl> '
        else:
            prompt = prompt[:-1]
            self.prompt = f'{prompt}> '.lower()

    def exit_console(self):
        print('closing connections...')
        try:
            self.connection.close()
            self.engine.dispose()
        finally:
            sys.exit('exit')

    def listen_signals(self):
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

    def signal_handler(self, signum, frame):
        if signum == signal.SIGINT or signum == signal.SIGTERM:
            self.exit_console()


def main():
    args = arg_parser()
    conf = Config()
    if args.echo:
        conf.echo_config()
    elif args.version:
        print(VERSION)
    else:
        conf.write_config(args.configuration)
        if args.configuration:
            sys.exit()
        logger_options(args.debug)
        print(BANNER)
        conn, engine = snowflake_connect(conf.read_config())
        try:
            c = Controller(conn, engine, args.safe)
            c.run_console()
        finally:
            conn.close()
            engine.dispose()


if __name__ == '__main__':
    main()
