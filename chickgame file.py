# Importieren der Pygame-Bibliothek
import pygame, math

# initialisieren von pygame
pygame.init()


###---Variablen und Konstanten---###
# genutzte Farbe
ORANGE  = ( 255, 140, 0)
ROT     = ( 255, 0, 0)
GRUEN   = ( 0, 255, 0)
SCHWARZ = ( 0, 0, 0)
WEISS   = ( 255, 255, 255)

BGcolor = SCHWARZ # Hintergrundfarbe

### --- Textbox unten --- ###
info_height = 30


#Texte
txtaktion_eatdand = "LÖWENZAHN ESSEN"
txt_aktion_eatstrawb = "ERDBEERE ESSEN"
txtin_space_content = ""
txtin_space = f"Drücke LEERTASTE zum Aktion: {txtin_space_content} auszuführen"
txtin_wasd = "Bewege dich mit W, A, S und D"
txtin_unessbar = "Sieht nicht mehr so lecker aus..."



curr_txt = txtin_wasd


### --- Fensterbreite, -hoehe und Grid-Einstellungen
# Fensterbreite
FENSTERBREITE = 1100 ### Umstellbar, entweder 1080 oder 1100
FENSTER_PADDING = 10 ### nicht Umstellbar

# Grid-bewegung 
schrittzahl = 12
### Wenn Fensterbreite = 1080, dann 32, 24, 16 oder 8.  Wenn Fensterbreite = 1100, dann 18, 12, oder 6
schrittweite_temp = FENSTERBREITE - 2*FENSTER_PADDING
schrittweite = schrittweite_temp / schrittzahl

# Fensterhoehe
y_ratio = 2/3
zeilen = int(schrittzahl * y_ratio)
FENSTERHOEHE = zeilen * schrittweite + 2 * FENSTER_PADDING + info_height - schrittweite

# Zeit Management
bewegung_delay = 200  # Millisekunden pro Schritt
letzte_bewegung = 0
letzte_taste = None

### --- Charaktere und Spielsteine --- ###
# Was Chick braucht
charpos_x =  schrittweite + FENSTER_PADDING
charpos_y =  schrittweite + FENSTER_PADDING + info_height

CHAR_DURCHMESSER = schrittweite

bewegung_x = schrittweite
bewegung_y = schrittweite
blickrichtung = "front"   # front = vorne, back = hinten

#Spielsteine
dand_hoehe_temp = schrittweite /5 
dand_hoehe = dand_hoehe_temp *4
dand_hoehe_curr = dand_hoehe
dand_breite = schrittweite
dand_breite_curr = dand_breite
dandpos_x = 5*schrittweite + FENSTER_PADDING
dandpos_y = 3*schrittweite + FENSTER_PADDING + info_height
dand_eat_count = 0
dand_visible = True
dand_eat_start_time = 0

ESS_DAUER = bewegung_delay * 5


strawb_hoehe_temp = schrittweite /5 
strawb_hoehe = schrittweite
strawb_hoehe_curr = dand_hoehe
strawb_breite = schrittweite
strawb_breite_curr = strawb_breite
strawbpos_x = 3*schrittweite + FENSTER_PADDING
strawbpos_y = 3*schrittweite + FENSTER_PADDING + info_height
strawb_eat_count = 0
strawb_visible = True
strawb_eat_start_time = 0

# Slide-Bewegung
slide_speed = 10
ziel_x = charpos_x
ziel_y = charpos_y
bewegt_sich = False



### --- Fenster öffnen --- ###
screen = pygame.display.set_mode((FENSTERBREITE, FENSTERHOEHE))

# Animation
chick_front_img = pygame.image.load("chickfront.png").convert_alpha()
chick_back_img  = pygame.image.load("chickback.png").convert_alpha()
chick_toright_img  = pygame.image.load("chicktoright.png").convert_alpha()
chick_toleft_img  = pygame.image.load("chicktoleft.png").convert_alpha()

dandelion_img  = pygame.image.load("dandelion.png").convert_alpha()
dandelion_eaten_img = pygame.image.load("dandelion_eaten.png").convert_alpha()
strawberry_img = pygame.image.load("strawberry.png").convert_alpha()
strawberry_eaten_img = pygame.image.load("strawberry_eaten.png").convert_alpha()

#Charakter

chick_front = pygame.transform.scale(
    chick_front_img,
    (int(CHAR_DURCHMESSER), int(CHAR_DURCHMESSER))
)

