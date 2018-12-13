class Segment:
    def __init__(self, seq_number=-1, ack_number=-1, last_frag='1', syn='0', fin='0', data='', segment=''):
        if segment == '':
            self.seq_number = seq_number
            self.ack_number = ack_number
            self.last_frag = last_frag
            self.syn = syn
            self.fin = fin
            self.data = data
            self.segment = ('%04d' % self.seq_number) + ('%04d' % self.ack_number) + self.last_frag + self.syn + self.fin + self.data
        else:
            self.seq_number = int(segment[:4])
            self.ack_number = int(segment[4:8])
            self.last_frag = segment[8]
            self.syn = segment[9]
            self.fin = segment[10]
            self.data = segment[11:]
            self.segment = segment

    def set_ack_number(self, ack_number):
        self.ack_number = ack_number
        self.segment = self.segment[:4] + ('%04d' % ack_number) + self.segment[8:]

    def print(self):
        print('seq_number:', self.seq_number)
        print('ack_number:', self.ack_number)
        print('last_frag:', self.last_frag)
        print('syn:', self.syn)
        print('fin:', self.fin)
        print('data:', self.data)
        print()
