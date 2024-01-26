import pygame

class Sheet():
    # This function is used for cutting sprite sheets into indviual iamges which are htne put into a list
    def cut(atlas, width, height, sliceStart, sliceEnd):
        #The function takes in a sprite sheet/atlas, a tile width and height, along with a
        #start of slice and end of slice with the otpion to set an ending as false
        cutSheet = []
        counter = 0


        for i in range(int(atlas.get_height() / height)):
            for ii in range(int(atlas.get_width() / width)):
                #the atlas must be made with out blank space and all tiles be the same size or an even fraction
                #function loops through each tile by column then row
                rect = pygame.Rect((ii * width, i  * height), (width, height))
                #the crop of the atlas is done by a rect which gets the postion of the tile with the size of the tile being constant
                #it is then checked if there is a slice and if the tile is in the slice

                if counter >= sliceStart:

                    if sliceEnd == "False":

                        image = atlas.convert_alpha().subsurface(rect)

                        #a pygame image is a surface which you can also blit images onto which can be cropped by a rect
                        # so here the rect is used to crop the atlas at the point of the tile
                        cutSheet.append(image)


                    elif (not counter > sliceEnd) and  sliceEnd >= sliceStart:


                        image = atlas.convert_alpha().subsurface(rect)
                        cutSheet.append(image)
                counter += 1
        #each time a image was made it was apened to a list which is returned

        if len(cutSheet) == 1:
            return cutSheet[0]

            #checks if player is only getting one frame and returns the frame rather than a frame in a list
        else:
            return cutSheet
    def numberSheet(atlas,width,height):
        font = pygame.font.SysFont(None, 24)
        for i in range(int(atlas.get_height() / height)):
            for ii in range(int(atlas.get_width() / width)):
                atlas.blit(font.render(str(i * (atlas.get_width() / width) + ii), True, (255,255,255)), (width * ii, height * i))
        return atlas

    # path ensures that no matter what computer this is being ran on the correct path will be fond
    def path(relativePath):
        return os.path.dirname(__file__)[:-3] + relativePath

class TrueFalseTimer():
    def __init__(self, time):
        self.ogTime = time
        self.currentTime = self.ogTime
        self.ended = False

    def update(self, dt):
        print("dt", dt/1000)
        if self. currentTime > 0:

            self.currentTime -= dt / 1000
        elif not self.ended:
            self.ended = True
    def checkEnded(self):
        return self.ended
    def restart(self):
        self.ended = False
        self.currentTime = self.ogTime







