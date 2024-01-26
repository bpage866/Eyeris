
class PickUpsHolder():
    def __init__(self):
        self.pickups = []

    def update(self, playerPostion, drops):
        for drop in drops:
            self.pickups.append(drop)
        for pickUp in self.pickups:
            pickUp.update(playerPostion)
    def addItems(self, items):
        for drop in items:
            self.pickups.append(drop)
    def setScreenOffset(self, offset):
        for pickUp in self.pickups:
            pickUp.setScreenOffset(offset)
    def render(self, screen):
        for pickUp in self.pickups:
            pickUp.render(screen)

    def returnIfItemsPickedUp(self):
        returning = []
        for pickUp in self.pickups:
            if pickUp.pickedUp:
                #if a item has considered itself picked up and this is ran only when items can be picked up
                #the item is returned while being removed from here so it no longer affected by these functions
                returning.append(pickUp)
                self.pickups.remove(pickUp)
        return returning

