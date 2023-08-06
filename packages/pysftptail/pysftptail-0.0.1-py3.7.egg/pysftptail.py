import os
import logging
from contextlib import closing
import paramiko
import click
from colorama import init, Style

init()

logging.basicConfig(level=logging.INFO, format=Style.DIM + '> %(asctime)s [%(levelname)s]:%(name)s - %(message)s' + Style.RESET_ALL)

def tail(host: str, username: str, password: str, lines: int, follow: bool, file_path: str, port:int = 22) -> str:
    """[summary]

    Args:
        host (str): [sftp server uri]
        username (str): [username login credential]
        password (str): [user password]
        number (int): [number of line to be printed from the end of the file]
        follow (bool): [flag to decide if the file will be watched, like tail -f]
        file_path (str): [file path of the file to be tail]
    """
    with closing(paramiko.Transport((host, port))) as transport:
        transport.connect(username=username, password=password)
        with closing(paramiko.SFTPClient.from_transport(transport)) as sftpclient:
            logging.info(f'Connection succesfully stablished to {host}')
            logging.info(f'tail {file_path}')

            if follow:
                with sftpclient.open(file_path, mode='a+') as fp:
                    logging.info('watching file...')
                    print()
                    while True:
                        line = fp.readline()
                        if line:
                            print(Style.BRIGHT + line)
            else:
                with sftpclient.open(file_path, mode='rb', bufsize=0) as fp:
                    logging.info(f'tail last {lines} line(s)...')
                    print()
                    fp.seek(-2, os.SEEK_END)
                    file_lines = []
                    for i in range(lines):
                        cur_char = fp.read(1)
                        while cur_char.decode() != os.linesep:
                            fp.seek(-2, os.SEEK_CUR)
                            cur_char = fp.read(1)
                        cur_pos = fp.tell()
                        file_lines.append(fp.readline().decode())
                        fp.seek(cur_pos - 2)
                    result = ''.join(file_lines[::-1])
                    print(Style.BRIGHT + result)
                    return result



@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('--host', '-h', prompt=True, confirmation_prompt=True, hide_input=True, help='SFTP host server, prompted if omitted.')
@click.option('--username', '-u', prompt=True, default=lambda: os.environ.get('USER', ''), help='SFTP username, prompted if omitted.')
@click.option('--password', '-p', prompt=True, hide_input=True, help='SFTP password, prompted if omitted.')
@click.option('--lines', '-n', default=5, show_default=True, help='Output the last n lines.')
@click.option('--follow', '-f', is_flag=True, help='Output data as the file grows.')
@click.argument('file_path', required=True)
@click.version_option(version='0.0.1')
def cli(host: str, username: str, password: str, lines: int, follow: bool, file_path: str) -> None:
    tail(host=host, username=username, password=password, lines=lines, follow=follow, file_path=file_path)

if __name__ == '__main__':
    cli()
