import json
import os
import time
from typing import Optional, Dict, List, Any


def load_transactions(file_path: str = None) -> List[Dict[str, Any]]:
    if file_path is None:
        file_path = os.path.join(os.path.dirname(__file__), "transactions.json")
    
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return []
    
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def linear_search(transactions: List[Dict], target_id: int) -> Optional[Dict]:
    for transaction in transactions:
        if transaction["id"] == target_id:
            return transaction
    return None


def binary_search(sorted_transactions: List[Dict], target_id: int) -> Optional[Dict]:
    left = 0
    right = len(sorted_transactions) - 1
    
    while left <= right:
        mid = (left + right) // 2
        mid_id = sorted_transactions[mid]["id"]
        
        if mid_id == target_id:
            return sorted_transactions[mid]
        elif mid_id < target_id:
            left = mid + 1
        else:
            right = mid - 1
    
    return None


def build_hash_table(transactions: List[Dict]) -> Dict[int, Dict]:
    return {tx["id"]: tx for tx in transactions}


def hash_lookup(hash_table: Dict[int, Dict], target_id: int) -> Optional[Dict]:
    return hash_table.get(target_id, None)


def measure_search_time(search_func, *args, iterations: int = 1000) -> float:
    start_time = time.perf_counter()
    
    for _ in range(iterations):
        search_func(*args)
    
    end_time = time.perf_counter()
    total_time = (end_time - start_time) * 1_000_000
    
    return total_time / iterations


def run_comparison(num_records: int = 20):
    print("=" * 70)
    print("DSA INTEGRATION: SEARCH ALGORITHM COMPARISON")
    print("=" * 70)
    print()
    
    all_transactions = load_transactions()
    
    if len(all_transactions) == 0:
        print("Error: No transactions loaded. Please ensure transactions.json exists.")
        return
    
    transactions = all_transactions[:max(num_records, len(all_transactions))]
    num_transactions = len(transactions)
    
    print(f"Dataset Size: {num_transactions} transactions")
    print("-" * 70)
    print()
    
    transaction_list = transactions.copy()
    sorted_transactions = sorted(transactions, key=lambda x: x["id"])
    hash_table = build_hash_table(transactions)
    
    test_ids = [
        transactions[0]["id"],
        transactions[len(transactions) // 2]["id"],
        transactions[-1]["id"],
        999999
    ]
    
    print("SEARCH RESULTS AND TIMING")
    print("-" * 70)
    
    results = {
        "linear": [],
        "binary": [],
        "hash": []
    }
    
    for target_id in test_ids:
        print(f"\nSearching for ID: {target_id}")
        print("-" * 40)
        
        linear_time = measure_search_time(linear_search, transaction_list, target_id)
        linear_result = linear_search(transaction_list, target_id)
        results["linear"].append(linear_time)
        print(f"  Linear Search:     {linear_time:.4f} us | Found: {linear_result is not None}")
        
        binary_time = measure_search_time(binary_search, sorted_transactions, target_id)
        binary_result = binary_search(sorted_transactions, target_id)
        results["binary"].append(binary_time)
        print(f"  Binary Search:     {binary_time:.4f} us | Found: {binary_result is not None}")
        
        hash_time = measure_search_time(hash_lookup, hash_table, target_id)
        hash_result = hash_lookup(hash_table, target_id)
        results["hash"].append(hash_time)
        print(f"  Hash Lookup:       {hash_time:.4f} us | Found: {hash_result is not None}")
    
    print()
    print("=" * 70)
    print("PERFORMANCE SUMMARY")
    print("=" * 70)
    print()
    
    avg_linear = sum(results["linear"]) / len(results["linear"])
    avg_binary = sum(results["binary"]) / len(results["binary"])
    avg_hash = sum(results["hash"]) / len(results["hash"])
    
    print(f"Average Execution Times (over {len(test_ids)} searches, 1000 iterations each):")
    print(f"  Linear Search:     {avg_linear:.4f} us")
    print(f"  Binary Search:     {avg_binary:.4f} us")
    print(f"  Hash Lookup:       {avg_hash:.4f} us")
    print()
    
    print("Speed Comparison:")
    print(f"  Hash Lookup is {avg_linear / avg_hash:.2f}x faster than Linear Search")
    print(f"  Binary Search is {avg_linear / avg_binary:.2f}x faster than Linear Search")
    print(f"  Hash Lookup is {avg_binary / avg_hash:.2f}x faster than Binary Search")
    print()
    
    print("=" * 70)
    print("TIME COMPLEXITY ANALYSIS")
    print("=" * 70)
    print()
    print("Algorithm        | Time Complexity | Space Complexity | Notes")
    print("-" * 70)
    print("Linear Search    | O(n)            | O(1)             | Simple, no preprocessing")
    print("Binary Search    | O(log n)        | O(1)             | Requires sorted data")
    print("Hash Lookup      | O(1) average    | O(n)             | Fastest lookup, needs hash table")
    print()
    
    return results


def run_scalability_test():
    print()
    print("=" * 70)
    print("SCALABILITY TEST")
    print("=" * 70)
    print()
    
    all_transactions = load_transactions()
    
    if len(all_transactions) < 100:
        print("Not enough transactions for scalability test (need at least 100)")
        return
    
    sizes = [20, 50, 100, 200, 500, 1000]
    sizes = [s for s in sizes if s <= len(all_transactions)]
    
    print(f"Testing with dataset sizes: {sizes}")
    print()
    print("Size    | Linear (us) | Binary (us) | Hash (us)")
    print("-" * 55)
    
    for size in sizes:
        transactions = all_transactions[:size]
        sorted_tx = sorted(transactions, key=lambda x: x["id"])
        hash_table = build_hash_table(transactions)
        
        target_id = transactions[-1]["id"]
        
        linear_time = measure_search_time(linear_search, transactions, target_id)
        binary_time = measure_search_time(binary_search, sorted_tx, target_id)
        hash_time = measure_search_time(hash_lookup, hash_table, target_id)
        
        print(f"{size:>6}  | {linear_time:>10.4f}  | {binary_time:>10.4f}  | {hash_time:>10.4f}")
    
    print()


if __name__ == "__main__":
    results = run_comparison(num_records=20)
    run_scalability_test()
    
    print("=" * 70)
    print("REFLECTION QUESTIONS FOR REPORT")
    print("=" * 70)
    print()
    print("1. Why is dictionary/hash lookup faster than linear search?")
    print("   - Hash tables use a hash function to compute the index directly")
    print("   - O(1) average access vs O(n) for linear search")
    print("   - No need to iterate through all elements")
    print()
    print("2. Why is binary search faster than linear but slower than hash?")
    print("   - Binary search eliminates half the remaining elements each step: O(log n)")
    print("   - Still requires comparisons, unlike direct hash access")
    print("   - Requires sorted data (preprocessing cost)")
    print()
    print("3. What other data structure could improve efficiency?")
    print("   - B-Tree: Self-balancing, efficient for disk-based storage")
    print("   - Database Indexing: Built on B-Tree/B+ Tree structures")
    print("   - Trie: Useful for prefix-based searches on string IDs")
    print("   - Bloom Filter: Fast membership testing (with false positives)")
    print()
