"""
from 
https://www.reddit.com/r/pygame/comments/w4yf4q/comment/ih5jlv2/?utm_source=share&utm_medium=web2x&context=3
"""

import pygame

pygame.init()

class Notifier:
    def __init__(self):
        self._subscribers = {}  # Should use a defaultdict

    def dispatch(self, events):
        for event in events:
            subscribed = self._get_subscribers(event.type)
            for subscriber in subscribed:
                """ Maybe add some try-catch if subscriber no longer exists/None, remove from list """
                if callable(subscriber):
                    subscriber()
                elif isinstance(subscriber, object):
                    subscriber.handle_event(event)

    def _get_subscribers(self, event_type):
        subscribers = self._subscribers.get(event_type)
        return subscribers if subscribers else []

    def subscribe(self, event, subscriber):
        """ Can be turned into a decorator but gets really complicated """
        subscribers = self._subscribers.get(event)
        if subscribers:
            subscribers.append(subscriber)
        else:
            self._subscribers.update({event: [subscriber]})

    def unsubscribe(self, event, subscriber):
        subscribers = self._get_subscribers(event)
        if subscribers:
            subscribers.remove(subscriber)

class Sprite:
    def handle_event(self, event_type):
        print(event_type)
        #if event_type == pygame.KEYDOWN:
        #    ...

def quit_game():
    pygame.quit()
    quit()

def unsubscribe():
    notifier.unsubscribe(pygame.MOUSEMOTION, sprite2)

WIDTH, HEIGHT = 500, 500
UNSUBSCRIBE = pygame.USEREVENT + 0
# After 3 seconds sprite2 will no longer get notified for MOUSEMOTION
pygame.time.set_timer(UNSUBSCRIBE, 3_000)

screen = pygame.display.set_mode((WIDTH, HEIGHT))

notifier = Notifier()
sprite1 = Sprite()
sprite2 = Sprite()

notifier.subscribe(pygame.KEYDOWN, sprite1)
notifier.subscribe(pygame.MOUSEMOTION, sprite2)
notifier.subscribe(pygame.QUIT, quit_game)
notifier.subscribe(UNSUBSCRIBE, unsubscribe)

while True:
    notifier.dispatch(pygame.event.get())