chick_back = pygame.transform.scale(
    chick_back_img,
    (int(CHAR_DURCHMESSER), int(CHAR_DURCHMESSER))
)

chick_toright = pygame.transform.scale(
    chick_toright_img,
    (int(CHAR_DURCHMESSER), int(CHAR_DURCHMESSER))
)

chick_toleft = pygame.transform.scale(
    chick_toleft_img,
    (int(CHAR_DURCHMESSER), int(CHAR_DURCHMESSER))
)

chick_allpos = chick_front

#Spielsteine

dandelion = pygame.transform.scale(
    dandelion_img,
    (int(dand_breite), int(dand_hoehe))
)

dandelion_eaten = pygame.transform.scale(
    dandelion_eaten_img,
    (int(dand_breite), int(dand_hoehe))
)

dand_eat_status = "not eaten"

strawberry = pygame.transform.scale(
    strawberry_img,
    (int(strawb_breite), int(strawb_hoehe))
)

strawberry_eaten = pygame.transform.scale(
    strawberry_eaten_img,
    (int(strawb_breite), int(strawb_hoehe))
)

strawb_eat_status = "not eaten"



### --- Info zum Fenster öffnen --- ###
pygame.display.set_caption('Sophias "Chick grid" projekt')
spielaktiv = True
clock = pygame.time.Clock()

### --- Schleife Hauptprogramm --- ###
while spielaktiv:
    # Überprüfen, ob Nutzer eine Aktion durchgeführt hat
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            spielaktiv = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                spielaktiv = False
            #if event.key == pygame.K_d or pygame.K_a or pygame.K_w or pygame.K_s or pygame.K_SPACE:
            if event.key in (pygame.K_d, pygame.K_a, pygame.K_w, pygame.K_s, pygame.K_SPACE):
                letzte_taste = event.key
            elif event.type == pygame.KEYUP:
                if event.key in (pygame.K_d, pygame.K_a, pygame.K_w, pygame.K_s, pygame.K_SPACE):
                    letzte_taste = None
    
    #Zeit abfragen (für bewegung)
    aktuelle_zeit = pygame.time.get_ticks()

    # Tastenzustand abfragen (für Bewegung)
    if letzte_taste and aktuelle_zeit - letzte_bewegung >= bewegung_delay:
        # X-Richtung
        if letzte_taste == pygame.K_d and charpos_x + bewegung_x <= FENSTERBREITE - CHAR_DURCHMESSER - FENSTER_PADDING:
            ziel_x = charpos_x + bewegung_x
            bewegt_sich = True
            blickrichtung = "toright"
            chick_allpos = chick_toright
            letzte_bewegung = aktuelle_zeit
        elif letzte_taste == pygame.K_a and charpos_x - bewegung_x >= FENSTER_PADDING:
            ziel_x = charpos_x - bewegung_x
            bewegt_sich = True
            blickrichtung = "toleft"
            chick_allpos = chick_toleft
            letzte_bewegung = aktuelle_zeit
        # Y-Richtung
        elif letzte_taste == pygame.K_s and charpos_y + bewegung_y <= FENSTERHOEHE - CHAR_DURCHMESSER - FENSTER_PADDING:
            ziel_y = charpos_y + bewegung_y
            blickrichtung = "front"
            chick_allpos = chick_front
            bewegt_sich = True
            letzte_bewegung = aktuelle_zeit
        elif letzte_taste == pygame.K_w and charpos_y - bewegung_y >= FENSTER_PADDING:
            ziel_y = charpos_y - bewegung_y
            blickrichtung = "back"
            chick_allpos = chick_back
            bewegt_sich = True
            letzte_bewegung = aktuelle_zeit
        
