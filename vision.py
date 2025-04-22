import cv2
import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, WHITE
import mediapipe as mp

# Mediapipe setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils
cap = cv2.VideoCapture(1)  # Use 0 for the default webcam

def update_webcam(screen):
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

            pos_y = int(hand_landmarks.landmark[9].y * SCREEN_HEIGHT)

    # Resize the frame to fit 1/3 of the screen width
    frame = cv2.resize(frame, (SCREEN_WIDTH // 3, SCREEN_HEIGHT))
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert back to RGB for pygame

    # Create a pygame surface from the frame and blit it to the left side of the screen
    frame_surface = pygame.surfarray.make_surface(frame)
    screen.blit(pygame.transform.rotate(frame_surface, -90), (0, 0))

    return pos_y

def wait_for_hand_detection(screen, clock):
    """Wait until the system detects a hand."""
    waiting_font = pygame.font.SysFont(None, 48)
    detecting = True

    while detecting:
        # Fill the screen with black
        screen.fill(BLACK)

        # Display the webcam feed on the left 1/3 of the screen
        pos_y = update_webcam(screen)

        # Render the detection message on the right 2/3 of the screen
        message = waiting_font.render("Detecting hand... Please show your hand.", True, WHITE)
        message_x = SCREEN_WIDTH // 3 + (2 * SCREEN_WIDTH // 3) // 2 - message.get_width() // 2
        message_y = SCREEN_HEIGHT // 2
        screen.blit(message, (message_x, message_y))

        pygame.display.flip()

        # Check if a hand is detected
        if pos_y is not None:  # Hand detected
            # Display confirmation message
            detected_message = waiting_font.render("Hand detected! Starting the game...", True, WHITE)
            screen.fill(BLACK)
            screen.blit(detected_message, (message_x, message_y))
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