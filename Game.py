import pygame
import json
import random
from random import choice
from Conexiones_MySQL import conectar_db
from tkinter import messagebox
import time

score = 0
nivel = 0
is_jumping = False
jump_count = 10
correct_answers_session = 0
logro_mostrar_tiempo = 0
logro_mostrado = {5: False, 10: False, 15: False, 30: False}

escenarios = [
    "img/game_fondo_1.jpg",
    "img/game_fondo_2.jpg",
    "img/game_fondo_3.jpg",
    "img/game_fondo_4.jpg",
    "img/game_fondo_5.jpg",
    "img/game_fondo_6.jpg",
]

def cargar_fondo(nivel, screen_width, screen_height):
    escenario_index = (nivel // 5) % len(escenarios)
    fondo = pygame.image.load(escenarios[escenario_index])
    fondo = pygame.transform.scale(fondo, (screen_width, screen_height))
    return fondo

def guardar_progreso(id_estudiantes, nivel, puntos):
    conexion = conectar_db()
    if conexion:
        cursor = conexion.cursor()
        query = """
            UPDATE progreso
            SET nivel = %s, puntos = %s
            WHERE id_estudiantes = %s
        """
        cursor.execute(query, (nivel, puntos, id_estudiantes))
        conexion.commit()
        cursor.close()
        conexion.close()

def cargar_progreso(id_estudiantes):
    conexion = conectar_db()
    if conexion:
        cursor = conexion.cursor()
        query = """
        SELECT nivel, puntos 
        FROM progreso WHERE id_estudiantes = %s
        """
        cursor.execute(query, (id_estudiantes,))
        resultado = cursor.fetchone()
        cursor.close()
        conexion.close()
        if resultado:
            return resultado
    return (0, 0)

def obtener_preguntas(cantidad=30):
    conexion = conectar_db()
    if  conexion:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM preguntas ORDER BY RAND() LIMIT %s", (cantidad,))
        preguntas = cursor.fetchall()
        conexion.close()
        if preguntas:
            return preguntas

def mostrar_logro(screen, correct_answers_session):
    logro_image = None
    logro_text = ""
    mostrar_duracion = 2

    if correct_answers_session in logro_mostrado and not logro_mostrado[correct_answers_session]:
        if correct_answers_session == 5:
            logro_image = pygame.image.load("img/5pre.png")
            logro_text = "5 Preguntas Correctas"
        elif correct_answers_session == 10:
            logro_image = pygame.image.load("img/10pre.png")
            logro_text = "10 Preguntas Correctas"
        elif correct_answers_session == 15:
            logro_image = pygame.image.load("img/15pre.png")
            logro_text = "15 Preguntas Correctas"
        elif correct_answers_session == 30:
            logro_image = pygame.image.load("img/30pre.png")
            logro_text = "30 Preguntas Correctas"

    if logro_image:
        logro_image = pygame.transform.scale(logro_image, (200, 200))
        image_x = (screen.get_width() - logro_image.get_width()) // 2
        image_y = (screen.get_height() - logro_image.get_height()) // 2 - 50
        screen.blit(logro_image, (image_x, image_y))

        font = pygame.font.Font("font/Eight-Bit Madness.ttf", 50)
        logro_alcanzado_surface = font.render("Logro Alcanzado", True, (0, 0, 0))
        logro_alcanzado_x = (screen.get_width() - logro_alcanzado_surface.get_width()) // 2
        logro_alcanzado_y = image_y + logro_image.get_height() + 10
        screen.blit(logro_alcanzado_surface, (logro_alcanzado_x, logro_alcanzado_y))

        logro_text_surface = font.render(logro_text, True, (0, 0, 0))
        text_x = (screen.get_width() - logro_text_surface.get_width()) // 2
        text_y = logro_alcanzado_y + logro_alcanzado_surface.get_height() + 10
        screen.blit(logro_text_surface, (text_x, text_y))

        logro_mostrado[correct_answers_session] = True
        pygame.display.flip()

        start_time = pygame.time.get_ticks()
        while pygame.time.get_ticks() - start_time < mostrar_duracion * 1000:
            pygame.event.pump()
            pygame.time.wait(30)
        
        mostrar_gif_logro(screen)

def mostrar_gif_logro(screen):
    global score
    gif_images = [pygame.image.load(f"img/star_{i}.png") for i in range(1, 7)]
    gif_rect = gif_images[0].get_rect()
    gif_rect.y = screen.get_height() // 2 - gif_rect.height // 2
    gif_rect.x = screen.get_width()

    gif_speed = 10
    gif_active = True
    gif_frame = 0
    total_frames = len(gif_images)

    surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)

    fondo = cargar_fondo(nivel, screen.get_width(), screen.get_height())

    while gif_active:
        surface.fill((0, 0, 0, 0))
        surface.blit(fondo, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gif_active = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if gif_rect.collidepoint(event.pos):
                    score += 500
                    gif_active = False

        gif_rect.x -= gif_speed
        if gif_rect.x + gif_rect.width < 0:
            gif_active = False

        surface.blit(gif_images[gif_frame], gif_rect)

        gif_frame = (gif_frame + 1) % total_frames

        screen.blit(surface, (0, 0))
        pygame.display.flip()
        pygame.time.wait(30)

    return score

def pantalla_inicio(screen, screen_width, screen_height):
    start_screen_image = pygame.image.load("img/game_start.jpg")
    start_screen_image = pygame.transform.scale(start_screen_image, (screen_width, screen_height))
    screen.blit(start_screen_image, (0, 0))

    font_start = pygame.font.Font("font/Eight-Bit Madness.ttf", 100)
    font_text = pygame.font.Font("font/Eight-Bit Madness.ttf", 75)

    text = font_start.render("START", True, (0, 0, 0))
    screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2.7 - text.get_height() // 2))

    start_text = font_text.render("Clases 5° a 7°", True, (0, 0, 0))
    screen.blit(start_text, (screen_width // 2 - start_text.get_width() // 2, screen_height - 230))

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False

def dibuja_pj(screen, character_images, x, y, character_index):
    screen.blit(character_images[character_index], (x, y))
    character_index = (character_index + 1) % len(character_images)
    return character_index

def jump_pj(character_y, is_jumping, jump_count):
    if is_jumping:
        if jump_count >= -10:
            neg = 1 if jump_count >= 0 else -1
            character_y -= (jump_count ** 2) * 0.3 * neg
            jump_count -= 0.5
        else:
            jump_count = 10
            is_jumping = False
    return character_y, is_jumping, jump_count

def mostrar_pregunta(screen, correct_sound, incorrect_sound, id_estudiante, screen_width, screen_height, cantidad_preguntas=30):
    global score, nivel, correct_answers_session

    preguntas_db = obtener_preguntas(cantidad=cantidad_preguntas)
    if not preguntas_db:
        print("No se pudieron cargar las preguntas desde la base de datos.")
        return False

    pregunta_actual = random.choice(preguntas_db)

    question_text = pregunta_actual["preguntas"]
    opciones = [
        pregunta_actual["opcion_1"],
        pregunta_actual["opcion_2"],
        pregunta_actual["opcion_3"],
        pregunta_actual["opcion_4"]
    ]
    respuesta_correcta = pregunta_actual["respuesta_correcta"]
    attempts = 2
    answer = None

    imagen_fondo = cargar_fondo(nivel, screen_width, screen_height)
    overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    overlay.fill((255, 255, 255, 80))

    font = pygame.font.Font(None, 36)

    def wrap_text(text, font, max_width):
        words = text.split(" ")
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + (word if current_line == "" else " " + word)
            test_width = font.size(test_line)[0]
            
            if test_width <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
                
        lines.append(current_line)
        return lines

    max_width = screen.get_width() - 130
    wrapped_question = wrap_text(question_text, font, max_width)

    question_y_pos = 130
    question_surfaces = [font.render(line, True, (0, 0, 0)) for line in wrapped_question]

    options_start_y = question_y_pos + len(question_surfaces) * 40 + 20

    option_surfaces = [font.render(f"{i+1}. {opt}", True, (0, 0, 0)) for i, opt in enumerate(opciones)]

    while attempts > 0:
        screen.blit(imagen_fondo, (0, 0))
        screen.blit(overlay, (0, 0))

        y_offset = question_y_pos
        for line_surface in question_surfaces:
            screen.blit(line_surface, (100, y_offset))
            y_offset += 40

        y_offset = options_start_y
        for option_surface in option_surfaces:
            screen.blit(option_surface, (100, y_offset))
            y_offset += 40

        pygame.display.flip()

        answer = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    answer = opciones[0]
                elif event.key == pygame.K_2:
                    answer = opciones[1]
                elif event.key == pygame.K_3:
                    answer = opciones[2]
                elif event.key == pygame.K_4 and len(opciones) > 3:
                    answer = opciones[3]

        if answer:
            if answer == respuesta_correcta:
                score += 100
                nivel += 1
                correct_answers_session += 1
                guardar_progreso(id_estudiante, nivel, score)
                correct_sound.play()
                return True
            else:
                attempts -= 1
                incorrect_sound.play()
                answer = None

    return False


def mostrar_puntuacion(screen, score, nivel):
    font_score = pygame.font.Font("font/Eight-Bit Madness.ttf", 50)
    score_text = font_score.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    font_nivel = pygame.font.Font("font/Eight-Bit Madness.ttf", 50)
    level_text = font_nivel.render(f"Nivel: {nivel}", True, (0, 0, 0))
    screen.blit(level_text, (10, 60))

def game_over(screen, screen_width, screen_height, id_estudiante):
    guardar_progreso(id_estudiante, 0, 0)
    font_end = pygame.font.Font("font/Eight-Bit Madness.ttf", 80)
    text = font_end.render("Game Over", True, (255, 50, 50))
    screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2 - text.get_height() // 2))
    pygame.display.flip()
    pygame.time.delay(2000)

def cargar_preguntas(filepath):
    questions = []
    try:
        with open(filepath) as file:
            questions = json.load(file)
    except FileNotFoundError:
        print("Error: El archivo de preguntas no se encuentra.")
    return questions

class Enemigo:
    def __init__(self, image, screen_width, screen_height):
        self.image = image
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.x = screen_width + self.width
        self.y = random.randint(screen_height - 100, screen_height - 30)
        self.speed = random.randint(5, 10)

    def mover(self):
        self.x -= self.speed

    def dibujar(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def fuera_de_pantalla(self):
        return self.x < -self.width

    def colisiona(self, character_x, character_y, character_width, character_height):
        margen = 40
        return (
            self.x + margen < character_x + character_width and
            self.x + self.width - margen > character_x and
            self.y + margen < character_y + character_height and
            self.y + self.height - margen > character_y
        )

def manejar_enemigos(screen, enemigos, character_x, character_y, character_width, character_height, screen_width, screen_height, id_estudiante):
    global score
    for enemigo in enemigos[:]:
        enemigo.mover()
        enemigo.dibujar(screen)
        if enemigo.colisiona(character_x, character_y, character_width, character_height):
            score -= 300
            enemigos.remove(enemigo)
            if score <= 0:
                game_over(screen, screen_width, screen_height, id_estudiante)
                return False
        if enemigo.fuera_de_pantalla():
            enemigos.remove(enemigo)
    return True

enemigo_images = [pygame.image.load(f"img/enemigo{i}.png") for i in range(1, 9)]
enemigos = []
enemigo_timer = 0

def iniciar_juego(id_estudiante):
    global score, is_jumping, jump_count, nivel, correct_answers_session
    pygame.init()
    screen_width, screen_height = 1100, 500
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.SRCALPHA)
    pygame.display.set_caption("GAME")
    clock = pygame.time.Clock()

    nivel, score = cargar_progreso(id_estudiante)
    juego_activo = True
    correct_answers_session = 0
    enemigo_timer = 0

    pantalla_inicio(screen, screen_width, screen_height)

    fondo = cargar_fondo(nivel, screen_width, screen_height)

    character_images = [pygame.image.load(f"img/run_{i}.png") for i in range(1, 7)]
    character_index = 0
    character_x, character_y = 50, screen_height - 100
    is_jumping, jump_count = False, 10
    character_velocity = 5

    pygame.mixer.init()
    respuesta_correcta_sound = pygame.mixer.Sound("music/correct.mp3")
    respuesta_incorrecta_sound = pygame.mixer.Sound("music/wronganswer.mp3")

    running = True
    distance = 0
    while running:
        screen.blit(fondo, (0, 0))

        fondo = cargar_fondo(nivel, screen_width, screen_height)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    guardar_progreso(id_estudiante, nivel, score)
                    messagebox.showinfo("Juego Pausado", "Progreso guardado.")
                    running = False
                    break
                elif event.key == pygame.K_SPACE and not is_jumping:
                    is_jumping = True

        enemigo_timer += 1
        if enemigo_timer >= 60:
            enemigo_image = random.choice(enemigo_images)
            enemigos.append(Enemigo(enemigo_image, screen_width, screen_height))
            enemigo_timer = 0

        if not manejar_enemigos(screen, enemigos, character_x, character_y, character_images[0].get_width(), character_images[0].get_height(), screen_width, screen_height, id_estudiante):
            running = False

        if correct_answers_session in [5, 10, 15, 30] and not logro_mostrado[correct_answers_session]:
            mostrar_logro(screen, correct_answers_session)

        character_index = dibuja_pj(screen, character_images, character_x, character_y, character_index)
        character_y, is_jumping, jump_count = jump_pj(character_y, is_jumping, jump_count)

        distance += 1
        if distance % 200 == 0:
            if not mostrar_pregunta(screen, respuesta_correcta_sound, respuesta_incorrecta_sound, id_estudiante, screen_width, screen_height):
                game_over(screen, screen_width, screen_height, id_estudiante)
                running = False
            distance += 200

        mostrar_puntuacion(screen, score, nivel)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()