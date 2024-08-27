import pygame
from pygame.locals import *
import sys
import time
import random

class Game:
    def __init__(self):
        pygame.init()

        self.w = 750
        self.h = 500
        self.reset = True
        self.active = False
        self.input_box = pygame.Rect(50, 250, 650, 50)
        self.color_inactive = pygame.Color('lightskyblue3')
        self.color_active = pygame.Color('dodgerblue2')
        self.color = self.color_inactive
        self.font = pygame.font.Font(None, 32)
        self.word = ''
        self.input_text = ''
        self.time_start = 0
        self.total_time = 0
        self.accuracy = '0%'
        self.results = 'Time:0 Accuracy:0 % Wpm:0 '
        self.wpm = 0
        self.end = False
        self.HEAD_C = (255,213,102)
        self.TEXT_C = (240,240,240)
        self.RESULT_C = (255,70,70)

        # Initialize cursor attributes
        self.cursor_visible = True
        self.cursor_timer = 0

        self.bg = pygame.image.load('./img/solid-color-image.png')

        self.screen = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Type Speed Test')

    def draw_text(self, screen, msg, y ,fsize, color):
        font = pygame.font.Font(None, fsize)
        text = font.render(msg, True, color)
        text_rect = text.get_rect(center=(self.w / 2, y))
        screen.blit(text, text_rect)
        pygame.display.update()

    def get_sentence(self):
        """
        Gets a random sentence from the text file.
        """
        with open('sentences.txt') as f:
            sentences = f.readlines()
        sentence = random.choice(sentences).strip()
        return sentence

    def show_results(self, screen):
        if not self.end:
            # Calculate time
            self.total_time = time.time() - self.time_start

            # Calculate accuracy by correct characters
            count = 0
            w = self.word.split()
            input_split = self.input_text.split()
            for i in range(len(w)):
                for j, c in enumerate(w[i]):
                    try:
                        if input_split[i][j] == c:
                            count += 1
                    except:
                        pass

            self.accuracy = count / len(self.word.replace(" ", "")) * 100

            # Calculate words per minute
            self.wpm = len(self.input_text) * 60 / (5 * self.total_time)
            self.end = True

            self.results = 'Time: ' + str(round(self.total_time)) + " secs   Accuracy: " + str(round(self.accuracy)) + "%" + '   Wpm: ' + str(round(self.wpm))

            # Draw icon image
            self.time_img = pygame.image.load('./img/icon.png')
            self.time_img = pygame.transform.scale(self.time_img, (150, 150))
            screen.blit(self.time_img, (self.w/2 - 75, self.h - 140))
            self.draw_text(screen, "Reset", self.h - 70, 26, (100, 100, 100))
            
            print(self.results)
            pygame.display.update()

    def reset_game(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.bg, (0, 0))
        msg = 'Typing Speed Test'
        self.draw_text(self.screen, msg, 80, 80, self.HEAD_C)

        pygame.draw.rect(self.screen, (255, 192, 25), self.input_box, 2)
        
        self.reset = False
        self.end = False

        self.input_text = ''
        self.word = ''
        self.time_start = 0
        self.total_time = 0
        self.wpm = 0

        self.word = self.get_sentence()
        if not self.word: 
            self.reset_game()

        self.draw_text(self.screen, self.word, 200, 28, self.TEXT_C)

        pygame.display.update()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.input_box.collidepoint(event.pos):
                self.active = not self.active
                self.color = self.color_active if self.active else self.color_inactive

        if event.type == pygame.KEYDOWN:
            if self.active and not self.end:
                if event.key == pygame.K_RETURN:
                    self.show_results(self.screen)
                elif event.key == pygame.K_BACKSPACE:
                    self.input_text = self.input_text[:-1]
                else:
                    self.input_text += event.unicode

    def run(self):
        self.reset_game()
        self.running = True

        while self.running:
            clock = pygame.time.Clock()

            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()
                self.handle_event(event)

            self.screen.fill((0, 0, 0))
            self.screen.blit(self.bg, (0, 0))

            txt_surface = self.font.render(self.input_text, True, self.color)
            width = max(650, txt_surface.get_width() + 10)
            self.input_box.w = width
            self.screen.blit(txt_surface, (self.input_box.x + 5, self.input_box.y + 15))
            pygame.draw.rect(self.screen, self.color, self.input_box, 2)

            # Blinking cursor
            if self.active:
                self.cursor_timer += clock.get_time()
                if self.cursor_timer >= 500:
                    self.cursor_visible = not self.cursor_visible
                    self.cursor_timer = 0
                if self.cursor_visible:
                    cursor_rect = pygame.Rect(self.input_box.x + 5 + txt_surface.get_width(), self.input_box.y + 15, 2, self.font.get_height())
                    pygame.draw.rect(self.screen, self.color, cursor_rect)

            pygame.display.flip()
            clock.tick(60)

Game().run()
