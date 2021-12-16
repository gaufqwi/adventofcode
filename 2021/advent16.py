from aocpython.problem import AOCProblem

hex2bin = {'0' : '0000', '1': '0001', '2': '0010', '3': '0011', '4': '0100', '5': '0101', '6': '0110', '7': '0111',
           '8' : '1000', '9': '1001', 'A': '1010', 'B': '1011', 'C': '1100', 'D': '1101', 'E': '1110', 'F': '1111'}

class Problem(AOCProblem):
    def common(self):
        temp = ''
        for c in self.data.read().strip():
            temp += hex2bin[c]
        self.data = temp

    def parse_packet(self, pos):
        ver = int(self.data[pos:pos+3],2)
        pos += 3
        tid = int(self.data[pos:pos+3],2)
        pos += 3
        if tid == 4:
            self.log.debug(f'Literal packet at {pos-6}')
            # Read literal packet
            bits = ''
            while True:
                word = self.data[pos:pos+5]
                pos += 5
                bits += word[1:]
                if word[0] == '0':
                    break
            value = int(bits, 2)
            return ({'ver': ver, 'tid': tid, 'value': value}, pos)
        else:
            # Read operator packet
            subpackets = []
            mode = self.data[pos]
            pos += 1
            if mode == '0':
                self.log.debug(f'Length mode packet at {pos-7}')
                # length mode
                length = int(self.data[pos:pos+15], 2)
                pos += 15
                endpos = pos + length
                while pos != endpos:
                    subpacket, pos = self.parse_packet(pos)
                    subpackets.append(subpacket)
            else:
                self.log.debug(f'Count mode packet at {pos-7}')
                # count mode
                count = int(self.data[pos:pos+11], 2)
                pos += 11
                while count > 0:
                    subpacket, pos = self.parse_packet(pos)
                    subpackets.append(subpacket)
                    count -= 1
            return ({'ver': ver, 'tid': tid, 'subpackets': subpackets}, pos)

    def add_versions(self, packet):
        total = packet['ver']
        try:
            for sp in packet['subpackets']:
                total += self.add_versions(sp)
        except KeyError:
            pass
        return total

    def eval_packet(self, packet):
        if 'value' in packet:
            return packet['value']
        tid = packet['tid']
        subpacket_values = [self.eval_packet(p) for p in packet['subpackets']]
        if tid == 0:
            # Sum
            return sum(subpacket_values)
        elif tid == 1:
            # Product
            product = 1
            for v in subpacket_values:
                product *= v
            return product
        elif tid == 2:
            # Min
            return min(subpacket_values)
        elif tid == 3:
            # Max
            return max(subpacket_values)
        elif tid == 5:
            # GT
            return int(subpacket_values[0] > subpacket_values[1])
        elif tid == 6:
            # LT
            return int(subpacket_values[0] < subpacket_values[1])
        elif tid == 7:
            # Equal
            return int(subpacket_values[0] == subpacket_values[1])

    def part1(self):
        packet = self.parse_packet(0)[0]
        total = self.add_versions(packet)
        print(f'Sum of versions is {total}')

    def part2(self):
        packet = self.parse_packet(0)[0]
        value = self.eval_packet(packet)
        print(f'Value is {value}')
