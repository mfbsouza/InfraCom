import socket

MESSAGE_SIZE = 1024
HEADER_SIZE = 9
DATA_SIZE = MESSAGE_SIZE - HEADER_SIZE

class MySocket(socket.socket):
    # get a message of any size and return a list of fragments of that message, each one withthe size equal to DATA_SIZE or smaller
    def fragment_message(self, msg):
        fragments = []
        
        while len(msg) > 0:
            fragments.append(msg[:(DATA_SIZE-1)])
            msg = msg[DATA_SIZE:]

        # print('fragments:\n')
        # i = 0
        # while i < len(fragments):
        #     print(fragments[i])
        #     print()
        #     i += 1

        return fragments

    # add a header (4 bytes for sequence number + 4 bytes for next ack number) to a segment's data
    def add_header_to_segment(self, data, seq_number, ack_number, last_frag='0'):
        segment = ('%04d' % seq_number) + ('%04d' % ack_number) + last_frag + data

        # print(segment)
        return segment


    # send message to specified destination (fragmented, if necessary)
    def send_message(self, msg, seq_number, ack_number, dest_addr):
        message_fragments = self.fragment_message(msg)

        for i, fragment in enumerate(message_fragments):
            if i == (len(message_fragments) - 1):
                fragment = self.add_header_to_segment(fragment, seq_number, ack_number, '1')
            else:
                fragment = self.add_header_to_segment(fragment, seq_number, ack_number)

            self.sendto(fragment.encode(), dest_addr)
            seq_number += 1

        return seq_number