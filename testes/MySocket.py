import socket
from Segment import Segment

MESSAGE_SIZE = 1024
HEADER_SIZE = 11
DATA_SIZE = MESSAGE_SIZE - HEADER_SIZE

class MySocket(socket.socket):
    def send_segment(self, segment, ack_number, dest_addr):
        segment.set_ack_number(ack_number)
        self.sendto(segment.segment.encode(), dest_addr)

    # get a message of any size and return a list of fragments of that message, each one with the size equal to DATA_SIZE or smaller. Also adds a header to each fragment
    def fragment_message(self, msg, seq_number):
        segments = []
        
        while len(msg) > 0:
            if len(msg) < DATA_SIZE:
                segment = Segment(seq_number, data=msg[:(DATA_SIZE-1)])
            else:
                segment = Segment(seq_number, last_frag='0', data=msg[:(DATA_SIZE-1)])
            
            segments.append(segment)
            seq_number += 1
            msg = msg[DATA_SIZE:]

        # print('segments:\n')
        # for segment in segments:
        #     print(segment + '\n')

        return segments, seq_number