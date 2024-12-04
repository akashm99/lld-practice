from enum import Enum
from abc import ABC, abstractmethod
from collections import defaultdict

class PackageSize(Enum):
    SMALL = 1
    MEDIUM = 2
    LARGE = 3

class Package:
    def __init__(self, size: PackageSize, customer_id: str):
        self.size = size
        self.customer_id = customer_id

class Locker:
    def __init__(self, locker_id: str, size: PackageSize):
        self.locker_id = locker_id
        self.size = size
        self.package = None

    def is_available(self):
        return self.package is None

    def store_package(self, package: Package):
        self.package = package

    def retrieve_package(self):
        package = self.package
        self.package = None
        return package

class LockerManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LockerManager, cls).__new__(cls)
            cls._instance.lockers_by_size = defaultdict(list)
            cls._instance.lockers_by_customer = {}
        return cls._instance

    def add_locker(self, locker: Locker):
        self.lockers_by_size[locker.size].append(locker)

    def find_available_locker(self, size: PackageSize):
        available_lockers = [locker for locker in self.lockers_by_size[size] if locker.is_available()]
        return available_lockers[0] if available_lockers else None

    def find_locker_by_customer(self, customer_id: str):
        return self.lockers_by_customer.get(customer_id)

    def store_package(self, locker: Locker, package: Package):
        locker.store_package(package)
        self.lockers_by_customer[package.customer_id] = locker

    def retrieve_package(self, customer_id: str):
        locker = self.lockers_by_customer.get(customer_id)
        if locker:
            package = locker.retrieve_package()
            del self.lockers_by_customer[customer_id]
            return package
        return None

class LockerAllocationStrategy(ABC):
    @abstractmethod
    def allocate_locker(self, package: Package, locker_manager: LockerManager):
        pass

class FirstAvailableStrategy(LockerAllocationStrategy):
    def allocate_locker(self, package: Package, locker_manager: LockerManager):
        return locker_manager.find_available_locker(package.size)

class MostAvailableStrategy(LockerAllocationStrategy):
    def allocate_locker(self, package: Package, locker_manager: LockerManager):
        # Find the size category with the most available lockers
        max_available = -1
        best_size = None
        for size, lockers in locker_manager.lockers_by_size.items():
            available_count = sum(1 for locker in lockers if locker.is_available())
            if available_count > max_available:
                max_available = available_count
                best_size = size
        if best_size:
            return locker_manager.find_available_locker(best_size)
        return None

class LockerController:
    def __init__(self, allocation_strategy: LockerAllocationStrategy):
        self.allocation_strategy = allocation_strategy
        self.locker_manager = LockerManager()

    def set_strategy(self, strategy: LockerAllocationStrategy):
        self.allocation_strategy = strategy

    def receive_package(self, package: Package):
        locker = self.allocation_strategy.allocate_locker(package, self.locker_manager)
        if locker:
            self.locker_manager.store_package(locker, package)
            return locker.locker_id
        return "No available locker"

    def retrieve_package(self, customer_id: str):
        package = self.locker_manager.retrieve_package(customer_id)
        return package if package else "Package not found"

# Usage
if __name__ == "__main__":
    locker_manager = LockerManager()
    for size in PackageSize:
        for i in range(5):  # 5 lockers of each size
            locker_manager.add_locker(Locker(f"{size.name}_{i}", size))

    controller = LockerController(FirstAvailableStrategy())

    # Receive a package
    package = Package(PackageSize.SMALL, 'customer_1')
    locker_id = controller.receive_package(package)
    print(f"Package stored in locker: {locker_id}")

    # Switch to MostAvailableStrategy
    controller.set_strategy(MostAvailableStrategy())

    # Receive another package
    package = Package(PackageSize.MEDIUM, 'customer_2')
    locker_id = controller.receive_package(package)
    print(f"Package stored in locker: {locker_id}")

    # Retrieve a package
    retrieved_package = controller.retrieve_package('customer_1')
    print(f"Retrieved package for customer_1: {retrieved_package.customer_id}")
