import time
import json
import hashlib
import base64
import os
from typing import Dict, Any, List, Tuple
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization

# ==========================================
# 1. Cryptographic Primitives & Helpers
# ==========================================

class CAHPUtils:
    @staticmethod
    def get_timestamp() -> int:
        return int(time.time())

    @staticmethod
    def b64_enc(data: bytes) -> str:
        return base64.b64encode(data).decode('utf-8')

    @staticmethod
    def b64_dec(data: str) -> bytes:
        return base64.b64decode(data.encode('utf-8'))

    @staticmethod
    def sha256(data: bytes) -> bytes:
        return hashlib.sha256(data).digest()

class MerkleProver:
    """
    Implements Section 5: Canonical Weight Commitment
    """
    @staticmethod
    def compute_root_from_file(file_path: str) -> bytes:
        # Simulating file reading for the reference
        # In prod, read 1MB chunks: while chunk := f.read(1024*1024)
        chunks = []
        
        # Mocking a 5MB model for demonstration
        mock_data = b"model_weight_data" * 100000 
        chunk_size = 1024 * 1024
        
        for i in range(0, len(mock_data), chunk_size):
            chunk = mock_data[i:i+chunk_size]
            chunks.append(hashlib.sha256(chunk).digest())
            
        return MerkleProver._build_tree(chunks)

    @staticmethod
    def _build_tree(leaves: List[bytes]) -> bytes:
        if not leaves:
            return hashlib.sha256(b"").digest()
        
        tree = leaves
        while len(tree) > 1:
            next_level = []
            for i in range(0, len(tree), 2):
                left = tree[i]
                right = tree[i+1] if i+1 < len(tree) else left # Duplicate last if odd
                combined = hashlib.sha256(left + right).digest()
                next_level.append(combined)
            tree = next_level
        return tree[0]

    @staticmethod
    def bind_identity(merkle_root: bytes, challenger_nonce: bytes, burn_txid: str) -> bytes:
        """
        Section 5.3: Root = hash(root || challenger_nonce || small_burn_txid)
        """
        payload = merkle_root + challenger_nonce + burn_txid.encode('utf-8')
        return hashlib.sha256(payload).digest()

class Hashcash:
    """
    Section 6: Energy-Bounded Challenge
    """
    @staticmethod
    def solve(prefix: bytes, difficulty_bits: int) -> Tuple[bytes, float]:
        start = time.time()
        nonce = 0
        target = 1 << (256 - difficulty_bits)
        
        while True:
            n_bytes = nonce.to_bytes(8, 'big')
            h = hashlib.sha256(prefix + n_bytes).digest()
            h_int = int.from_bytes(h, 'big')
            
            if h_int < target:
                end = time.time()
                return n_bytes, (end - start)
            
            nonce += 1

# ==========================================
# 2. Message Format (Section 3)
# ==========================================

class CAHPMessage:
    def __init__(self, sender_kp, phase: int, sender_type: str, session_id: bytes, payload: Dict):
        self.phase = phase
        self.sender_type = sender_type
        self.sender_pk = sender_kp.public_key()
        self.sender_sk = sender_kp
        self.session_id = session_id
        self.timestamp = CAHPUtils.get_timestamp()
        self.nonce = os.urandom(8)
        self.payload = payload
        self.signature = b""

    def sign(self):
        # Canonicalize fields for signing
        # In production, use CBOR. Here we use deterministic JSON.
        data_struct = {
            "phase": self.phase,
            "sender_type": self.sender_type,
            "sender_id": CAHPUtils.b64_enc(self.sender_pk.public_bytes(
                encoding=serialization.Encoding.Raw,
                format=serialization.PublicFormat.Raw
            )),
            "session_id": CAHPUtils.b64_enc(self.session_id),
            "timestamp": self.timestamp,
            "nonce": CAHPUtils.b64_enc(self.nonce),
            "payload": self.payload
        }
        
        canonical_bytes = json.dumps(data_struct, sort_keys=True).encode('utf-8')
        self.signature = self.sender_sk.sign(canonical_bytes)
        data_struct['signature'] = CAHPUtils.b64_enc(self.signature)
        return data_struct

    @staticmethod
    def verify(message_dict: Dict) -> bool:
        # Reconstruct canonical bytes
        sig = CAHPUtils.b64_dec(message_dict.pop('signature'))
        sender_pk_bytes = CAHPUtils.b64_dec(message_dict['sender_id'])
        
        canonical_bytes = json.dumps(message_dict, sort_keys=True).encode('utf-8')
        
        public_key = ed25519.Ed25519PublicKey.from_public_bytes(sender_pk_bytes)
        
        # 1. Verify Signature
        try:
            public_key.verify(sig, canonical_bytes)
        except Exception:
            return False

        # 2. Verify Timestamp (Section 3: +/- 60 seconds)
        now = CAHPUtils.get_timestamp()
        if abs(now - message_dict['timestamp']) > 60:
            print("(!) Validation Failed: Timestamp expired")
            return False
            
        return True

# ==========================================
# 3. Node Implementations
# ==========================================

