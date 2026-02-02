"""
============================================================
DSA Integration: Search Algorithm Comparison
============================================================
This module implements and compares three search methods:
1. Linear Search - O(n) time complexity
2. Binary Search - O(log n) time complexity (requires sorted data)
3. Hash/Dictionary Lookup - O(1) average time complexity

Author: Olivier Collins ITANGISHAKA
Assignment: Building and Securing a REST API - Task 5
============================================================
"""

import json
import os
import time
from typing import Optional, Dict, List, Any


# ============================================================
# DATA LOADING
# ============================================================
def load_transactions(file_path: str = None) -> List[Dict[str, Any]]:
    """
    Load transactions from JSON file.
    
    Args:
        file_path: Path to the JSON file containing transactions
        
    Returns:
        List of transaction dictionaries
    """
    if file_path is None:
        file_path = os.path.join(os.path.dirname(__file__), "transactions.json")
    
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return []
    
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


# ============================================================
# SEARCH ALGORITHM 1: LINEAR SEARCH
# ============================================================
def linear_search(transactions: List[Dict], target_id: int) -> Optional[Dict]:
    """
    Linear Search: Scan through the list sequentially to find a transaction by ID.
    
    Time Complexity: O(n) - where n is the number of transactions
    Space Complexity: O(1) - no additional space needed
    
    How it works:
    - Start from the first element
    - Compare each element's ID with the target ID
    - Return the element if found, None if not found
    
    Args:
        transactions: List of transaction dictionaries
        target_id: The transaction ID to search for
        
    Returns:
        The transaction dictionary if found, None otherwise
    """
    for transaction in transactions:
        if transaction["id"] == target_id:
            return transaction
    return None


# ============================================================
# SEARCH ALGORITHM 2: BINARY SEARCH
# ============================================================
def binary_search(sorted_transactions: List[Dict], target_id: int) -> Optional[Dict]:
    """
    Binary Search: Search on a sorted list by repeatedly dividing the search interval in half.
    
    Time Complexity: O(log n) - where n is the number of transactions
    Space Complexity: O(1) - iterative implementation
    
    PREREQUISITE: The list MUST be sorted by ID for binary search to work correctly.
    
    How it works:
    - Start with the middle element
    - If target equals middle element, return it
    - If target is less than middle, search the left half
    - If target is greater than middle, search the right half
    - Repeat until found or search space is exhausted
    
    Args:
        sorted_transactions: List of transaction dictionaries SORTED by ID
        target_id: The transaction ID to search for
        
    Returns:
        The transaction dictionary if found, None otherwise
    """
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


# ============================================================
# SEARCH ALGORITHM 3: HASH/DICTIONARY LOOKUP
# ============================================================
def build_hash_table(transactions: List[Dict]) -> Dict[int, Dict]:
    """
    Build a hash table (dictionary) mapping transaction IDs to transactions.
    
    Time Complexity: O(n) - one-time cost to build the hash table
    Space Complexity: O(n) - stores all transactions in the dictionary
    
    Args:
        transactions: List of transaction dictionaries
        
    Returns:
        Dictionary mapping transaction ID to transaction data
    """
    return {tx["id"]: tx for tx in transactions}


def hash_lookup(hash_table: Dict[int, Dict], target_id: int) -> Optional[Dict]:
    """
    Hash/Dictionary Lookup: Direct access using the ID as a key.
    
    Time Complexity: O(1) average case - constant time lookup
    Space Complexity: O(1) - lookup itself doesn't need extra space
                     (but the hash table requires O(n) space)
    
    How it works:
    - Use Python's built-in dictionary
    - The ID is hashed to find the memory location directly
    - No iteration or comparison needed
    
    Args:
        hash_table: Dictionary mapping transaction IDs to transactions
        target_id: The transaction ID to search for
        
    Returns:
        The transaction dictionary if found, None otherwise
    """
    return hash_table.get(target_id, None)


# ============================================================
# PERFORMANCE MEASUREMENT
# ============================================================
def measure_search_time(search_func, *args, iterations: int = 1000) -> float:
    """
    Measure the average execution time of a search function.
    
    Args:
        search_func: The search function to measure
        *args: Arguments to pass to the search function
        iterations: Number of times to run the search for averaging
        
    Returns:
        Average execution time in microseconds
    """
    start_time = time.perf_counter()
    
    for _ in range(iterations):
        search_func(*args)
    
    end_time = time.perf_counter()
    total_time = (end_time - start_time) * 1_000_000  # Convert to microseconds
    
    return total_time / iterations


