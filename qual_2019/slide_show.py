import pandas
import random
from common import logger
from typing import List
from image import Image
from slide import Slide
from collections import Counter

N_RANDOM = 500

# A : 12345
# B : 34567
# C : 67812
# A - B
# B - A
# A - C

class SlideShow:
    def __init__(self, slides: List["Slide"]):
        assert isinstance(slides, list)
        self.slides = slides
    
    @classmethod
    def combine_slides(cls, slides: List["Slide"], mode="baseline") -> "SlideShow":
        logger.info(len(slides))
        start = slides.pop()
        ordered_slides = [start]
        i = 0
        if mode == "baseline":
            # shuffle
            while len(slides) > N_RANDOM:
                i += 1
                if i % 1000 == 0:
                    print(i)
                sample_slides = slides[:N_RANDOM]
                slides = slides[N_RANDOM:]
                highest, rests = ordered_slides[-1].pick_highest(sample_slides)
                ordered_slides.append(highest)
                slides.extend(rests)
            ordered_slides.extend(slides)
        logger.info(len(ordered_slides))
        return cls(ordered_slides)

    def get_score(self):
        return sum(Slide.get_score(self.slides[i], self.slides[i + 1]) for i in range(len(self.slides) - 1))
    
    def visualize_items(self):
        letter_counts = Counter()
        df = pandas.DataFrame.from_dict(letter_counts, orient='index')
        df.plot(kind='bar')
    
    def serialize(self, file_name):
        with open(file_name, "w") as f:
            f.write(f"{len(self.slides)}\n")
            for slide in self.slides:
                f.write(" ".join(map(str, slide.image_ids)) + "\n")


if __name__ == "__main__":
    total_score = 0
    from pathlib import Path
    for data in Path("data").glob("*"):
        images = Image.read_input(data)
        slides = Slide.combine_images(images, "minimum_intersection")
        slide_show = SlideShow.combine_slides(slides, "baseline")
        score = slide_show.get_score()
        total_score += score
        logger.info(total_score)
        slide_show.serialize("output.txt")