class Node:
    def __init__(self, node_type: str):
        self.type = node_type
        self.key_pair = ed25519.Ed25519PrivateKey.generate()
        self.session_store = {}

    def create_msg(self, phase, session_id, payload):
        msg = CAHPMessage(self.key_pair, phase, self.type, session_id, payload)
        return msg.sign()

class MetabolicNode(Node): # e.g., Helix
    def __init__(self):
        super().__init__("metabolic")

    def generate_challenge(self) -> bytes:
        return os.urandom(16)

class OpenWeightNode(Node): # e.g., Local Llama
    def __init__(self):
        super().__init__("open_weight")
        # Pre-calculate model root for demo
        print("[INIT] OpenWeightNode: Hashing local model (simulation)...")
        self.raw_merkle_root = MerkleProver.compute_root_from_file("fake_model.gguf")

# ==========================================
# 4. Handshake Execution Flow (Section 7)
# ==========================================

def run_cahp_handshake():
    print("
--- CAHP v0.2 Protocol Simulation ---
")

    # Setup
    alice = MetabolicNode()  # Challenger
    bob = OpenWeightNode()   # Prover
    
    session_id = os.urandom(16)
    print(f"Session ID: {CAHPUtils.b64_enc(session_id)}")

    # --- Phase 1: Discovery ---
    print("
[Phase 1] Discovery")
    # Alice broadcasts
    msg_1 = alice.create_msg(1, session_id, {"hello": "syn"})
    print(f"Alice -> Bob: SYN")
    
    # Bob verifies and responds
    if not CAHPMessage.verify(msg_1.copy()): raise Exception("Verification Fail")
    msg_1_ack = bob.create_msg(1, session_id, {"hello": "ack"})
    print(f"Bob -> Alice: ACK")

    # --- Phase 2: Proof Exchange ---
    print("
[Phase 2] Proof Exchange")
    # Alice sends Proof-of-Burn (simulated TXID)
    msg_2_alice = alice.create_msg(2, session_id, {
        "proof_type": "burn", 
        "txid": "helix_tx_7f8a9b...", 
        "amount": 5000000 # sats
    })
    
    # Bob receives Alice's proof, verifies it, extracts nonce (using session_id as nonce for binding)
    challenger_nonce = session_id 
    
    # Bob constructs Canonical Weight Commitment (Section 5)
    # Binds identity to challenger + small burn
    burn_txid = "bitcoin_tx_123..." 
    bound_root = MerkleProver.bind_identity(bob.raw_merkle_root, challenger_nonce, burn_txid)
    
    msg_2_bob = bob.create_msg(2, session_id, {
        "proof_type": "merkle_weight",
        "bound_root": CAHPUtils.b64_enc(bound_root),
        "burn_txid": burn_txid
    })
    print(f"Alice sends Burn Proof. Bob sends Weight Commitment (Root: {msg_2_bob['payload']['bound_root'][:10]}...)")

    # --- Phase 3: Challenge (Energy Bound) ---
    print("
[Phase 3] Challenge")
    # Alice challenges Bob to prove compute capability (Sybil resistance)
    puzzle_prefix = alice.generate_challenge()
    difficulty = 16 # Low for demo, spec suggests higher for ~10J
    
    msg_3 = alice.create_msg(3, session_id, {
        "challenge_type": "hashcash",
        "prefix": CAHPUtils.b64_enc(puzzle_prefix),
        "difficulty": difficulty
    })
    print(f"Alice -> Bob: Solve Hashcash (Difficulty {difficulty})")

    # --- Phase 4: Response ---
    print("
[Phase 4] Response")
    if not CAHPMessage.verify(msg_3.copy()): raise Exception("Verification Fail")
    
    # Bob solves
    print("Bob is solving puzzle...")
    nonce_sol, runtime = Hashcash.solve(puzzle_prefix, difficulty)
    print(f"Solved in {runtime:.4f}s")
    
    msg_4 = bob.create_msg(4, session_id, {
        "solution": CAHPUtils.b64_enc(nonce_sol),
        "runtime_attestation": runtime
    })
    print(f"Bob -> Alice: Solution {CAHPUtils.b64_enc(nonce_sol)}")

    # --- Phase 5: Verification & Ticket ---
    print("
[Phase 5] Verification")
    if not CAHPMessage.verify(msg_4.copy()): raise Exception("Verification Fail")
    
    # Alice verifies solution
    check_h = hashlib.sha256(puzzle_prefix + nonce_sol).digest()
    check_int = int.from_bytes(check_h, 'big')
    target = 1 << (256 - difficulty)
    
    if check_int < target:
        print("Alice: Solution Valid.")
        # Issue Session Ticket
        ticket = {
            "status": "verified",
            "expiry": CAHPUtils.get_timestamp() + 86400, # 24h
            "capabilities": ["inference", "rag"]
        }
        msg_5 = alice.create_msg(5, session_id, ticket)
        print("Alice -> Bob: Session Established [VERIFIED:CAHP]")
        print(f"Ticket Signature: {msg_5['signature'][:20]}...")
    else:
        print("Alice: Solution Invalid.")

if __name__ == "__main__":
    run_cahp_handshake()
