import pygame
import sys
import time
import random
import statistics
import math
import array
from enum import Enum

class AppState(Enum):
    MENU = 1
    INSTRUCTION = 2
    TRAINING = 3
    TEST = 4
    RESULTS = 5

class PsychoTesterApp:
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.init()
        pygame.mixer.init()
        
        self.base_width = 800
        self.base_height = 600
        self.width = self.base_width
        self.height = self.base_height
        
        # Flaga pygame.RESIZABLE aktywuje natywne przyciski systemowe do zmiany rozmiaru/pełnego ekranu
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        pygame.display.set_caption("Tester Sprawności Psychomotorycznej")
        
        self.clock = pygame.time.Clock()
        self.fps = 500 
        self.state = AppState.MENU
        
        self.font_title = pygame.font.Font(None, 48)
        self.font_text = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)
        self.font_large = pygame.font.Font(None, 72)
        
        self.test_mode = 1          
        self.current_test_name = ""
        self.results = []           
        self.num_trials = 5         
        self.current_trial = 0
        self.sub_state = "IDLE"     
        self.wait_start_time = 0
        self.random_delay = 0
        self.stimulus_start_time = 0
        self.last_reaction_time = 0
        
        self.false_start = False
        self.false_starts_count = 0 
        self.correct_responses = 0  
        
        self.current_arrow_dir = "LEFT" 
        self.last_was_correct = False
        
        self.beep_sound = self.generate_beep(1000, 0.2)
        self.visual_frame_drawn = False 

    def generate_beep(self, frequency, duration):
        sample_rate = 44100
        n_samples = int(round(duration * sample_rate))
        buf = array.array('h') 
        
        for i in range(n_samples):
            t = float(i) / sample_rate
            value = int(32767 * 0.5 * math.sin(2.0 * math.pi * frequency * t))
            buf.append(value) 
            buf.append(value) 
            
        return pygame.mixer.Sound(buffer=buf)

    def start_new_trial(self):
        self.sub_state = "WAITING"
        self.random_delay = random.uniform(2.0, 5.0) 
        self.wait_start_time = time.perf_counter()
        self.false_start = False
        self.current_arrow_dir = random.choice(["LEFT", "RIGHT"])
        self.visual_frame_drawn = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_app()
                
            # Obsługa zmiany rozmiaru okna przez system (np. kliknięcie zielonej kuleczki na Macu)
            if event.type == pygame.VIDEORESIZE:
                self.width = event.w
                self.height = event.h
                self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit_app()
                    
                if self.state == AppState.MENU:
                    if event.key == pygame.K_1:
                        self.test_mode = 1
                        self.current_test_name = "Test prosty optyczny (Spacja)"
                        self.advance_state()
                    elif event.key == pygame.K_2:
                        self.test_mode = 2
                        self.current_test_name = "Test złożony (Strzałki)"
                        self.advance_state()
                    elif event.key == pygame.K_3:
                        self.test_mode = 3
                        self.current_test_name = "Test prosty akustyczny (Spacja)"
                        self.advance_state()
                        
                elif self.state in [AppState.INSTRUCTION, AppState.RESULTS]:
                    if event.key == pygame.K_SPACE:
                        self.advance_state()
                        
                elif self.state in [AppState.TEST, AppState.TRAINING]:
                    
                    if self.sub_state == "WAITING":
                        if event.key in [pygame.K_SPACE, pygame.K_LEFT, pygame.K_RIGHT]:
                            self.false_start = True
                            if self.state == AppState.TEST:
                                self.false_starts_count += 1
                            self.sub_state = "FEEDBACK"
                            self.wait_start_time = time.perf_counter()
                            
                    elif self.sub_state == "STIMULUS":
                        end_time = time.perf_counter() 
                        
                        valid_key_pressed = False
                        is_correct = False
                        
                        if self.test_mode in [1, 3]: 
                            if event.key == pygame.K_SPACE:
                                valid_key_pressed = True
                                is_correct = True
                                
                        elif self.test_mode == 2: 
                            if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                                valid_key_pressed = True
                                if event.key == pygame.K_LEFT and self.current_arrow_dir == "LEFT":
                                    is_correct = True
                                elif event.key == pygame.K_RIGHT and self.current_arrow_dir == "RIGHT":
                                    is_correct = True

                        if valid_key_pressed:
                            self.last_reaction_time = (end_time - self.stimulus_start_time) * 1000 
                            self.last_was_correct = is_correct
                            
                            if self.state == AppState.TEST:
                                self.results.append(self.last_reaction_time)
                                if is_correct:
                                    self.correct_responses += 1
                                    
                            self.sub_state = "FEEDBACK"
                            self.wait_start_time = time.perf_counter()

    def advance_state(self):
        if self.state == AppState.MENU:
            self.state = AppState.INSTRUCTION
        elif self.state == AppState.INSTRUCTION:
            self.state = AppState.TRAINING
            self.current_trial = 0
            self.start_new_trial()
        elif self.state == AppState.TRAINING:
            self.state = AppState.TEST
            self.current_trial = 0
            self.results = []
            self.false_starts_count = 0
            self.correct_responses = 0
            self.start_new_trial()
        elif self.state == AppState.TEST:
            self.state = AppState.RESULTS
        elif self.state == AppState.RESULTS:
            self.state = AppState.MENU

    def update(self):
        if self.state in [AppState.TEST, AppState.TRAINING]:
            current_time = time.perf_counter()
            if self.sub_state == "WAITING":
                if current_time - self.wait_start_time >= self.random_delay:
                    self.sub_state = "STIMULUS"
                    self.visual_frame_drawn = False 
                    
                    if self.test_mode == 3:
                        self.stimulus_start_time = time.perf_counter()
                        self.beep_sound.stop() 
                        self.beep_sound.play()
                        
            elif self.sub_state == "FEEDBACK":
                if current_time - self.wait_start_time >= 1.5:
                    self.current_trial += 1
                    limit = 3 if self.state == AppState.TRAINING else self.num_trials
                    if self.current_trial >= limit:
                        self.advance_state()
                    else:
                        self.start_new_trial()

    def draw_text_centered(self, text, font, color, y_offset=0, x_offset=0):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(self.width/2 + x_offset, self.height/2 + y_offset))
        self.screen.blit(text_surface, text_rect)

    def draw_text_left(self, text, font, color, x, y):
        text_surface = font.render(text, True, color)
        offset_x = (self.width - self.base_width) // 2 
        offset_y = (self.height - self.base_height) // 2 
        self.screen.blit(text_surface, (x + offset_x, y + offset_y))

    def draw_arrow(self, direction, color):
        cx, cy = self.width // 2, self.height // 2
        if direction == "LEFT":
            points = [(cx-60, cy), (cx+20, cy-60), (cx+20, cy-30), (cx+80, cy-30), (cx+80, cy+30), (cx+20, cy+30), (cx+20, cy+60)]
        else:
            points = [(cx+60, cy), (cx-20, cy-60), (cx-20, cy-30), (cx-80, cy-30), (cx-80, cy+30), (cx-20, cy+30), (cx-20, cy+60)]
        pygame.draw.polygon(self.screen, color, points)

    def quit_app(self):
        pygame.quit()
        sys.exit()

    def draw_graph(self):
        if len(self.results) < 2:
            self.draw_text_centered("Zbyt mało danych do wykresu.", self.font_small, (150, 150, 150), 160)
            return

        offset_x = (self.width - self.base_width) // 2 
        offset_y = (self.height - self.base_height) // 2 

        chart_x, chart_y = 150 + offset_x, 370 + offset_y
        chart_w, chart_h = 500, 160 
        
        WHITE = (255, 255, 255)
        GREEN = (50, 255, 50)
        YELLOW = (255, 200, 0)

        pygame.draw.line(self.screen, WHITE, (chart_x, chart_y), (chart_x, chart_y + chart_h), 2)
        pygame.draw.line(self.screen, WHITE, (chart_x, chart_y + chart_h), (chart_x + chart_w, chart_y + chart_h), 2)
        
        text_surface1 = self.font_small.render("Czas (ms)", True, WHITE)
        self.screen.blit(text_surface1, (chart_x - 80, chart_y - 20))
        
        text_surface2 = self.font_small.render("Nr próby", True, WHITE)
        self.screen.blit(text_surface2, (chart_x + chart_w + 10, chart_y + chart_h - 10))

        max_val = max(max(self.results), 500) 
        x_step = chart_w / (len(self.results) - 1)
        
        points = []
        for i, val in enumerate(self.results):
            x = chart_x + i * x_step
            y = (chart_y + chart_h) - (val / max_val) * chart_h 
            points.append((x, y))

        pygame.draw.lines(self.screen, GREEN, False, points, 3)
        for i, (x, y) in enumerate(points):
            pygame.draw.circle(self.screen, YELLOW, (int(x), int(y)), 6)
            val_text = self.font_small.render(f"{int(self.results[i])}", True, WHITE)
            self.screen.blit(val_text, (x - 15, y - 25))
            trial_text = self.font_small.render(f"{i+1}", True, WHITE)
            self.screen.blit(trial_text, (x - 5, chart_y + chart_h + 10))

    def draw(self):
        self.screen.fill((30, 30, 30))
        WHITE = (255, 255, 255)
        YELLOW = (255, 200, 0)
        GREEN = (50, 255, 50)
        RED = (255, 50, 50)
        LIGHT_BLUE = (100, 200, 255)
        
        if self.state == AppState.MENU:
            self.draw_text_centered("Witaj w Testerze Psychomotorycznym", self.font_title, WHITE, -100)
            self.draw_text_centered("Wybierz rodzaj testu:", self.font_text, LIGHT_BLUE, -20)
            self.draw_text_centered("[ 1 ] Test Prosty Optyczny (Zielony kwadrat)", self.font_text, WHITE, 30)
            self.draw_text_centered("[ 2 ] Test Złożony Optyczny (Strzałki Lewo/Prawo)", self.font_text, WHITE, 80)
            self.draw_text_centered("[ 3 ] Test Prosty Akustyczny (Sygnał dźwiękowy)", self.font_text, WHITE, 130)
            
        elif self.state == AppState.INSTRUCTION:
            self.draw_text_centered(f"Instrukcja: {self.current_test_name}", self.font_title, WHITE, -80)
            if self.test_mode == 1:
                self.draw_text_centered("Gdy zobaczysz ZIELONY KWADRAT, wciśnij SPACJĘ.", self.font_text, WHITE, 0)
            elif self.test_mode == 2:
                self.draw_text_centered("Gdy zobaczysz STRZAŁKĘ, wciśnij ODPOWIEDNI KIERUNEK", self.font_text, WHITE, 0)
                self.draw_text_centered("na klawiaturze (Lewo lub Prawo).", self.font_text, WHITE, 40)
            elif self.test_mode == 3:
                self.draw_text_centered("Patrz w środek ekranu. Gdy usłyszysz DŹWIĘK,", self.font_text, WHITE, 0)
                self.draw_text_centered("jak najszybciej wciśnij SPACJĘ.", self.font_text, WHITE, 40)
                
            self.draw_text_centered("[Naciśnij SPACJĘ aby przejść do szkolenia]", self.font_text, YELLOW, 120)
            
        elif self.state in [AppState.TEST, AppState.TRAINING]:
            faza = "SZKOLENIE" if self.state == AppState.TRAINING else "TEST"
            limit = 3 if self.state == AppState.TRAINING else self.num_trials
            self.draw_text_centered(f"{faza} - Próba {self.current_trial + 1} / {limit}", self.font_text, WHITE, -250)

            if self.sub_state == "WAITING":
                self.draw_text_centered("+", self.font_title, WHITE, 0)
                
            elif self.sub_state == "STIMULUS":
                if self.test_mode == 1:
                    pygame.draw.rect(self.screen, GREEN, (self.width//2 - 100, self.height//2 - 100, 200, 200))
                elif self.test_mode == 2:
                    self.draw_arrow(self.current_arrow_dir, GREEN)
                elif self.test_mode == 3:
                    self.draw_text_centered("+", self.font_title, WHITE, 0) 
                
            elif self.sub_state == "FEEDBACK":
                if self.false_start:
                    self.draw_text_centered("FALSTART! Wciśnięto za wcześnie.", self.font_title, RED, -40)
                else:
                    self.draw_text_centered(f"Czas: {self.last_reaction_time:.0f} ms", self.font_large, YELLOW, -40)
                    if self.test_mode == 2:
                        if self.last_was_correct:
                            self.draw_text_centered("DOBRZE", self.font_title, GREEN, 40)
                        else:
                            self.draw_text_centered("BŁĄD KIERUNKU!", self.font_title, RED, 40)
                            
                    if self.state == AppState.TRAINING:
                        self.draw_text_centered("(Wynik nie jest zapisywany)", self.font_text, WHITE, 100)

        elif self.state == AppState.RESULTS:
            self.draw_text_centered(f"RAPORT: {self.current_test_name}", self.font_title, WHITE, -250)
            
            if len(self.results) > 0:
                srednia = statistics.mean(self.results)
                odchylenie = statistics.stdev(self.results) if len(self.results) > 1 else 0
                
                prog_czasu = 350 if self.test_mode in [1, 3] else 500
                ocena_kolor = GREEN if srednia < prog_czasu else RED
                
                self.draw_text_left(f"Średni czas reakcji: {srednia:.0f} ms", self.font_text, ocena_kolor, 150, 100)
                self.draw_text_left(f"Najszybsza reakcja: {min(self.results):.0f} ms", self.font_small, WHITE, 150, 140)
                self.draw_text_left(f"Najwolniejsza reakcja: {max(self.results):.0f} ms", self.font_small, WHITE, 150, 170)
                self.draw_text_left(f"Stabilność (Odchylenie stand.): {odchylenie:.0f} ms", self.font_small, LIGHT_BLUE, 150, 200)
                self.draw_text_left(f"Liczba falstartów: {self.false_starts_count}", self.font_small, RED if self.false_starts_count > 0 else GREEN, 150, 230)

                if self.test_mode == 2:
                    skutecznosc = (self.correct_responses / len(self.results)) * 100
                    kolor_skut = GREEN if skutecznosc > 80 else RED
                    self.draw_text_left(f"Poprawność decyzji: {skutecznosc:.0f}%", self.font_text, kolor_skut, 150, 260)

                self.draw_graph()
            else:
                self.draw_text_centered("Brak zapisanych wyników (same falstarty).", self.font_text, RED, -100)
                
            self.draw_text_centered("[Naciśnij SPACJĘ aby wrócić do Menu]", self.font_small, YELLOW, 280)

        pygame.display.flip()

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            
            if self.state in [AppState.TEST, AppState.TRAINING]:
                if self.sub_state == "STIMULUS" and self.test_mode in [1, 2]:
                    if not self.visual_frame_drawn:
                        self.stimulus_start_time = time.perf_counter()
                        self.visual_frame_drawn = True

            self.clock.tick(self.fps)

if __name__ == "__main__":
    app = PsychoTesterApp()
    app.run()