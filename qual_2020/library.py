class Book:
    def __init__(self, id: int, score: int):
        self.id = id
        self.score = score

    def __repr__(self):
        return f"Book(id: {self.id}, score: {self.score})"




class Library:
    def __init__(self, books):
        self.books = books

    @staticmethod
    def order_library(libraries: List["Library"], type_ = "baseline") -> List["Library"]:
        if type_ == "baseline":
            # Sean est(8:20)
            return libraries
        elif type_ == "":

            pass

    @staticmethod
    def order_books(libraries, type_="baseline"):
        if type_ == "baseline":
            # Sean est(8:30)
            pass
        elif type_ == "": 
            # Donghyun 


            # Structure : (book_id, (libray_ids))
            # duplicates = [(0, (A,B)), (2, (A,D,E)), (4, (B,C)), ...]
            #
            # PSUEDO CODE
            #
            # while !duplicates.empty() {
            #   dup = duplicates.pop()
            #      
            #   for library_id in dup.second:
            #       # 1. Select best library to scan
            #       # 2. Remove the book from the rest and book_capacity++
            # }

            duplicates = []     # [book, [libraries]]
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

            pass

    @staticmethod
    def get_score(libraries):
        scorer.get_score.main()  # Call the main function

    @staticmethod
    def to_output(libraries, file_nmae):
        pass


"""
void order_books(std::vector<std::vector<Book>> libraries) {
    std::map<int, std::vector<int>> duplicates;
    

    
    // NEED TO SORT init
    
    // 1. Form duplicates
    for (int idx = 0; idx < libraries.size(); idx += 2) {
        
        std::vector<Book> lib1 = libraries.at(idx);
        std::vector<Book> lib2 = libraries.at(idx+1);
        
        // NEED TO SORT lib1 & lib2

        // get duplicate book b/w lib1 and lib2 (PYTHON) 
        // Update Counter & check book w count == 2
        // repeated_book_ids = [book_id for book_id, count in Book.book_id2count.items() if count > 1] 
        
        while len(repeated_book_ids) > 0 {
            int book_id = repeated_book_ids.at(0);
            
            auto it = mymap.find(book_id);
            
            if (it == mymap.end()) {
                std::vector<int> libs;
                lib.push_back(idx);
                lib.push_back()
                duplicates.insert(book_id, libs);
            }
            else {
                
            }
            
            repeated_book_ids.pop_front();
        }
    }
    
    // 2. Edit libraries
    while (!duplicates.empty()) {
        
    }
    
}


"""