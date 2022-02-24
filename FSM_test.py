#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 24 23:51:03 2022

@author: alberto
"""

# run main.py first

import FSM

FSM_test = FSM.Finite_State_Machine('FSM_test')
FSM_event = FSM.Event('input', [pygame.K_LEFT, pygame.K_RIGHT])
FSM_event.print_list()

for ii,event in enumerate(event_list):
    if event.type == pygame.KEYDOWN:
        print('at position {:}'.format(ii))
        # event.key
        FSM_event.check_events(event)
        print('')
