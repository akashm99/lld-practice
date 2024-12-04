from abc import ABC, abstractmethod
from typing import List, Optional

# Vehicle classes
class Vehicle(ABC):
    def __init__(self, license_plate: str):
        self.license_plate = license_plate

class Car(Vehicle):
    pass

class Motorcycle(Vehicle):
    pass

# Factory for creating vehicles
class VehicleFactory:
    @staticmethod
    def create_vehicle(vehicle_type: str, license_plate: str) -> Vehicle:
        if vehicle_type == 'car':
            return Car(license_plate)
        elif vehicle_type == 'motorcycle':
            return Motorcycle(license_plate)
        else:
            raise ValueError(f"Unknown vehicle type: {vehicle_type}")

# Parking Spot
class ParkingSpot:
    def __init__(self, spot_id: str, size: str, distance_to_entrance: int):
        self.spot_id = spot_id
        self.size = size
        self.distance_to_entrance = distance_to_entrance
        self.vehicle: Optional[Vehicle] = None

    def is_available(self) -> bool:
        return self.vehicle is None

    def park_vehicle(self, vehicle: Vehicle):
        self.vehicle = vehicle

    def remove_vehicle(self) -> Optional[Vehicle]:
        vehicle = self.vehicle
        self.vehicle = None
        return vehicle


# Parking Allocation Strategy
class ParkingAllocationStrategy(ABC):
    @abstractmethod
    def find_spot(self, vehicle: Vehicle, levels: List['ParkingLevel']) -> Optional[ParkingSpot]:
        pass

class FirstAvailableStrategy(ParkingAllocationStrategy):
    def find_spot(self, vehicle: Vehicle, levels: List['ParkingLevel']) -> Optional[ParkingSpot]:
        for level in levels:
            for spot in level.spots:
                if spot.is_available() and self._can_fit(vehicle, spot):
                    return spot
        return None

    def _can_fit(self, vehicle: Vehicle, spot: ParkingSpot) -> bool:
        if isinstance(vehicle, Motorcycle):
            return True
        elif isinstance(vehicle, Car):
            return spot.size in ['compact', 'large']
        return False

class BestFitStrategy(ParkingAllocationStrategy):
    def find_spot(self, vehicle: Vehicle, levels: List['ParkingLevel']) -> Optional[ParkingSpot]:
        best_spot = None
        for level in levels:
            for spot in level.spots:
                if spot.is_available() and self._can_fit(vehicle, spot):
                    if best_spot is None or self._is_better_spot(spot, best_spot):
                        best_spot = spot
        return best_spot

    def _can_fit(self, vehicle: Vehicle, spot: ParkingSpot) -> bool:
        if isinstance(vehicle, Motorcycle):
            return True
        elif isinstance(vehicle, Car):
            return spot.size in ['compact', 'large']
        return False

    def _is_better_spot(self, spot: ParkingSpot, best_spot: ParkingSpot) -> bool:
        size_priority = {'motorcycle': 0, 'compact': 1, 'large': 2}
        return size_priority[spot.size] < size_priority[best_spot.size]

class ClosestToEntranceStrategy(ParkingAllocationStrategy):
    def find_spot(self, vehicle: Vehicle, levels: List['ParkingLevel']) -> Optional[ParkingSpot]:
        closest_spot = None
        for level in levels:
            for spot in level.spots:
                if spot.is_available() and self._can_fit(vehicle, spot):
                    if closest_spot is None or spot.distance_to_entrance < closest_spot.distance_to_entrance:
                        closest_spot = spot
        return closest_spot

    def _can_fit(self, vehicle: Vehicle, spot: ParkingSpot) -> bool:
        if isinstance(vehicle, Motorcycle):
            return True
        elif isinstance(vehicle, Car):
            return spot.size in ['compact', 'large']
        return False


# Parking Lot
class ParkingLot:
    def __init__(self):
        self.levels: List[ParkingLevel] = []

    def add_level(self, level: 'ParkingLevel'):
        self.levels.append(level)

class ParkingLevel:
    def __init__(self, level_id: str):
        self.level_id = level_id
        self.spots: List[ParkingSpot] = []

    def add_spot(self, spot: ParkingSpot):
        self.spots.append(spot)


# Parking Lot Controller
class ParkingLotController:
    def __init__(self, allocation_strategy: ParkingAllocationStrategy):
        self.parking_lot = ParkingLot()
        self.allocation_strategy = allocation_strategy

    def add_parking_spot(self, level_id: str, spot_id: str, size: str, distance_to_entrance: int):
        for level in self.parking_lot.levels:
            if level.level_id == level_id:
                spot = ParkingSpot(spot_id, size, distance_to_entrance)
                level.add_spot(spot)
                return
        new_level = ParkingLevel(level_id)
        spot = ParkingSpot(spot_id, size, distance_to_entrance)
        new_level.add_spot(spot)
        self.parking_lot.add_level(new_level)

    def park_vehicle(self, vehicle: Vehicle) -> str:
        spot = self.allocation_strategy.find_spot(vehicle, self.parking_lot.levels)
        if spot:
            spot.park_vehicle(vehicle)
            return f"Vehicle {vehicle.license_plate} parked in spot {spot.spot_id}"
        return "No available spot"

    def unpark_vehicle(self, spot_id: str) -> str:
        for level in self.parking_lot.levels:
            for spot in level.spots:
                if spot.spot_id == spot_id and not spot.is_available():
                    vehicle = spot.remove_vehicle()
                    return f"Vehicle {vehicle.license_plate} removed from spot {spot_id}"
        return "Spot not found or already empty"


# Usage
if __name__ == "__main__":
    # Initialize the controller with a parking allocation strategy
    controller = ParkingLotController(FirstAvailableStrategy())

    # Add parking spots
    controller.add_parking_spot("Level1", "A1", "compact", 10)
    controller.add_parking_spot("Level1", "A2", "large", 5)
    controller.add_parking_spot("Level1", "A3", "motorcycle", 15)
    controller.add_parking_spot("Level2", "B1", "compact", 20)
    controller.add_parking_spot("Level2", "B2", "large", 25)

    # Create and park vehicles
    car1 = VehicleFactory.create_vehicle("car", "ABC123")
    print(controller.park_vehicle(car1))

    motorcycle1 = VehicleFactory.create_vehicle("motorcycle", "XYZ789")
    print(controller.park_vehicle(motorcycle1))

    # Try to park another car when full
    car2 = VehicleFactory.create_vehicle("car", "DEF456")
    print(controller.park_vehicle(car2))

    # Unpark a vehicle
    print(controller.unpark_vehicle("A1"))

    # Park a new car in the now available spot
    print(controller.park_vehicle(car2))

    # Switch to BestFitStrategy
    controller = ParkingLotController(BestFitStrategy())
    car3 = VehicleFactory.create_vehicle("car", "GHI789")
    print(controller.park_vehicle(car3))

    # Switch to ClosestToEntranceStrategy
    controller = ParkingLotController(ClosestToEntranceStrategy())
    car4 = VehicleFactory.create_vehicle("car", "JKL012")
    print(controller.park_vehicle(car4))
