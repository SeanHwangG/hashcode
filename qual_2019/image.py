from typing import List


class Image:
    def __init__(self, id, tags, orientation):
        assert orientation == 'v' or orientation == 'h'
        self.id = id
        self.tags = tags
        self.orientation = orientation # v / h
    
    @classmethod
    def read_input(cls, file_name) -> List["Image"]:
        images = []
        with open(file_name, "r") as f:
            total = int(f.readline())
            for id in range(total):
                line = f.readline().strip().split()
                orientation = line[0].lower()
                tags = set(line[2:])
                images.append(cls(id, tags, orientation))
        return images

    def __repr__(self):
        return f"Image(id: {self.id}, orientation: {self.orientation}, tags: {self.tags})"

if __name__ == '__main__':
    images = Image.read_input("../d_pet_pictures.txt")