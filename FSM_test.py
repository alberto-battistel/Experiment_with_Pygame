#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 24 23:51:03 2022

@author: alberto
"""

#%%
# run main.py first

import FSM

FSM_test = FSM.Finite_State_Machine('FSM_test')
FSM_event_pressed_right = FSM.Event('pressed_right', [pygame.K_RIGHT])
FSM_event_pressed_left = FSM.Event('pressed_left', [pygame.K_LEFT])

FSM_test.add_to_events([FSM_event_pressed_right, FSM_event_pressed_left])

FSM_test.print_event_list()

dictionary = {'state1': [('pressed_right', 'state2')],
              'state2': [('pressed_left', 'state1')],}
FSM_table = FSM.Event_State_Table(dictionary)
FSM_table.print_table()

FSM_state1 = FSM.State('state1', True)
FSM_state2 = FSM.State('state2', False)

FSM_test.event_state_table = FSM_table
FSM_test.add_to_states([FSM_state1, FSM_state2])
FSM_test.pass_starting_state()
FSM_test.print_state_list()


#%%

for ii,event in enumerate(event_list):
    if event.type == pygame.KEYDOWN:
        print('at position {:}'.format(ii))
        # event.key
        # FSM_event.check_events(event)
        FSM_test.check_events(event)
        FSM_test.check_table()
        print('')
        