# ist Küken auf dem löwenzahn?
        if letzte_taste == pygame.K_SPACE:
            if charpos_x == dandpos_x and charpos_y == dandpos_y: 
                txtin_space_content = txtaktion_eatdand
                blickrichtung = "front"
                if dand_eat_count == 1 and pygame.time.get_ticks() - dand_eat_start_time >= ESS_DAUER:
                    dand_visible = False
                    dand_eat_count = 0
                    dand_eat_status = "not eaten"
                elif dand_eat_count == 0 and pygame.time.get_ticks() - dand_eat_start_time >= ESS_DAUER:
                    dand_eat_status = "eaten"
                    dand_eat_count = 1
                    dand_eat_start_time = pygame.time.get_ticks()
                    
            if charpos_x == strawbpos_x and charpos_y == strawbpos_y:
                txtin_space_content = txt_aktion_eatstrawb
                if strawb_eat_status == "not eaten":
                    blickrichtung = "front"
                    strawb_eat_start_time = pygame.time.get_ticks()
                    if strawb_eat_start_time >= ESS_DAUER:
                        strawb_eat_status = "eaten"
                        strawb_eat_start_time = 0
                        strawb_eat_start_time = pygame.time.get_ticks()
                elif strawb_eat_status == "eaten":
                    curr_txt = txtin_unessbar
            else:
                if strawb_eat_start_time != 0:
                    strawb_eat_start_time = 0
        pass

    # --- Spiellogik hier integrieren ---#

    if bewegt_sich:
        fertig_x = True
        fertig_y = True

        # X-Achse
        if charpos_x < ziel_x:
            charpos_x += slide_speed
            fertig_x = False
            if charpos_x >= ziel_x:
                charpos_x = ziel_x

        elif charpos_x > ziel_x:
            charpos_x -= slide_speed
            fertig_x = False
            if charpos_x <= ziel_x:
                charpos_x = ziel_x

        # Y-Achse
        if charpos_y < ziel_y:
            charpos_y += slide_speed
            fertig_y = False
            if charpos_y >= ziel_y:
                charpos_y = ziel_y

        elif charpos_y > ziel_y:
            charpos_y -= slide_speed
            fertig_y = False
            if charpos_y <= ziel_y:
                charpos_y = ziel_y

        # Bewegung beenden
        if fertig_x and fertig_y:
            bewegt_sich = False
            letzte_taste = None
    
    
    # Spielfeld löschen
    screen.fill(BGcolor)

    #--- Spielfeld/figuren zeichnen ---#
    # Falls von vorne kommt


    if blickrichtung == "front":
        screen.blit(chick_front, (charpos_x, charpos_y))

    if blickrichtung == "toright":
        screen.blit(chick_toright, (charpos_x, charpos_y))

    if blickrichtung == "toleft":
        screen.blit(chick_toleft, (charpos_x, charpos_y))

    if blickrichtung == "back":
        screen.blit(chick_back, (charpos_x, charpos_y))
    
    dandelion_eaten = pygame.transform.scale(
        dandelion_eaten_img,
        (int(dand_breite), int(dand_hoehe))
    )
    dandelion = pygame.transform.scale(
        dandelion_img,
        (int(dand_breite_curr), int(dand_hoehe_curr))
    )
    if dand_visible and dand_eat_status == "not eaten":
        screen.blit(dandelion, (dandpos_x, dandpos_y + dand_hoehe_temp))
    elif dand_visible and dand_eat_status == "eaten":
        screen.blit(dandelion_eaten, (dandpos_x, dandpos_y + dand_hoehe_temp))

    if strawb_visible and strawb_eat_status == "not eaten":
        screen.blit(strawberry, (strawbpos_x, strawbpos_y + FENSTER_PADDING))
    elif strawb_visible and strawb_eat_status == "eaten":
        screen.blit(strawberry_eaten, (strawbpos_x, strawbpos_y + FENSTER_PADDING))
    
    if charpos_x == dandpos_x and charpos_y == dandpos_y: 
        txtin_space_content = txtaktion_eatdand
    elif charpos_x == strawbpos_x and charpos_y == strawbpos_y and strawb_eat_status == "not eaten":
        txtin_space_content = txt_aktion_eatstrawb

    # Text schreiben
    pygame.font.init()
    font = pygame.font.SysFont('calibri', info_height // 3 *2 )

    #Curr_text festlegen
    txtin_space = "Drücke LEERTASTE um die Aktion: "+ txtin_space_content + " auszuführen"
    if charpos_x == dandpos_x and charpos_y == dandpos_y and dand_visible == True or charpos_x == strawbpos_x and charpos_y == strawbpos_y and strawb_visible == True and strawb_eat_status == "not eaten":
        curr_txt = txtin_space
    elif charpos_x == strawbpos_x and charpos_y == strawbpos_y and strawb_eat_status == "eaten" and letzte_taste == pygame.K_SPACE:
            curr_txt = txtin_unessbar
    else:
        curr_txt = txtin_wasd
    

    text_surface = font.render(curr_txt, True, WEISS)
    upperspace_text = info_height + FENSTER_PADDING
    screen.blit(text_surface, (10 + FENSTER_PADDING, FENSTER_PADDING *2))

    # Fenster aktualisieren
    pygame.display.flip()

    # Refresh-Zeiten festlegen
    clock.tick(60)

pygame.quit()
quit()
#zuletzt bearbeitet: 03. Februar 2026
