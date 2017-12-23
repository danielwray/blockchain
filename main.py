import time
import hashlib
import json
import threading

thread_lock = threading.Lock()
threads = []


class Block:

    def __init__(self, index, timestamp, data, previous_hash=""):
        self.index = index
        self.internal_index = 0
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.nonce = 0
        self.hash = self.calculate_block_hash()

    def calculate_block_hash(self):
        block = json.dumps({"index": self.index,
                            "internal_index": self.internal_index,
                            "previous_hash": self.previous_hash,
                            "timestamp": str(self.timestamp),
                            "data": self.data,
                            "nonce": self.nonce})
        encoded_block = str(block).encode('utf-8')
        hashed = hashlib.sha256(encoded_block).hexdigest()
        return hashed

    def mine_block(self, difficulty):
        difficulty_level = "0" * difficulty
        while not str(self.hash).startswith(difficulty_level):
            self.nonce += 1
            self.hash = self.calculate_block_hash()
        return


class BlockChain:

    def __init__(self):
        self.chain = [self.create_initial_block()]
        self.difficulty = 3

    @staticmethod
    def create_initial_block():
        return Block(0, time.strftime("%d/%m/%Y"), "initial block", "0")

    def get_latest_block(self):
        return self.chain[len(self.chain) - 1]

    def get_all_blocks(self):
        blockchain = []
        for block_index in range(0, len(self.chain)):
            blockchain.append({"internal_index" : self.chain[block_index].internal_index,
                               "index": self.chain[block_index].index,
                               "timestamp": self.chain[block_index].timestamp,
                               "data": self.chain[block_index].data,
                               "hash": self.chain[block_index].hash,
                               "previous_hash": self.chain[block_index].previous_hash,
                               "nonce": self.chain[block_index].nonce})
        return blockchain

    def add_new_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.internal_index = self.get_latest_block().internal_index + 1

        mt = ThreadSpawner(new_block, self.difficulty)
        mt.start()
        threads.append(mt)

        self.chain.append(new_block)

        for thread in threads:
            thread.join()
        return

    def is_chain_valid(self):
        for block_index in range(1, len(self.chain)):
            current_block = self.chain[block_index]
            previous_block = self.chain[block_index - 1]

            if current_block.hash != current_block.calculate_block_hash():
                return "Current hash has been tampered!"

            if current_block.previous_hash != previous_block.hash:
                return "Hashes do not match on chain!"

        return True


class ThreadSpawner(threading.Thread):
    def __init__(self, block, difficulty):
        threading.Thread.__init__(self)
        self.block = block
        self.difficulty = difficulty

    def run(self):
        thread_lock.acquire()
        self.block.mine_block(self.difficulty)
        thread_lock.release()


def main():
    dcoin = BlockChain()


if __name__ == '__main__':
    main()
