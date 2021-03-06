from PIL import Image
import numpy as np

import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = [15, 10]

from gym_micropolis.envs.tilemap import zoneFromInt_A
from gym_micropolis.envs.corecontrol import MicropolisControl

# Our dictionnary for the terrains :
tile_initials = {
    "Land":" ",
    "Rubble":".",
    "Road":"#",
    "NuclearPowerPlant":"N",
    "Residential":"R",
    "Commercial":"C",
    "Industrial":"I"
}
tile_nums = {
    "Land": 0,
    "Rubble": 0,
    "Road": 1,
    "NuclearPowerPlant": 2,
    "Residential": 3,
    "Commercial": 4,
    "Industrial": 5
}
tile_nums_sprites = [
    0,  # ground
    76,  # Road
    820,  # Nuclear power plant
    244,  # Residential
    427,  # Commercial
    616   # Industrial
]
# Get all distinct terrains in terrain_str :
# set(sum(str_zones, []))

def saveMapInts(int_zones, filename):
    '''
    function that prints the basic buildings with ascii chars
    :param int_zones: the MicropolisControl.getTileMap() list
    :return:
    '''

    # The int_zones is transposed in the real game
    int_zones = np.transpose(int_zones)
    str_zones = np.zeros(int_zones.shape, dtype=int)

    for x in range(len(int_zones)):
        # We replace those long strings with their initials representation from the dictionnary above
        for y in range(len(int_zones[x])):
            if zoneFromInt_A(int_zones[x][y]) in tile_nums.keys():
                # look up and replace
                str_zones[x][y] = tile_nums[zoneFromInt_A(int_zones[x][y])]
            else:
                str_zones[x][y] = 0

    # Save the array in filename.npy
    np.save(filename, str_zones)

    return

def printMapAscii(int_zones):
    '''
    function that prints the basic buildings with ascii chars
    :param int_zones: the MicropolisControl.getTileMap() list
    :return:
    '''

    # The int_zones is transposed in the real game
    int_zones = np.transpose(int_zones)
    str_zones = []

    for x in range(len(int_zones)):
        # We retrieve the long text version of the zones
        str_zones.append([zoneFromInt_A(int_zones[x][y]) for y in range(len(int_zones[x]))])
        # We replace those long strings with their initials representation from the dictionnary above
        for y in range(len(int_zones[x])):
            if str_zones[x][y] in tile_initials.keys():
                # look up and replace
                str_zones[x][y] = str_zones[x][y].replace(str_zones[x][y], tile_initials[str_zones[x][y]])
            else:
                str_zones[x][y] = '?'

    # We merge the row values into strings
    terr = ["".join(x) for x in str_zones]

    # We print the lines (with a contour for the edges)
    print("-" * (len(terr[0]) + 2))
    for t in terr:
        print("|" + t + "|")
    print(' ' + "-" * len(terr[0]) + ' ')

    return


class SpriteSheetReader:
    '''
    the class used to extract the specific sprite from the tiles sheet
    '''
    def __init__(self, imageName="images/tileEngine/tiles.png", tileSize=16, sheetWidth=16):
        self.imageName = imageName
        self.tileSize = tileSize
        self.sheetWidth = sheetWidth

        self.spritesheet = Image.open(imageName)
        self.tileSize = tileSize
        self.margin = 0

    def getTile(self, tilenum):
        '''
        tilenum is the tilenumber from the functions in  gym_micropolis.envs.tilemap.zoneFromInt_A()
        :param tilenum:
        :return:
        '''
        tileY = tilenum // self.sheetWidth
        tileX = tilenum % self.sheetWidth

        posX = self.tileSize * tileX
        posY = self.tileSize * tileY
        box = (posX, posY, posX + self.tileSize, posY + self.tileSize)
        return self.spritesheet.crop(box)


class SpriteSheetWriter:
    '''
    the class used to construct the terrain sprite after sprite
    '''
    def __init__(self, mapSize, tileSize=16):
        self.tileSize = tileSize
        self.mapSize = mapSize
        self.spritesheet = Image.new("RGB", (self.mapSize * tileSize, self.mapSize * self.tileSize), (0, 0, 0))
        self.tileX = 0
        self.tileY = 0
        self.margin = 0

    def getCurPos(self):
        self.posX = self.tileSize * self.tileX
        self.posY = self.tileSize * self.tileY
        if (self.posX + self.tileSize > self.mapSize * self.tileSize):
            self.tileX = 0
            self.tileY = self.tileY + 1
            self.getCurPos()
        if (self.posY + self.tileSize > self.mapSize * self.tileSize):
            raise Exception('Image does not fit within spritesheet!')

    def addImage(self, image):
        self.getCurPos()
        destBox = (self.posX, self.posY, self.posX + image.size[0], self.posY + image.size[1])
        self.spritesheet.paste(image, destBox)
        self.tileX = self.tileX + 1

    def show(self):
        self.spritesheet.show()

def getMapImage(int_zones):
    '''
    Constructs the png og the pretty micropolis map
    :param int_zones: the MicropolisControl.getTileMap() list
    :return:
    '''

    reader = SpriteSheetReader()
    writer = SpriteSheetWriter(mapSize=len(int_zones))

    # The int_zones is transposed in the real game
    int_zones = np.transpose(int_zones)
    for row in int_zones:
        for tile in row:
            writer.addImage(reader.getTile(tile))
    return writer.spritesheet

def showMap(m, generated=False):
    '''
    easier function to call to matplotlib a city map
    in fact you would only need an array of ints retrieved from gym_micropolis.envs.tilemap.zoneFromInt_A()
    but for me it was always a MicropolisControl that filled it so I made it easier this way
    :param m: a MicropolisControl instance
    :param generated True if the m is a int array to be transposed using tile_nums_sprites, false if m is a MicropolisEngine
    :return:
    '''
    if generated :
        ints = m
        # Transpose the ints to their corresponding image index
        for x in range(len(m)):
            for y in range(len(m[x])):
                ints[x][y] = tile_nums_sprites[m[x][y]]
    else :
        ints = m.getTileMap()

    fig = plt.imshow(np.asarray(getMapImage(ints)))
    plt.axis('off')
    fig.axes.get_xaxis().set_visible(False)
    fig.axes.get_yaxis().set_visible(False)
#     plt.show()
    return

def plotResults(q):
    '''
    prints 3 plots : the pop_progression, the initial plan, and the city map after simulation
    :param q: a quimby class instance
    :return:
    '''
    q.print_param()

    # PLOT 1
    plt.subplot(1, 3, 1)
    plt.plot(q.pop_progression)
    plt.title('best score by generation')
    plt.ylabel('score')


    city = q.genomes[np.argmax(q.populations)]
    m = q.build_city(city=city, display=False)

    # PLOT 2
    plt.subplot(1, 3, 2)
    plt.imshow(np.asarray(getMapImage(m.getTileMap())))
    plt.title('best city plan')
    plt.axis('off')

    # Run simulation for steps
    for i in range(q.n_steps_evaluation):
        m.engine.simTick()

    # PLOT 3
    plt.subplot(1, 3, 3)
    plt.imshow(np.asarray(getMapImage(m.getTileMap())))
    plt.title('best city plan after simulation')
    plt.axis('off')

    m.close()

    # END
    plt.tight_layout()
    plt.figure(figsize=(15, 5))
    plt.show()

    return


