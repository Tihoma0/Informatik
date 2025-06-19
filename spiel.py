# Importieren der Pygame-Bibliothek
import pygame
# initialisieren von pygame
pygame.init()
# genutzte Farbe
ORANGE  = ( 255, 140, 0)
ROT     = ( 255, 0, 0)
GRUEN   = ( 0, 255, 0)
SCHWARZ = ( 0, 0, 0)
WEISS   = ( 255, 255, 255)
# Fenster öffnen
screen = pygame.display.set_mode((640, 480))
# Titel für Fensterkopf
pygame.display.set_caption("Unser erstes Pygame-Spiel")
