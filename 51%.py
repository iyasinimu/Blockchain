import hashlib

from collections import Counter
import time


class Block:

  def __init__(self, index, data, miner, previous_hash, difficulty=2):
    self.index = index
    self.timestamp = time.time()
    self.data = data
    self.miner = miner  # Added miner attribute
    self.previous_hash = previous_hash
    self.difficulty = difficulty
    self.nonce = 0
    self.hash = self.mine_block()

  def calculate_hash(self):
    contents = f"{self.index}{self.timestamp}{self.data}{self.miner}{self.previous_hash}{self.difficulty}{self.nonce}"
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
    return Block(0, "Genesis Block", "System", "0", self.difficulty)

  def add_block(self, data, miner):
    prev_block = self.chain[-1]
    new_block = Block(
        len(self.chain), data, miner, prev_block.hash, self.difficulty
    )
    self.chain.append(new_block)

  def verify_51_percent_attack(self):
    """Calculates block control per miner and verifies if any single miner holds >= 51% dominance."""
    total_blocks = len(self.chain)
    miner_counts = Counter(block.miner for block in self.chain)

    print("\n--- MINER CONTROL ANALYSIS ---")
    attack_detected = False
    for miner, count in miner_counts.items():
      percentage = (count / total_blocks) * 100
      print(
          f"Miner: {miner:} | Blocks Mined: {count}/{total_blocks} | Share:"
          f" {percentage:.2f}%"
      )

      if percentage >= 51.0:
        attack_detected = True
        dominant_miner = miner
        dominant_share = percentage

    print("-" * 50)
    if attack_detected:
      print(
          f"ALERT: 51% Attack risk present! Miner '{dominant_miner}' controls"
          f" {dominant_share:.2f}% of the chain."
      )
    else:
      print(
          "STATUS: Safe. No single miner controls 51% or more of the chain."
      )

    return attack_detected


# --- Usage Example ---
my_blockchain = Blockchain(difficulty=2)

print("Mining Blocks...")
my_blockchain.add_block("Alice sent Bob 5 BTC", miner="Miner_A")
my_blockchain.add_block("Bob sent Charlie 2 BTC", miner="Miner_A")
my_blockchain.add_block("Charlie sent David 1 BTC", miner="Miner_A")
my_blockchain.add_block("David sent Eve 0.5 BTC", miner="Miner_B")

# Verify 51% attack condition
my_blockchain.verify_51_percent_attack()