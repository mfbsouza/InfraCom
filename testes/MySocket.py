import socket

MESSAGE_SIZE = 1024
HEADER_SIZE = 11
DATA_SIZE = MESSAGE_SIZE - HEADER_SIZE

class MySocket(socket.socket):
    # get a message of any size and return a list of fragments of that message, each one with the size equal to DATA_SIZE or smaller. Also adds a header to each fragment
    def fragment_message(self, msg, seq_number):
        fragments = []
        
        while len(msg) > 0:
            if len(msg) < DATA_SIZE:
                fragment = self.add_header_to_segment(msg[:(DATA_SIZE-1)], seq_number, '1')
            else:
                fragment = self.add_header_to_segment(msg[:(DATA_SIZE-1)], seq_number)
            
            fragments.append(fragment)
            seq_number += 1
            msg = msg[DATA_SIZE:]

        # print('fragments:\n')
        # i = 0
        # while i < len(fragments):
        #     print(fragments[i])
        #     print()
        #     i += 1

        return fragments, seq_number

    # add a header (4 bytes for sequence number + 4 bytes for next ack number) to a segment's data
    def add_header_to_segment(self, data, seq_number, ack_number=-1, syn='0', fin='0', last_frag='0'):
        ack_number = int(ack_number)

        segment = ('%04d' % seq_number) + ('%04d' % ack_number) + last_frag + syn + fin + data

        # print(segment)
        return segment

    def set_ack_number(self, segment, ack_number):
        segment = segment[:4] + ('%04d' % ack_number) + segment[8:]

        return segment

    # # send message to specified destination (fragmented, if necessary)
    # def send_message(self, fragments, seq_number, ack_number, dest_addr):
    #     for i, fragment in enumerate(fragments):
    #         if i == (len(fragments) - 1):
    #             fragment = self.add_header_to_segment(fragment, seq_number, ack_number, '1')
    #         else:
    #             fragment = self.add_header_to_segment(fragment, seq_number, ack_number)

    #         self.sendto(fragment.encode(), dest_addr)

    def send_segment(self, segment, ack_number, dest_addr):
        segment = self.set_ack_number(segment, ack_number)

        self.sendto(segment.encode(), dest_addr)