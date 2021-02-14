import pandas
from typing import List, Set
from collections import Counter
from common import logger
from itertools import islice
import random

N_RANDOM = 500

class Slide:
    def __init__(self, image_ids: List[int], tags: Set[str], orientation=None):
        assert isinstance(image_ids, list)
        self.image_ids = image_ids  # only 2 if verticals combined
        self.tags = tags
    
    @property
    def id(self):
        return "_".join(self.image_ids)
    
    @classmethod
    def combine_images(cls, images: List["Image"], mode="uncombined") -> List["Slide"]:
        assert isinstance(images, list)
        if mode == "uncombined":
            return [cls([image.id], image.tags, orientation=image.orientation) for image in images]
        elif mode == "baseline":
            return cls._combine_images_baseline(images)
        elif mode == "minimum_intersection":
            return cls._combine_images_minimum_intersction(images)
        slides = []
        return slides
    
    @classmethod
    def _combine_images_minimum_intersction(cls, images: List["Image"]) -> List["Slide"]:
        assert isinstance(images, list)
        
        slides = []
        # insert horizontal photos
        vertical_images = []
        for image in images:
            if image.orientation == 'v':
                vertical_images.append(image)
            else:
                slides.append(cls([image.id], image.tags))
        
        # combine 2 vertical photos and insert
        shuffle_period = 0
        while len(vertical_images) > 1:
            # shuffle only when period is less than 1
            if shuffle_period < 1:
                random.shuffle(vertical_images)
                shuffle_period = len(vertical_images) / N_RANDOM
            shuffle_period -= 1
            
            # random select
            selected = vertical_images[:N_RANDOM]
            vertical_images = vertical_images[N_RANDOM:]
            
            # find minimum intersction image
            this_image = selected[0]
            min_tags_length = len(this_image.tags & selected[1].tags)
            min_candidate_idx = 1

            for candidate_idx in range(2, len(selected)):
                candidate = selected[candidate_idx]
                tags_length = len(this_image.tags & candidate.tags)
                if tags_length < min_tags_length:
                    min_tags_length = tags_length
                    min_candidate_idx = candidate_idx
            
            # insert combined slicde
            candidate = selected[min_candidate_idx]
            slides.append(cls([this_image.id, candidate.id], this_image.tags|candidate.tags))

            # append back to selected images
            vertical_images.extend(selected[1:min_candidate_idx])
            vertical_images.extend(selected[min_candidate_idx+1:])
        return slides

    @classmethod
    def _combine_images_baseline(cls, images: List["Image"]) -> List["Slide"]:
        assert isinstance(images, list)
        slides = []
        vertical_images = []
        for image in images:
            if image.orientation == 'v':
                vertical_images.append(image)
            else:
                slides.append(cls([image.id], image.tags))
        prev_image = None
        for image in vertical_images:
            if prev_image is None:
                prev_image = image
                continue
            slides.append(cls([image.id, prev_image.id], image.tags|prev_image.tags))
            prev_image = None
        return slides
    
    def __repr__(self):
        return f"Slide(id: {self.image_ids}, tags: {self.tags})"

    @staticmethod
    def get_score(slide1, slide2):
        return min(len(slide1.tags & slide2.tags), len(slide1.tags - slide2.tags), len(slide2.tags - slide1.tags)) 
    
    @staticmethod
    def to_df(slides, top):
        tag2count = Counter()
        logger.info(len(slides))
        for slide in islice(slides, 1000):
            cur_count = Counter(slide.tags)
            tag2count = tag2count | cur_count
        
        return tag2count # pandas.DataFrame.from_dict(tag2count.most_common(10))
    
    def pick_highest(self, slides):
        max_idx, max_slide = max(enumerate(slides), key = lambda slide: Slide.get_score(self, slide[1]))
        # logger.debug(f"Picked {max_idx} score +  {Slide.get_score(self, slides[max_idx])}")
        return max_slide, slides[:max_idx] + slides[max_idx + 1:]

# for test
if __name__ == '__main__':
    from image import Image
    images = Image.read_input("./d_pet_pictures.txt")
    slides = Slide.combine_images(images, "minimum_intersction")
    print(slides[-5:])