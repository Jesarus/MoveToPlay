import cv2
import pygame
from config import LARGURA_TELA, ALTURA_TELA, PRETO, BRANCO
import mediapipe as mp

# Mediapipe setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils
cap = cv2.VideoCapture(1)  # Use 0 for the default webcam

def atualizar_webcam(tela):
    """Capture and display the webcam feed on the left 1/3 of the screen."""
    success, frame = cap.read()
    if not success:
        return None

    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(img_rgb)

    h, w, _ = frame.shape
    pos_y = None  # Default to None if no hand is detected

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            cx = int(hand_landmarks.landmark[9].x * w)
            cy = int(hand_landmarks.landmark[9].y * h)

            cv2.circle(frame, (cx, cy), 10, (0, 255, 0), cv2.FILLED)
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            pos_y = int(hand_landmarks.landmark[9].y * ALTURA_TELA)

    # Resize the frame to fit 1/3 of the screen width
    frame = cv2.resize(frame, (LARGURA_TELA // 3, ALTURA_TELA))
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert back to RGB for pygame

    # Create a pygame surface from the frame and blit it to the left side of the screen
    frame_surface = pygame.surfarray.make_surface(frame)
    tela.blit(pygame.transform.rotate(frame_surface, -90), (0, 0))

    return pos_y

def wait_for_hand_detection(tela, clock):
    """Wait until the system detects a hand."""
    fonte_espera = pygame.font.SysFont(None, 48)
    detecting = True

    while detecting:
        # Fill the screen with black
        tela.fill(PRETO)

        # Display the webcam feed on the left 1/3 of the screen
        pos_y = atualizar_webcam(tela)

        # Render the detection message on the right 2/3 of the screen
        mensagem = fonte_espera.render("Detectando mão... Por favor, mostre sua mão.", True, BRANCO)
        mensagem_x = LARGURA_TELA // 3 + (2 * LARGURA_TELA // 3) // 2 - mensagem.get_width() // 2
        mensagem_y = ALTURA_TELA // 2
        tela.blit(mensagem, (mensagem_x, mensagem_y))

        pygame.display.flip()

        # Check if a hand is detected
        if pos_y is not None:  # Hand detected
            # Display confirmation message
            mensagem_detectada = fonte_espera.render("Mão detectada! Iniciando o jogo...", True, BRANCO)
            tela.fill(PRETO)
            tela.blit(mensagem_detectada, (mensagem_x, mensagem_y))
            pygame.display.flip()
            pygame.time.wait(1000)  # Wait for 1 second before starting the game
            return True

        # Handle quit event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

        clock.tick(30)

def release_resources():
    """Release webcam and Mediapipe resources."""
    cap.release()
    cv2.destroyAllWindows()