import hashlib
import time


class Block:
    def __init__(self, index, data, nonce, previous_hash, difficulty=2):
        self.index = index
        self.timestamp = time.time()
        self.data = data
        self.previous_hash = previous_hash
        self.difficulty = difficulty
        self.nonce = nonce
        self.hash = self.mine_block()

    def calculate_hash(self):
        contents = f"{self.index}{self.timestamp}{self.data}{self.previous_hash}{self.difficulty}{self.nonce}"
        return hashlib.sha256(contents.encode()).hexdigest()

    def mine_block(self):
        target = "0" * self.difficulty

        current_hash = self.calculate_hash()
        while not current_hash.startswith(target):
            self.nonce += 1
            current_hash = self.calculate_hash()

        return current_hash


class Blockchain:
    def __init__(self, difficulty=2):
        self.difficulty = difficulty
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, "Plabon", 4, "0", self.difficulty)

    def add_block(self, data):
        prev_block = self.chain[-1]
        new_block = Block(len(self.chain), data, 5, prev_block.hash, self.difficulty, )
        self.chain.append(new_block)


my_blockchain = Blockchain(difficulty=3)

print("Mining Block 1...")
my_blockchain.add_block("Alice sent Bob 5 BTC")

print("Mining Block 2...")
my_blockchain.add_block("Bob sent Charlie 2 BTC")

print("\n--- BLOCKCHAIN CONTENTS ---")
for block in my_blockchain.chain:
    print(f"Index     : {block.index}")
    print(f"Data      : {block.data}")
    print(f"Difficulty: {block.difficulty}")
    print(f"Nonce     : {block.nonce}")
    print(f"Hash      : {block.hash}")
    print(f"Prev Hash : {block.previous_hash}\n" + "-" * 50)