from common import logger
from scorer.get_score import get_score
from typing import List
from collections import Counter
import heapq


"""
heappush(heap, item)
heappop(heap)
heapify(x)                          # Transform list x into a heap, in-place, in linear time
merge(*iterables, key=N, reverse=F) # Merge sorted inputs into a single sorted output
nlargest(n, iterable, key=N)        # return n th largest index and number
nsmallest(n, iterable, key=N)

heapify_lst = [9, 8, 7, 6, 5, 4, 3, 2, 1]
heapify(lst)    # [0, 1, 3, 2, 5, 4, 7, 9, 6, 8]
heappush(lst, 10)
for i in range(k):
  ans = heapq.heappop(lst)

heapq.nsmallest(2, lst)  # n smallest elements

# Counter
from collections import Counter
c = Counter()
c = Counter('gallahad')     # new counter from an iterable
c = Counter({'red': 4, 'blue': 2})  # new counter from a mapping
c = Counter(cats=4, dogs=8)   # keyword args
del c['sausage']

elements()          # iterator over elements repeating count | ignore if less than one
most_common([k])        # Return k most common key value pair in order in O(n log k)
subtract([iterable-or-mapping])   # Subtract another mapping
update([iterable-or-mapping])   # Add another mapping
"""

class Library:
    total_day = 0
    total_book = 0
    total_library = 0
    def __init__(self, id_, books, signin_length, book_per_day):
        self.id = id_
        self.books = books
        self.signin_length = signin_length
        self.book_per_day = book_per_day

    @staticmethod
    def order_library(libraries: List["Library"], type_ = "stage1") -> List["Library"]:
        if type_ == "baseline":
            # Order by shortest singin length
            return list(sorted(libraries, key=lambda l: l.signin_length))
        elif type_ == "stage1":
            # for lib in libraries:
            #     lib.score = len(lib.books) * lib.books_per_day - lib.signin_length
            # return list(sorted(libraries, key=lambda l : l.score, reverse=True))
            return list(sorted(libraries, key=lambda l: (l.signin_length, -l.book_per_day)))

    @staticmethod
    def order_books(libraries, type_="baseline") -> List["Library"]:
        # sort : 
        # update : max_i
        if type_ == "baseline":
            ordered_libraries = []
            cur_day = 0
            for library in libraries:
                cur_day += library.signin_length
                book_capacity = max(Library.total_day - cur_day, 0) * library.book_per_day
                library.books.sort(reverse=True, key = lambda b : b.score)
                library.books = library.books[:book_capacity]
                ordered_libraries.append(library)
            return ordered_libraries
        elif type_ == "": 
            # Donghyun 
            # left_day * book_perday [n_books]
            # score = id
            # Library 1 [5] : 10 7 6 4 3 | 2 0
            # Library 2 [3] : [10] 6 5 | 4 1
            # Library 3 [2] : 3 2 | 1
            libraries = []
            duplicates = []     # [book, [librarys]]

            cur_day = 0

            for library in libraries:
                library.books.sort(key=lambda book: book.score, reverse=True)
                cur_day += library.signin_length   # udpate current date
                book_capacity = max(Library.total_day - cur_day, 0) * library.book_per_day # Ignore duplicate, just copy with highest score first
                Book.book_id2count.update(library.books[:book_capacity])                   # update Counter 

            repeated_book_ids = [book_id for book_id, count in Book.book_id2count.items() if count > 1]    # books more than 2 counts
            while len(repeated_book_ids) > 1:
                pass
                # Update logic

                # Structure : [Book_id, [library_ids]]
                #
                # ex) duplicates = [(0, [A,B]), (2, [A,D,E]), (4, [B,C]), ...]
                # 
                # <PSUEDO CODE>
                #
                # while !duplicates.empty() {
                #   dup = duplicates.pop()
                #      
                #   for library_id in dup.second:
                #       # 1. Select best library to scan the according book
                #       # 2. Remove the book from lists of the rest library
                # }
                

    @staticmethod
    def to_output(libraries, filename):
        with open(filename, 'w') as f:
            f.write(f"{len(libraries)}\n")
            for lib in libraries:
                f.write(f"{lib.id} {len(lib.books)}\n")
                f.write(' '.join(map(lambda b:str(b.id), lib.books))+"\n")


class Book:
    book_id2count = Counter()
    
    def __init__(self, id: int, score: int, library_ids = None):
        self.id = id
        self.score = score
        self.library_ids = library_ids

    def __repr__(self):
        return f"Book(id: {self.id}, score: {self.score})"

def parse_input(file_name: str) -> List["Library"]:
    logger.info(file_name)
    # Eunsoo
    libraries = []   
    with open(file_name, "r") as f:
        n_book, n_library, n_day = map(int, f.readline().split())
        Library.total_day = n_day
        Library.total_book = n_book
        Library.total_library = n_library
        # Book 0 : A B
        #      1
        # Lib  A : 0
        #      B : 0
        books = []
        scores = list(map(int, f.readline().split()))
        for id_, score in enumerate(scores):
            books.append(Book(id_, score))
        for id_ in range(n_library):
            _, signup_time, scan_per_day = map(int, f.readline().split())
            books_in_library_ids = map(int, f.readline().split())
            books_in_library = [books[id_] for id_ in books_in_library_ids]
            library = Library(id_, books_in_library, signup_time, scan_per_day)
            libraries.append(library)
    return libraries

if __name__ == "__main__":
    in_filenames = [ "input/a_example.txt", "input/b_read_on.txt", "input/c_incunabula.txt", "input/d_tough_choices.txt", "input/e_so_many_books.txt", "input/f_libraries_of_the_world.txt"]
    total = 0
    for fn in in_filenames:
        out_fn = "output" + fn[5:]
        libraries = parse_input(fn)
        ordered_libraries = Library.order_library(libraries)          # yoonji Kim est(8:50)
        ordered_libraries_books = Library.order_books(ordered_libraries)
        Library.to_output(ordered_libraries_books, out_fn)
        current = get_score(fn, out_fn)
        logger.info(current)
        total += current
    logger.info(total)
    # 2700
    # order library | order book | score
    # baseline      | baseline   | 68773405
    #               |            | 68773405

            