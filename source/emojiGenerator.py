import PIL
from PIL import Image
import os
from bookCover import BookHandler

class EmojiGenerator:
    """ 
    This is a class for generating the care emoji. 
      
    Attributes: 

    Methods:
        generateCareEmoji: Generate the emoji with user designated image inside as a Image object.
    """
    def __init__(self):
        # Load emoji file into an Image object
        self.__path = os.path.dirname(os.path.abspath(__file__))
        self.__img_emoji = Image.open(self.__path + "/images/emoji.png")
        self.__img_emoji = self.__img_emoji.convert("RGBA")
        self.__emoji_w, self.__emoji_h = self.__img_emoji.size

        # Load arm file into an Image object
        self.__img_arm = Image.open(self.__path + "/images/arm.png")
        self.__img_arm = self.__img_arm.convert("RGBA")
    
    def rotatingMask(self, img, rotation_angle = -20):
        """ 
        The function gets the rotation mask for the image rotation

        Parameters: 
            img (Image):            The Image object to rotate
            rotation_angle (float): rotation angle

        Returns: 
            Image:                  An Image object of the mask
        """
        img_mask = img.split()[3]
        img_mask = img_mask.rotate(rotation_angle, expand=1)
        return img_mask

    def generateCareEmoji(self, img_item, 
                                rotation_angle = -20, 
                                keep_ratio = True, 
                                img_width = 1000, 
                                img_height = 1000,
                                use_rel_pos = True,
                                rel_position = (0.2, 0.25),
                                abs_position = (0, 0)):
        """ 
        The function generates the emoji

        Parameters: 
            img_item (Image):               The Image object of the item
            rotation_angle (float):         The angle that img_item rotates
            keep_ration (bool):             True to keep the ration of size the item image
            img_width (int):                User designated width for img_item. Will be ignored if keep_ration = True
            img_height (int):               User designated height for img_item
            use_rel_pos (bool):             True to use relative position parameters
            rel_position ((float, float)):  The relative position in the emoji. Will be ignored if use_rel_pos = False
            abs_position ((int, int)):      The absolute position in the emoji. Will be ignored if use_rel_pos = True

        Returns: 
            Image:                          An Image object of the cover
        """
        img_emoji = self.__img_emoji.copy()
    
        img_item = img_item.convert("RGBA")

        # compute the resize parameters
        if keep_ratio:
            book_w, book_h = img_item.size
            new_w = 1000 * book_w // book_h
            new_h = 1000
        else:
            new_w, new_h = img_width, img_height


        img_item = img_item.resize((new_w, new_h), Image.ANTIALIAS)
        img_mask = self.rotatingMask(img_item)
        img_item = img_item.rotate(rotation_angle, expand = 1)

        # compute positions
        if use_rel_pos:
            r_w, r_h = rel_position
            position = (int(self.__emoji_w * r_w), int(self.__emoji_h * r_h))
        else:
            position = abs_position

        # paste the item image
        img_emoji.paste(img_item, position, mask = img_mask)

        # paste the arms
        img_emoji.paste(self.__img_arm, (0, 0), mask = self.__img_arm.split()[3])
        return img_emoji

if __name__ == '__main__':
    #isbn = '9781475738490'
    #emoji = generateBookCareEmoji(getImageByISBN(isbn))
    #emoji.save('output.png')
    
    #isbn2 = '9780024041517'
    #generateBookCareEmoji(getImageByISBN(isbn2)).save('output2.png')
    
    isbn3 = '9781111569624'
    book_cover = BookHandler().getImageByISBN(isbn3)
    EmojiGenerator().generateCareEmoji(book_cover).save('output3.png')
