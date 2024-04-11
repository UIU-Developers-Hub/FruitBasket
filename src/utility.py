windowConfig = (480, 720)  # Window dimensions

fontSize = 50  # Font size for text rendering

folderPaths = {
    "fruit": "assets/fruits/",  # Folder path for fruit assets
    "bug": "assets/bugs/",  # Folder path for bug assets
}

filePaths = {
    "font": "assets/font/Pixeltype.ttf",  # Path to the font file
    "bg": "assets/bg/bg.jpg",  # Path to the background image
    "player": "assets/player/basket.png"  # Path to the player image
}

levelWiseParameters = {
    1: {
        "fruitG": 330,  # Gravity for fruits in level 1
        "bugG": 333,  # Gravity for bugs in level 1
        "playerSpd": 30,  # Player speed in level 1
        "fruitSpwanLimit": 3,  # Maximum number of fruits spawned in level 1
        "bugSpwanLimit": 2  # Maximum number of bugs spawned in level 1
    },
    2: {
        "fruitG": 390,  # Gravity for fruits in level 2
        "bugG": 363,  # Gravity for bugs in level 2
        "playerSpd": 40,  # Player speed in level 2
        "fruitSpwanLimit": 4,  # Maximum number of fruits spawned in level 2
        "bugSpwanLimit": 3  # Maximum number of bugs spawned in level 2
    },
    3: {
        "fruitG": 400,  # Gravity for fruits in level 3
        "bugG": 393,  # Gravity for bugs in level 3
        "playerSpd": 60,  # Player speed in level 3
        "fruitSpwanLimit": 5,  # Maximum number of fruits spawned in level 3
        "bugSpwanLimit": 4  # Maximum number of bugs spawned in level 3
    },
    4: {
        "fruitG": 420,  # Gravity for fruits in level 4
        "bugG": 403,  # Gravity for bugs in level 4
        "playerSpd": 65,  # Player speed in level 4
        "fruitSpwanLimit": 5,  # Maximum number of fruits spawned in level 4
        "bugSpwanLimit": 4  # Maximum number of bugs spawned in level 4
    },
    5: {
        "fruitG": 530,  # Gravity for fruits in level 5
        "bugG": 453,  # Gravity for bugs in level 5
        "playerSpd": 70,  # Player speed in level 5
        "fruitSpwanLimit": 5,  # Maximum number of fruits spawned in level 5
        "bugSpwanLimit": 5  # Maximum number of bugs spawned in level 5
    }
}
