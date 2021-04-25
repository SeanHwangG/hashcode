import sys
import logging as log
import json
from math import ceil
from itertools import islice
from line_profiler import LineProfiler
import functools
import contextlib
import errno
import os
import signal
import time


class timeout(contextlib.ContextDecorator):
  def __init__(self, seconds, *, timeout_message=os.strerror(errno.ETIME), suppress_error=False):
    self.seconds = seconds
    self.timeout_message = timeout_message
    self.suppress_error = suppress_error

  def _timeout_handler(self, signum, frame):
    raise TimeoutError(self.timeout_message)

  def __enter__(self):
    signal.signal(signal.SIGALRM, self._timeout_handler)
    signal.alarm(self.seconds)

  def __exit__(self, exc_type, exc_val, exc_tb):
    signal.alarm(0)
    if self.suppress_error and exc_type is TimeoutError:
      return True


log.basicConfig(level=log.DEBUG, format='[%(filename)s:%(lineno)d] %(message)s',)

WEIGHTS = []
CUSTOMERS = []


@functools.lru_cache()
def get_distance(dist1, dist2):
  return ceil(((dist1[0] - dist2[0]) ** 2 + (dist1[1] - dist2[1]) ** 2) ** 0.5)


def move_item_drone2customer(drone, customers):
  customers = sorted(customers, key=lambda customer: get_distance(customer.location, drone.location))
  for customer in customers:
    # [1, 0, 0 ] drone.item_i2count
    # [0, 1, 0 ] drone.item_i2count
    # item_i2count => Counter() [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    #                           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    # 500 item     500 item
    # Counter(a) & Counter(b)
    # {15:24, 26:1} & {13:2, 15:2}
    #     => {15:2}
    for item_i in range(len(WEIGHTS)):
      amnt = min(customer.item_i2count[item_i], drone.item_i2count[item_i])
      if amnt > 0:
        drone.capacity += amnt
        customer.item_i2count[item_i] -= amnt
        print(f"{drone.i} D {customer.i} {item_i} {amnt}")
        return customer, item_i, amnt


def move_item_warehouse2drone(warehouse, drone):
  for i, weight in enumerate(WEIGHTS):
    max_possible = min(warehouse.item_i2count[i], drone.capacity // weight)
    if max_possible:
      print(f"{drone.i} L {warehouse.i} {i} {max_possible}")
      drone.item_i2count[i] += max_possible
      warehouse.item_i2count[i] -= max_possible
      drone.capacity -= max_possible * weight


class Customer:
  def __init__(self, i, location, item_i2count=None):
    self.i = i
    self.location = location
    self.item_i2count = item_i2count

  def __repr__(self):
    return str(self.__dict__)


class Drone:
  def __init__(self, i, location, max_load, finish_time=0, item_i2count=None):
    self.i = i
    self.location = location
    self.capacity = max_load
    self.finish_time = finish_time
    self.item_i2count = [0] * len(WEIGHTS)

  def __repr__(self):
    return f"{self.__dict__}"


class Warehouse:
  def __init__(self, i, location, item_i2count):
    self.i = i
    self.location = location
    self.item_i2count = item_i2count
    self.customer2dist = []

  def __repr__(self):
    return f"{self.__dict__}"

  def precompute_dist(self):
    for customer in CUSTOMERS:
      order_pos = customer.position
      self.customer2dist.append(math.ceil(math.dist(order_pos, self.location)))


def parse_input(filename: str):
  global CUSTOMERS
  global WEIGHTS
  with open(filename, 'r') as f:
    n_row, n_col, n_drone, n_turn, max_load = map(int, f.readline().strip().split())

    weights = int(f.readline().strip())
    WEIGHTS = list(map(int, f.readline().strip().split()))

    num_warehouses = int(f.readline().strip())
    warehouses = []  # [(location, products)]
    for i in range(num_warehouses):
      location = tuple(map(int, f.readline().strip().split()))
      item_i2count = list(map(int, f.readline().strip().split()))
      # warehouses.append((location, item_i2count))
      warehouses.append(Warehouse(i, location, item_i2count))

    num_orders = int(f.readline().strip())
    for i in range(num_orders):
      location = tuple(map(int, f.readline().strip().split()))
      num_products = int(f.readline().strip())
      products = list(map(int, f.readline().strip().split()))
      CUSTOMERS.append(Customer(i, location, [products.count(i) for i in range(len(WEIGHTS))]))  # [(location, products)]

  drones = []
  for i in range(n_drone):
    drones.append(Drone(i, warehouses[0].location, max_load))

  return drones, warehouses, n_turn


# LOAD
# d + 1 turns
# Go to inventory in shortest path
# WAREHOUSE -> INVENTORY

# DELIVER
# d + 1 turns
# Shortest path to customer

# UNLOAD
# d + 1 turns

# WAIT w
# w time


# [INPUT]
# [OUTPUT]
# 9            -> [n_command]
# 0 L 0 0 1    -> Drone_id, Action,

# class Product:
# def __init__(self, weight):
# def get_best_order_by_items(items):

def main():
  files = ["short.in", 'redundancy.in', 'busy_day.in', 'mother_of_all_warehouses.in']
  drones, warehouses, n_turn = parse_input(files[-1])
  answers = []
  for i, turn in enumerate(range(n_turn)):
    if i % 1000 == 10:
      log.debug(f"{i} loop")
      return
    warehouses = list(filter(lambda warehouse: sum(warehouse.item_i2count) != 0, warehouses))
    for i, drone in enumerate(drones):
      if drone.finish_time > turn:  # drone is working
        continue
      # Counter -> len(drone.item_i2count)
      if sum(drone.item_i2count) != 0:  # deliver
        # capa too large || capa + warehouse close
        move_item_drone2customer(drone, CUSTOMERS)
      else:  # load
        warehouse = min(warehouses, key=lambda warehouse: get_distance(warehouse.location, drone.location))
        move_item_warehouse2drone(warehouse, drone)


if __name__ == "__main__":
  lp = LineProfiler()
  lp_wrapper = lp(main)
  try:
    with timeout(10):
      lp_wrapper()
  finally:
    lp.print_stats()
