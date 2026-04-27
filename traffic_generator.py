#!/usr/bin/env python3
"""
API Traffic Generator for SRE Assignment
Simulates organic traffic patterns and includes stress testing capabilities.
"""

import requests
import time
import random
import argparse
import sys
import json
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import signal
import threading


class APITrafficGenerator:
    """Generates realistic traffic patterns for the items API."""

    def __init__(
        self, base_url: str = "http://localhost/api", stress_mode: bool = False
    ):
        self.base_url = base_url
        self.stress_mode = stress_mode
        self.running = False
        self.stats = {
            "requests": 0,
            "successes": 0,
            "failures": 0,
            "start_time": None,
            "errors": {},
        }
        self.lock = threading.Lock()

    def update_stats(self, success: bool, error_type: Optional[str] = None):
        """Thread-safe statistics update."""
        with self.lock:
            self.stats["requests"] += 1
            if success:
                self.stats["successes"] += 1
            else:
                self.stats["failures"] += 1
                if error_type:
                    self.stats["errors"][error_type] = (
                        self.stats["errors"].get(error_type, 0) + 1
                    )

    def get_items(self) -> Optional[list]:
        """GET all items."""
        try:
            response = requests.get(f"{self.base_url}/items", timeout=5)
            if response.status_code == 200:
                self.update_stats(True)
                return response.json()
            else:
                self.update_stats(False, f"GET_ITEMS_{response.status_code}")
                return None
        except requests.RequestException as e:
            self.update_stats(False, f"GET_ITEMS_ERROR_{type(e).__name__}")
            return None

    def get_item(self, item_id: int) -> Optional[Dict[str, Any]]:
        """GET a specific item."""
        try:
            response = requests.get(f"{self.base_url}/items/{item_id}", timeout=5)
            if response.status_code == 200:
                self.update_stats(True)
                return response.json()
            elif response.status_code == 404:
                self.update_stats(True)  # 404 is expected sometimes
                return None
            else:
                self.update_stats(False, f"GET_ITEM_{response.status_code}")
                return None
        except requests.RequestException as e:
            self.update_stats(False, f"GET_ITEM_ERROR_{type(e).__name__}")
            return None

    def update_item(self, item_id: int, name: str) -> Optional[Dict[str, Any]]:
        """PUT update an item."""
        try:
            response = requests.put(
                f"{self.base_url}/items/{item_id}", json={"name": name}, timeout=5
            )
            if response.status_code == 200:
                self.update_stats(True)
                return response.json()
            elif response.status_code == 404:
                self.update_stats(True)
                return None
            else:
                self.update_stats(False, f"UPDATE_ITEM_{response.status_code}")
                return None
        except requests.RequestException as e:
            self.update_stats(False, f"UPDATE_ITEM_ERROR_{type(e).__name__}")
            return None

    def delete_item(self, item_id: int) -> Optional[Dict[str, Any]]:
        """DELETE an item."""
        try:
            response = requests.delete(f"{self.base_url}/items/{item_id}", timeout=5)
            if response.status_code == 200:
                self.update_stats(True)
                return response.json()
            elif response.status_code == 404:
                self.update_stats(True)
                return None
            else:
                self.update_stats(False, f"DELETE_ITEM_{response.status_code}")
                return None
        except requests.RequestException as e:
            self.update_stats(False, f"DELETE_ITEM_ERROR_{type(e).__name__}")
            return None

    def create_item(self, name: str) -> Optional[Dict[str, Any]]:
        """POST create a new item"""
        try:
            response = requests.post(
                f"{self.base_url}/items", json={"name": name}, timeout=5
            )
            if response.status_code == 201 or response.status_code == 200:
                self.update_stats(True)
                return response.json()
            else:
                self.update_stats(False, f"CREATE_ITEM_{response.status_code}")
                return None
        except requests.RequestException as e:
            self.update_stats(False, f"CREATE_ITEM_ERROR_{type(e).__name__}")
            return None

    def print_stats(self):
        """Print current statistics."""
        with self.lock:
            if self.stats["start_time"]:
                elapsed = time.time() - self.stats["start_time"]
                requests_per_second = (
                    self.stats["requests"] / elapsed if elapsed > 0 else 0
                )

                print("\n" + "=" * 60)
                print(f"TRAFFIC GENERATOR STATISTICS")
                print(f"Mode: {'STRESS' if self.stress_mode else 'Organic'}")
                print(f"Running for: {elapsed:.1f}s")
                print(f"Total requests: {self.stats['requests']}")
                print(f"Successful: {self.stats['successes']}")
                print(f"Failed: {self.stats['failures']}")
                print(f"Requests/second: {requests_per_second:.2f}")
                if self.stats["errors"]:
                    print("\nError breakdown:")
                    for error, count in sorted(
                        self.stats["errors"].items(), key=lambda x: x[1], reverse=True
                    ):
                        print(f"  - {error}: {count}")
                print("=" * 60 + "\n")

    def organic_traffic(self, item_ids_cache: list, max_items: int = 100):
        """Simulate organic user traffic patterns."""
        # Random behavior selection with weighted probabilities
        action = random.choices(
            [
                "read_all",
                "read_one",
                "read_one",
                "update",
                "update",
                "create",
                "delete",
                "read_all",
                "read_one",
            ],
            weights=[0.15, 0.20, 0.20, 0.10, 0.10, 0.08, 0.07, 0.05, 0.05],
        )[0]

        if action == "read_all":
            # User browsing all items
            items = self.get_items()
            if items:
                item_ids_cache.clear()
                item_ids_cache.extend([item["id"] for item in items])
                # Small delay to simulate reading
                time.sleep(random.uniform(0.5, 2.0))

        elif action == "read_one":
            # User viewing a specific item
            if item_ids_cache:
                item_id = random.choice(item_ids_cache)
                item = self.get_item(item_id)
                time.sleep(random.uniform(0.3, 1.0))

        elif action == "update":
            # User updating an item
            if item_ids_cache:
                item_id = random.choice(item_ids_cache)
                adjectives = ["Updated", "Modified", "Changed", "Revised", "Edited"]
                items = ["item", "product", "entry", "record", "document"]
                new_name = f"{random.choice(adjectives)} {random.choice(items)} {random.randint(1, 1000)}"
                self.update_item(item_id, new_name)
                time.sleep(random.uniform(0.5, 1.5))

        elif action == "create":
            # User creating a new item
            nouns = [
                "Widget",
                "Gadget",
                "Tool",
                "Device",
                "Component",
                "Module",
                "Unit",
                "Element",
            ]
            adjectives = [
                "New",
                "Fresh",
                "Custom",
                "Special",
                "Premium",
                "Basic",
                "Advanced",
                "Standard",
            ]
            new_name = f"{random.choice(adjectives)} {random.choice(nouns)} {random.randint(1000, 9999)}"
            created = self.create_item(new_name)
            if created and "id" in created:
                item_ids_cache.append(created["id"])
                # Trim cache if it gets too large
                if len(item_ids_cache) > max_items * 2:
                    item_ids_cache = item_ids_cache[-max_items:]
            time.sleep(random.uniform(0.8, 2.0))

        elif action == "delete":
            # User deleting an item
            if item_ids_cache and len(item_ids_cache) > 10:  # Keep at least some items
                item_id = random.choice(item_ids_cache)
                deleted = self.delete_item(item_id)
                if deleted:
                    item_ids_cache.remove(item_id)
                time.sleep(random.uniform(0.5, 1.5))

        # Occasional get all items to refresh cache
        if random.random() < 0.1:  # 10% chance
            items = self.get_items()
            if items:
                item_ids_cache.clear()
                item_ids_cache.extend([item["id"] for item in items])

    def stress_traffic(self, item_ids_cache: list, concurrent_users: int = 5):
        """Simulate high-load traffic pattern for stress testing."""

        def stress_user(user_id: int, cache_ref: list):
            """Simulate a single stressed user making rapid requests."""
            operations = 0
            max_operations = random.randint(10, 30)
            max_items_limit = 200  # Define locally instead of referencing outer scope

            while operations < max_operations and self.running:
                action = random.choices(
                    [
                        "get_all",
                        "get_one",
                        "update",
                        "create",
                        "delete",
                        "random_fail",
                    ],
                    weights=[0.15, 0.25, 0.15, 0.15, 0.15, 0.15],
                )[0]

                if action == "get_all":
                    items = self.get_items()
                    if items and random.random() < 0.3:
                        # Thread-safe cache update
                        with self.lock:
                            cache_ref.clear()
                            cache_ref.extend([item["id"] for item in items[:100]])

                elif action == "get_one":
                    with self.lock:
                        cache_snapshot = cache_ref.copy() if cache_ref else []
                    if cache_snapshot:
                        item_id = random.choice(cache_snapshot)
                        self.get_item(item_id)
                    else:
                        # Try to get items if cache is empty
                        items = self.get_items()
                        if items:
                            with self.lock:
                                cache_ref.clear()
                                cache_ref.extend([item["id"] for item in items[:100]])

                elif action == "update":
                    with self.lock:
                        cache_snapshot = cache_ref.copy() if cache_ref else []
                    if cache_snapshot:
                        item_id = random.choice(cache_snapshot)
                        self.update_item(
                            item_id, f"Stress update {random.randint(1, 10000)}"
                        )

                elif action == "create":
                    # Create new items in stress mode
                    nouns = ["Stress", "Load", "Bulk", "Mass", "Rapid", "Quick"]
                    items = ["Item", "Entry", "Record", "Data", "Object"]
                    new_name = f"{random.choice(nouns)}-{random.choice(items)}-{random.randint(10000, 99999)}"
                    created = self.create_item(new_name)
                    if created and "id" in created:
                        with self.lock:
                            cache_ref.append(created["id"])
                            # Keep cache manageable
                            if len(cache_ref) > max_items_limit:
                                # Trim to keep size manageable
                                excess = len(cache_ref) - 150
                                if excess > 0:
                                    del cache_ref[:excess]

                elif action == "delete":
                    # More aggressive deletion in stress mode to control memory growth
                    with self.lock:
                        cache_snapshot = cache_ref.copy() if cache_ref else []
                    if len(cache_snapshot) > 20:  # Keep minimum items
                        item_id = random.choice(cache_snapshot)
                        deleted = self.delete_item(item_id)
                        if deleted:
                            with self.lock:
                                if item_id in cache_ref:
                                    cache_ref.remove(item_id)

                elif action == "random_fail":
                    # Occasionally request non-existent items to generate 404s
                    fake_id = random.randint(100000, 999999)
                    self.get_item(fake_id)

                operations += 1
                # Very short delays or no delays for stress testing
                time.sleep(random.uniform(0, 0.1))

        # Launch concurrent users
        threads = []
        for i in range(concurrent_users):
            thread = threading.Thread(
                target=stress_user, args=(i, item_ids_cache), daemon=True
            )
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join(timeout=10)

    def run(self, duration_minutes: Optional[int] = None, max_items: int = 500):
        """Main execution loop."""
        self.running = True
        self.stats["start_time"] = time.time()
        item_ids_cache = []

        print(
            f"Starting {'stress' if self.stress_mode else 'organic'} traffic generation..."
        )
        print(f"Base URL: {self.base_url}")
        if duration_minutes:
            print(f"Duration: {duration_minutes} minutes")
        print(f"Max items to track: {max_items}")
        print("Press Ctrl+C to stop\n")

        # Initial populate to have some data
        print("Warming up - fetching initial data...")
        items = self.get_items()
        if items:
            item_ids_cache.extend([item["id"] for item in items[:max_items]])
            print(f"Loaded {len(item_ids_cache)} items")
        else:
            print("Warning: No items found. API might be empty or unavailable.")

        start_time = time.time()
        stats_interval = 10  # Print stats every 10 seconds
        last_stats_time = start_time

        try:
            while self.running:
                # Check duration
                if duration_minutes and (time.time() - start_time) > (
                    duration_minutes * 60
                ):
                    print(
                        f"\nDuration of {duration_minutes} minutes reached. Stopping..."
                    )
                    break

                # Generate traffic based on mode
                if self.stress_mode:
                    # For stress mode, adjust concurrent users based on time
                    # Start with 3, ramp up to 15
                    elapsed = time.time() - start_time
                    max_concurrent = min(15, int(3 + elapsed / 10))
                    concurrent_users = random.randint(3, max_concurrent)
                    self.stress_traffic(item_ids_cache, concurrent_users)

                else:
                    # Organic mode - simulate user think time
                    self.organic_traffic(item_ids_cache, max_items)

                # Print statistics periodically
                if time.time() - last_stats_time >= stats_interval:
                    self.print_stats()
                    last_stats_time = time.time()

        except KeyboardInterrupt:
            print("\n\nReceived interrupt signal. Stopping gracefully...")

        self.running = False
        self.print_stats()
        print("Traffic generation completed.")


