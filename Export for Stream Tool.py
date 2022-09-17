__author__ = "Dox"
__version__ = "1.0.0"

import sys
from mawwwkLib import getChildFromName
from BrawlCrate.API import BrawlAPI
from BrawlLib.SSBB.ResourceNodes import *
from BrawlCrate.NodeWrappers import *
from System.IO import Directory

renderDict = {
    'Misc Data [0]': 'Mario',
    'Misc Data [1]': 'Donkey Kong',
    'Misc Data [2]': 'Link',
    'Misc Data [3]': 'Samus',
    'Misc Data [4]': 'Yoshi',
    'Misc Data [5]': 'Kirby',
    'Misc Data [6]': 'Fox',
    'Misc Data [7]': 'Pikachu',
    'Misc Data [8]': 'Luigi',
    'Misc Data [9]': 'Captain Falcon',
    'Misc Data [10]': 'Ness',
    'Misc Data [11]': 'Bowser',
    'Misc Data [12]': 'Peach',
    'Misc Data [13]': 'Zelda',
    'Misc Data [14]': 'Sheik',
    'Misc Data [15]': 'Ice Climbers',
    'Misc Data [16]': 'Marth',
    'Misc Data [17]': 'Mr. Game & Watch',
    'Misc Data [18]': 'Falco',
    'Misc Data [19]': 'Ganondorf',
    'Misc Data [21]': 'Meta Knight',
    'Misc Data [22]': 'Pit',
    'Misc Data [23]': 'Zero Suit Samus',
    'Misc Data [24]': 'Olimar',
    'Misc Data [25]': 'Lucas',
    'Misc Data [26]': 'Diddy Kong',
    'Misc Data [27]': 'Mewtwo',
    'Misc Data [28]': 'Charizard',
    'Misc Data [29]': 'Squirtle',
    'Misc Data [30]': 'Ivysaur',
    'Misc Data [31]': 'King Dedede',
    'Misc Data [32]': 'Lucario',
    'Misc Data [33]': 'Ike',
    'Misc Data [34]': 'Rob',
    'Misc Data [36]': 'Jigglypuff',
    'Misc Data [37]': 'Wario',
    'Misc Data [39]': 'Roy',
    'Misc Data [40]': 'Toon Link',
    'Misc Data [43]': 'Knuckles',
    'Misc Data [43]': 'Wolf',
    'Misc Data [45]': 'Snake',
    'Misc Data [46]': 'Sonic'
}

stockDict = {
    0: 'Mario',
    50: 'Donkey Kong',
    100: 'Link',
    150: 'Samus',
    200: 'Yoshi',
    250: 'Kirby',
    300: 'Fox',
    350: 'Pikachu',
    400: 'Luigi',
    450: 'Captain Falcon',
    500: 'Ness',
    550: 'Bowser',
    600: 'Peach',
    650: 'Zelda',
    700: 'Sheik',
    750: 'Ice Climbers',
    800: 'Marth',
    850: 'Mr. Game & Watch',
    900: 'Falco',
    950: 'Ganondorf',
    1050: 'Meta Knight',
    1100: 'Pit',
    1150: 'Zero Suit Samus',
    1200: 'Olimar',
    1250: 'Lucas',
    1300: 'Diddy Kong',
    1350: 'Mewtwo',
    1400: 'Charizard',
    1450: 'Squirtle',
    1500: 'Ivysaur',
    1550: 'King Dedede',
    1600: 'Lucario',
    1650: 'Ike',
    1700: 'Rob',
    1800: 'Jigglypuff',
    1850: 'Wario',
    1950: 'Roy',
    2000: 'Toon Link',
    2100: 'Knuckles',
    2150: 'Wolf',
    2200: 'Giga Bowser',
    2250: 'Snake',
    2300: 'Sonic',
    9000: 'Wario Man'
}
 
# takes in '1' and returns 'Mario (1)' etc
def getStockImageName(stockNum):
    for num in sorted(stockDict.keys(), reverse=True):
        if stockNum > num:
            return str(stockDict[num]), ' ('  + str(stockNum - num) + ')'


# renders: MenSelchrFaceB.001 (ARC char_bust_tex_lz77 -> BRES Misc Data [X])
def exportRenders(node, baseFolder):
    renderDir = baseFolder + '/Renders'
    Directory.CreateDirectory(renderDir)
    for childNode in node.Children:
        if childNode.Name not in renderDict:
            continue
        character = renderDict[childNode.Name]
        charRenderDir = renderDir + '/' + character
        Directory.CreateDirectory(charRenderDir)
        charNum = 1
        for textureNode in getChildFromName(childNode, 'Textures(NW4R)').Children:
            fileName = ''.join([character, ' (', str(charNum), ').png'])
            textureNode.Export(charRenderDir + '/' + fileName)
            charNum += 1

def exportStocks(node, baseFolder):
    stockDir = baseFolder + '/Stock Icons'
    Directory.CreateDirectory(stockDir)
    prevCharName = ''
    for textureNode in getChildFromName(node, 'Textures(NW4R)').Children:
        stockName = textureNode.Name
        stockNum = int(stockName.split('.')[-1])
        charName, charStockNum = getStockImageName(stockNum)
        if prevCharName != charName:
            charStockDir = stockDir + '/' + charName
            Directory.CreateDirectory(charStockDir)
            prevCharName = prevCharName
        fileName = charName + charStockNum + '.png'
        textureNode.Export(charStockDir + '/' + fileName)

# css: MenSelchrChrFace.001
# stock icons: InfStc.1660 (BRES Misc Data [90])

# Main function
if BrawlAPI.RootNode != None: # If there is a valid open file
    if BrawlAPI.RootNode.Name != 'sc_selcharacter_en':
        BrawlAPI.ShowError('Plugin must be run on sc_selcharacter.pac','Error')
    else:
        root = BrawlAPI.RootNode
        folder = BrawlAPI.OpenFolderDialog()
        count = 1
        if folder:
            nodes = BrawlAPI.NodeList # Get the wrapper of every node in the file (export filters are contained in wrappers)
            for node in nodes:
                if node.Name == 'char_bust_tex_lz77':
                    exportRenders(node, folder)
                elif node.Name == 'Misc Data [90]':
                    exportStocks(node, folder)
            if count: # If any textures are found, show the user a success message
                BrawlAPI.ShowMessage("Textures were successfully exported to " + folder, "Success")
            else: # If no textures are found, show an error message
                BrawlAPI.ShowError('No textures were found in the open file','Error')
else: # Show an error message if there is no valid file open
    BrawlAPI.ShowError('Cannot find Root Node (is a file open?)','Error')