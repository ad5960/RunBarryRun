import os

import pygame

from constants.window_config import SLOT_SIZE

# Define paths for all the assets
FLASH_ASSET_PATH = os.path.join(os.path.dirname(__file__), "../assets/flash_asset.png")
FLASH_STILL_ASSET_PATH = os.path.join(os.path.dirname(__file__), "../assets/flash_still.png")
OBSTACLE_ASSET_PATH = os.path.join(os.path.dirname(__file__), "../assets/obstacle.png")
FINISH_STILL_ASSET_PATH = os.path.join(os.path.dirname(__file__), "../assets/finish.png")
SEARCH_ASSET_PATH = os.path.join(os.path.dirname(__file__), "../assets/wavesound.png")

# Load and Scale all the assets
FLASH_IMAGE = pygame.image.load(FLASH_ASSET_PATH)
FLASH_IMAGE = pygame.transform.scale(FLASH_IMAGE, (SLOT_SIZE, SLOT_SIZE))

FLASH_STILL_IMAGE = pygame.image.load(FLASH_STILL_ASSET_PATH)
FLASH_STILL_IMAGE = pygame.transform.scale(FLASH_STILL_IMAGE, (SLOT_SIZE, SLOT_SIZE))

OBSTACLE_STILL_IMAGE = pygame.image.load(OBSTACLE_ASSET_PATH)
OBSTACLE_STILL_IMAGE = pygame.transform.scale(OBSTACLE_STILL_IMAGE, (SLOT_SIZE, SLOT_SIZE))

FINISH_STILL_IMAGE = pygame.image.load(FINISH_STILL_ASSET_PATH)
FINISH_STILL_IMAGE = pygame.transform.scale(FINISH_STILL_IMAGE, (SLOT_SIZE, SLOT_SIZE))

SEARCH_STILL_IMAGE = pygame.image.load(SEARCH_ASSET_PATH)
SEARCH_STILL_IMAGE = pygame.transform.scale(SEARCH_STILL_IMAGE, (SLOT_SIZE, SLOT_SIZE))