def main():
    parser = argparse.ArgumentParser(
        description="API Traffic Generator for Observability Testing",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate organic traffic for 30 minutes
  python traffic_generator.py --mode organic --duration 30
  
  # Generate stress traffic continuously
  python traffic_generator.py --mode stress
  
  # Target a specific server
  python traffic_generator.py --url http://192.168.1.100/api --mode stress
        """,
    )

    parser.add_argument(
        "--url",
        type=str,
        default="http://localhost/api",
        help="Base URL of the API (default: http://localhost/api)",
    )

    parser.add_argument(
        "--mode",
        type=str,
        choices=["organic", "stress"],
        default="organic",
        help="Traffic generation mode (default: organic)",
    )

    parser.add_argument(
        "--duration",
        type=int,
        default=None,
        help="Duration in minutes to run (default: run until interrupted)",
    )

    parser.add_argument(
        "--max-items",
        type=int,
        default=500,
        help="Maximum number of items to keep in cache (default: 500)",
    )

    args = parser.parse_args()

    # Create and run the traffic generator
    generator = APITrafficGenerator(
        base_url=args.url, stress_mode=(args.mode == "stress")
    )

    # Setup signal handler for graceful shutdown
    def signal_handler(signum, frame):
        print("\nSignal received. Shutting down...")
        generator.running = False

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    generator.run(duration_minutes=args.duration, max_items=args.max_items)


if __name__ == "__main__":
    main()
