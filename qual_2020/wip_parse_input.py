from main import Book, Library
from scorer.get_score import get_score

def parse_input(file_name):
    # Eunsoo
    libraries = []
    with open(file_name, "r") as f:
        n_book, n_library, n_day = map(int, input().split())
        books = [Book(id_, score) for id_, score in enumerate(map(int, input().split()))]
        for id_ in range(n_library):
            _, signup_time, scan_per_day = map(int, input().split())
            books_in_library_ids = map(int, input().split())
            books_in_library = [books[id_] for id_ in books_in_library_ids]
            library = Library(id_, books_in_library, signup_time, scan_per_day)
            libraries.append(library)
    return libraries

# 2
# 1 3
# 5 2 3
# 0 5
# 0 1 2 3 
def to_output(libraries, filename):
    with open(filename, 'w') as f:
        f.write(f"{len(libraries)}\n")
        for lib in libraries:
            f.write(f"{lib.id} {len(lib.books)}\n")
            f.write(' '.join(map(lambda b:str(b.id), lib.books))+"\n")

if __name__ == '__main__':
    libraries = parse_input("./input/a_example.txt")
    to_output(libraries, "./output/a_example.out")
    print(get_score("./input/a_example.txt", "./output/a_example.out"))
    # for l in libraries:
    #     print("Library")
    #     print("id", l.id)
    #     print("signin_length", l.signin_length)
    #     print("book_per_day", l.book_per_day)
    #     for b in l.books:
    #         print('  - ',b)
    #     print()
    