def run_comparison(num_records: int = 20):
    """
    Run a comprehensive comparison of all three search algorithms.
    
    Args:
        num_records: Minimum number of records to use (will use more if available)
    """
    print("=" * 70)
    print("DSA INTEGRATION: SEARCH ALGORITHM COMPARISON")
    print("=" * 70)
    print()
    
    # Load transactions
    all_transactions = load_transactions()
    
    if len(all_transactions) == 0:
        print("Error: No transactions loaded. Please ensure transactions.json exists.")
        return
    
    # Use at least the specified number of records
    transactions = all_transactions[:max(num_records, len(all_transactions))]
    num_transactions = len(transactions)
    
    print(f"Dataset Size: {num_transactions} transactions")
    print("-" * 70)
    print()
    
    # Prepare data structures
    # 1. List for linear search (unsorted)
    transaction_list = transactions.copy()
    
    # 2. Sorted list for binary search
    sorted_transactions = sorted(transactions, key=lambda x: x["id"])
    
    # 3. Hash table for dictionary lookup
    hash_table = build_hash_table(transactions)
    
    # Test IDs: beginning, middle, end, and non-existent
    test_ids = [
        transactions[0]["id"],                          # First element
        transactions[len(transactions) // 2]["id"],    # Middle element
        transactions[-1]["id"],                         # Last element
        999999                                          # Non-existent ID
    ]
    
    print("SEARCH RESULTS AND TIMING")
    print("-" * 70)
    
    # Results storage for summary
    results = {
        "linear": [],
        "binary": [],
        "hash": []
    }
    
    for target_id in test_ids:
        print(f"\nSearching for ID: {target_id}")
        print("-" * 40)
        
        # Linear Search
        linear_time = measure_search_time(linear_search, transaction_list, target_id)
        linear_result = linear_search(transaction_list, target_id)
        results["linear"].append(linear_time)
        print(f"  Linear Search:     {linear_time:.4f} µs | Found: {linear_result is not None}")
        
        # Binary Search
        binary_time = measure_search_time(binary_search, sorted_transactions, target_id)
        binary_result = binary_search(sorted_transactions, target_id)
        results["binary"].append(binary_time)
        print(f"  Binary Search:     {binary_time:.4f} µs | Found: {binary_result is not None}")
        
        # Hash Lookup
        hash_time = measure_search_time(hash_lookup, hash_table, target_id)
        hash_result = hash_lookup(hash_table, target_id)
        results["hash"].append(hash_time)
        print(f"  Hash Lookup:       {hash_time:.4f} µs | Found: {hash_result is not None}")
    
    # Summary Statistics
    print()
    print("=" * 70)
    print("PERFORMANCE SUMMARY")
    print("=" * 70)
    print()
    
    avg_linear = sum(results["linear"]) / len(results["linear"])
    avg_binary = sum(results["binary"]) / len(results["binary"])
    avg_hash = sum(results["hash"]) / len(results["hash"])
    
    print(f"Average Execution Times (over {len(test_ids)} searches, 1000 iterations each):")
    print(f"  Linear Search:     {avg_linear:.4f} µs")
    print(f"  Binary Search:     {avg_binary:.4f} µs")
    print(f"  Hash Lookup:       {avg_hash:.4f} µs")
    print()
    
    # Speed comparison
    print("Speed Comparison:")
    print(f"  Hash Lookup is {avg_linear / avg_hash:.2f}x faster than Linear Search")
    print(f"  Binary Search is {avg_linear / avg_binary:.2f}x faster than Linear Search")
    print(f"  Hash Lookup is {avg_binary / avg_hash:.2f}x faster than Binary Search")
    print()
    
    # Complexity Analysis
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
    """
    Test how each algorithm scales with increasing data sizes.
    """
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
    print("Size    | Linear (µs) | Binary (µs) | Hash (µs)")
    print("-" * 55)
    
    for size in sizes:
        transactions = all_transactions[:size]
        sorted_tx = sorted(transactions, key=lambda x: x["id"])
        hash_table = build_hash_table(transactions)
        
        # Search for the last element (worst case for linear)
        target_id = transactions[-1]["id"]
        
        linear_time = measure_search_time(linear_search, transactions, target_id)
        binary_time = measure_search_time(binary_search, sorted_tx, target_id)
        hash_time = measure_search_time(hash_lookup, hash_table, target_id)
        
        print(f"{size:>6}  | {linear_time:>10.4f}  | {binary_time:>10.4f}  | {hash_time:>10.4f}")
    
    print()


# ============================================================
# MAIN EXECUTION
# ============================================================
if __name__ == "__main__":
    # Run the main comparison with at least 20 records
    results = run_comparison(num_records=20)
    
    # Run scalability test
    run_scalability_test()
    
    # Print reflection prompts
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
