import pytest
from pysftptail import tail

@pytest.fixture
def setup():
    last_5_lines = '03/22 08:51:06 INFO   :.....mailslot_create: creating mailslot for RSVP\n\
03/22 08:51:06 INFO   :....mailbox_register: mailbox allocated for rsvp\n\
03/22 08:51:06 INFO   :.....mailslot_create: creating mailslot for RSVP via UDP\n\
03/22 08:51:06 INFO   :....mailbox_register: mailbox allocated for rsvp-udp\n\
03/22 08:51:06 TRACE  :..entity_initialize: interface 9.67.117.98, entity for rsvp allocated and initialized\n'
    with open('sample.log', 'r') as file:
        file_content = file.read()
        server_content = {'logs_dir': {'sample.log': str(file_content)}}
        return {'server_content': server_content, 'last_5_lines': last_5_lines}

def test_tail_no_follow_5n(sftpserver, setup):
    with sftpserver.serve_content(setup['server_content']):
        response = tail(host=sftpserver.host, port=sftpserver.port, username='user', password='password', lines=5, 
        follow=False, file_path='/logs_dir/sample.log')
        assert response == setup['last_5_lines']

