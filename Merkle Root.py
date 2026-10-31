import hashlib

def hash_data(data: str) -> str:
    return hashlib.sha256(data.encode()).hexdigest()

class MerkleTree:
    def __init__(self, txs: list[str]):
        self.leaves = [hash_data(tx) for tx in txs]
        self.tree = [self.leaves]
        self.build_tree()

    def build_tree(self):
        curr = self.leaves
        while len(curr) > 1:
            if len(curr) % 2 != 0:
                curr.append(curr[-1])
            nxt = [hash_data(curr[i] + curr[i+1]) for i in range(0, len(curr), 2)]
            self.tree.append(nxt)
            curr = nxt

    def get_root(self) -> str:
        return self.tree[-1][0]

    def get_proof(self, index: int) -> list[tuple[str, str]]:
        """Generates proof: list of (sibling_hash, direction)."""
        proof = []
        for layer in self.tree[:-1]:
            # Determine if current node is a right child (odd index)
            is_right = index % 2 == 1

            # Sibling is to the left if current node is right, otherwise to the right
            sibling_idx = index - 1 if is_right else index + 1

            # Handle odd layer length (duplicate last node if no right sibling exists)
            if sibling_idx >= len(layer):
                sibling_idx = index

            direction = "left" if is_right else "right"
            proof.append((layer[sibling_idx], direction))

            index //= 2

        return proof

def verify_tx(tx: str, proof: list[tuple[str, str]], root: str) -> bool:
    """Verifies a single transaction using only its proof and the root hash."""
    current_hash = hash_data(tx)
    for sibling, direction in proof:
        pair = (
            (sibling + current_hash)
            if direction == "left"
            else (current_hash + sibling)
        )
        current_hash = hash_data(pair)
    return current_hash == root

# --- Demonstration ---
txs = ["Alice pays Bob 10", "Bob pays Charlie 5", "Charlie pays Dave 2", "Dave pays Alice 1"]
tree = MerkleTree(txs)
root = tree.get_root()

# 1. Generate proof for index 2 ("Charlie pays Dave 2")
target_tx_idx = 2
proof = tree.get_proof(target_tx_idx)

# 2. Verify valid transaction
valid_tx = "Charlie pays Dave 2"
is_valid = verify_tx(valid_tx, proof, root)
print(f"Verify '{valid_tx}': {is_valid}")  # True

# 3. Verify fake/tampered transaction
fake_tx = "Charlie pays Dave 200"
is_fake_valid = verify_tx(fake_tx, proof, root)
print(f"Verify '{fake_tx}': {is_fake_valid}")  # False