import logging
import pathlib
import glob
import contextlib
import functools
import time
import signal
from collections import deque
from typing import List
from line_profiler import LineProfiler
import os
import errno
import numpy as np

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s, %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s')

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

class Car:
  F = 0
  street2cars = {}      #
  def __init__(self, streets: List["str"]):
    self.streets = deque(streets)
    self.intersection_id = None
    self.target_distance = Intersection.street2latency[self.streets[0]]
    self.score = None

class Intersection:
  id2intersection = {}
  street2intersect_id = {}  # arrival intersection when using street
  street2latency = {}       # street length
  def __init__(self, id_):
    self.id = id_
    self.schedules = [] # [(street, second), (street, second), (street, second)]

# D (≤ 10^4) : duration of simulation
# I (≤ 10^5) : number of intersection
# S (≤ 10^5) : number of Street
#     B / E (< I) : intersections at the start and end of the street
#     L (≤ D)     : time it takes a car to get from the beginning to end
# V (≤ 10^3) : number of Vehicle
#     P (P ≤ 10^3) - the number of streets that the car wants to travel
#           street ...
# F (≤ 10^3) : bonus points for each car that reaches its destination before time D
#            : beginning to the end of that street
def parse_input(file_name: str) -> (int, int, List["Car"], List["Intersection"]):
  intersections = []
  cars = []
  with open(file_name, "r") as f:
    D, I, S, V, F = map(int, f.readline().split())
    Car.F = F
    for i in range(I):
      intersection = Intersection(i)
      Intersection.id2intersection[i] = intersection
      intersections.append(intersection)
    for i in range(S):
      B, E, street, L = f.readline().split()
      Intersection.street2latency[street] = int(L)
      Intersection.street2intersect_id[street] = int(E)
    for _ in range(V):
      cars.append(Car(f.readline().split()[1:]))
  return D, F, intersections, cars

# A (< I) : number of intersections
# i (< I) : id of the intersection
# Ei      : number of incomming streets covered by this schedule
#
def to_output(file_name: str, intersections: List["Intersection"]):
  with open(file_name, 'w') as f:
    f.write(f"{len(intersections)}\n")
    for intersection in intersections:
      f.write(f"{intersection.id}\n")
      f.write(f"{len(intersection.schedules)}\n")
      for street_id, green_period in intersection.schedules:
        f.write(f"{street_id} {green_period}\n")

class Street:
  def __init__(self, id_, L):
    self.id = id_
    self.score = 0.0
    self.L = L
    self.count = 0

def eunsoo_solution(D: int, F:int, intersections:List['Intersection'], cars: List['Car']):
  street2latency = Intersection.street2latency
  street2interect_id = Intersection.street2intersect_id
  
  for i in intersections:
    i.incoming = []
  
  street_id2street = {}
  for street in street2interect_id:
    L = street2latency[street]
    intersect = intersectionsstreet2interect_id[street]
    street_id2street[street] = Street(street, L)
    intersect.incoming.append(street_id2street[street])

  for c in cars:
    prev = D
    for s in c.streets:
      street_id2street[s].score += (prev - street_id2street[s].L)/D
      prev -= street_id2street[s].L

  for i in intersections:
    schedule = [(i.id, i.score) for s in i.incoming]
    scores = [s[1] for s in schedule]
    total_score = sum(scores)
    score_ratio = [s/total_score for s in scores]
    min_score_ratio = min(score_ratio)
    periods = [int(s/min_score_ratio) for s in score_ratio]
    for s, p in zip(schedule, periods):
      id_ = s[0]
      i.schedules.append((id_, p))
  return intersections
  

def main():
  # for fn in ["input/a.txt", "input/b.txt"]:
  for fn in glob.glob('input/*'):
    logging.info(f"{fn}")
    D, F, intersections, cars = parse_input(fn)
    intersections = eunsoo_solution(D, F, intersections, cars)

    output_fn = f"output/eunsoo_{fn.split('/')[1]}"
    to_output(output_fn, intersections)

if __name__ == "__main__":
  lp = LineProfiler()
  lp_wrapper = lp(main)
  try:
    with timeout(10):
      lp_wrapper()
  finally:
    lp.print_stats()
