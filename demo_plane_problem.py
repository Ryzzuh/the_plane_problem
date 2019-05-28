#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  2 23:25:39 2019

@author: rhysall
r.allen@students.mq.edu.au
"""
#relase notes
#v.09 added the following features
#addition of core classes, plane and passenger
#import inspect
from os import system
from time import sleep
import random
import math
from IPython.display import clear_output




class booking_system:
    
    def __init__(self):
        pass
    
    def all_seats(self, plane):
        seats=[[x,y] for x in range(plane.h)\
              for y in range(plane.w) if y != plane.corridor]
        #print(seats)
        return seats
        
    def out_to_in_seats(self, plane):
        width = plane.w
        height = plane.h
        seats = []
        aisle = math.floor(width/2)
        for y in range(height)[::-1]:
            for x in range(2):
                seats.append([y,x])
            temp = []
            for x in range(aisle+1,width):
                temp.append([y,x])
            temp = temp[::-1]
            seats = seats + temp
        print(seats)
        return seats

    
    def random_seats(self, plane):
        seats = self.all_seats(plane)[::-1]
        random.shuffle(seats)
        return seats
    
    def back_half_to_front_half_seats(self, plane):
        seats = self.out_to_in_seats(plane)
        back_half = seats[:math.floor(len(seats)/2)]
        front_half = seats[math.floor(len(seats)/2):]
        random.shuffle(back_half)
        random.shuffle(front_half)
        new_seats = back_half+front_half
        #print(self.new_seats)
        return new_seats

    

class plane():
    
    ''' planes come as static (for now) 2d array '''
    def __init__(self, width, height):
        self.h, self.w = height, width
        self.seats = [[0 for x in range(self.w)] for y in range(self.h)]
        self.seated_passengers = [[0 for x in range(self.w)] for y in range(self.h)]
        self.boarded_passengers = []
        self.corridor =  math.floor((len(self.seats[0]))/2)


    ''' update positions passengers '''
    def update_position(self, passenger, curr_poss, new_pos):
        self.seats[new_pos[0]][new_pos[1]] = passenger
        self.seats[curr_poss[0]][curr_poss[1]] = 0
        
        
    ''' planes can display the seats (for human consumption) '''
    def display_seats(self):
        print(" -----------------------")
        for row in self.seats:
            x = map(lambda x:"#" if isinstance(x,passenger) else "-", row)
            print(list(x))
        print(" -----------------------")
        
        
    def is_entry_empty(self):
        if isinstance(self.corridor, passenger):
            return False
        else:
            return True
        
        
    def board_passenger(self, passenger):
        self.seats[0][2]= passenger
        system('clear')
        clear_output(wait=True)
        self.display_seats()
        
        
    def any_blockage(self, pnger):
        p_seat = pnger.seat
        p_row = list(map(lambda x:1 if \
                     isinstance(x,passenger) else 0, self.seats[p_seat[0]]))
        
        
        if p_seat[1] < self.corridor: #if left of isle
            sect = p_row[pnger.seat[1]:self.corridor]
            if sum(sect)>0 and pnger.position[1] == self.corridor:
                return sect[::-1].index(1)+1
            else:
                return 0 # "no blockage left"

        elif p_seat[1] > self.corridor: #else right of aisle
            sect = p_row[self.corridor+1:pnger.seat[1]]
            if sum(sect)>0 and pnger.position[1] == self.corridor:
                return sect.index(1)+1
            else:
                return 0 # "no blockage left"


    def all_seated(self):
        bool_all_seated = list(map(lambda x: \
                              True if x.is_seated \
                              else False, self.boarded_passengers))
        if len(self.boarded_passengers) > 0:
            return sum(bool_all_seated) == len(self.boarded_passengers)

    
    def seat_passengers(self):
        i = 0
        while not self.all_seated():
            if self.is_entry_empty() == True and len(passengers) > 0:
                self.boarded_passengers.append(passengers.pop(0))
                self.board_passenger(self.boarded_passengers[-1])
            for bp in self.boarded_passengers:
                if not bp.is_seated:
                    bp.find_seat()
                sleep(0.0025)
            system('clear')
            clear_output(wait=True)
            self.display_seats()
            i+=1
            print(i)
        return i



class passenger():
    
    
    def __init__(self, plane, seat):
        self.plane = plane
        self.seat = seat # row, aisle
        self.position = [0,2] # row, aisle
        self.is_seated = False
        '''can configure skewing this distribution !!! look to print graph'''
        self.luggage_time = \
        '''the below should be a function which is called on initalisation
        it should also increase the range as time passes - finding room for
        lugguage is increasingly harder as more passengers stow their own'''
        random.choices\
            (range(0, 6), weights=(0.2, 0.1, 0.15, 0.15, 0.25, 0.15))
        self.luggage_time = None
        self.wait_block = None
        
        '''add Markov property to increase range as time passes'''
    def adjust_luggage(self, time_passed):
        self.luggage_time = \
        random.choices(range(3, time_passed), \
                       weights=(0.2, 0.1, 0.15, 0.15, 0.25, 0.15))
        return 1
        
    
    def find_seat(self):
        '''NEXT, incorporate wait time if someone blocking seat'''
        if self.position == self.seat:
            if self.is_seated == False:
                self.is_seated = True
        elif self.position[0] == self.seat[0]:
            '''if n people in way, pass n turns'''
            self.move_horizontally()
        else:
            self.move_forward()
    
    def move_forward(self):
        pos = self.position
        if pos[0] < len(self.plane.seats)-1 \
        and isinstance(self.plane.seats[pos[0]+1][2],passenger)==False:
            self.plane.update_position(self, pos, [pos[0]+1, pos[1]])
            pos[0] = pos[0] + 1


    def move_horizontally(self):
        pos = self.position
        blockage = self.plane.any_blockage(self)
        if self.is_seated == True:
            print(self.position, self.seat)
            pass
        elif self.luggage_time == None:
            x = random.choices\
            (range(1, 7), weights=(0.2, 0.1, 0.15, 0.15, 0.25, 0.15))
            self.luggage_time = x[0] - 1
        elif self.luggage_time > 0:
            self.luggage_time -= 1
        elif self.luggage_time == 0:
            if blockage == 0 and self.is_seated == False:
                if pos < self.seat:
                    self.move_right()
                elif pos > self.seat:
                    self.move_left()
            elif blockage > 0 and self.wait_block == None and self.is_seated == False:
                ''' blockage algebra '''
                self.wait_block = blockage*2 - 1
            elif blockage > 0 and self.wait_block > 0 and self.is_seated == False:
                self.wait_block -=1
            elif blockage > 0 and self.wait_block == 0 and self.is_seated == False:
                self.plane.update_position(self, pos, self.seat)
                pos[1] = self.seat[1]
            

    def move_right(self):
        pos = self.position
        self.plane.update_position(self, pos, [pos[0], pos[1]+1])
        pos[1] = pos[1] + 1
        
            
    def move_left(self):
        pos = self.position
        self.plane.update_position(self, pos, [pos[0], pos[1]-1])
        pos[1] = pos[1] - 1






results = []
for r in range (2):
    system('clear')
    #clear_output(wait=True)

    passengers = []
    pl = plane(5,6)
    bs = booking_system()
    #all_seats = bs.all_seats(pl)[::-1]
    
    all_seats = booking_system().random_seats(pl)
    #all_seats = booking_system().out_to_in_seats(pl)
    #all_seats = booking_system().back_half_to_front_half_seats(pl)
    
    #all_seats = [[2,0],[2,1]]
    #all_seats = [[2,1],[2,0]]
    #all_seats = [[2,4],[2,3]]
    #all_seats = [[2,3],[2,4]]
    
    booked_seats = all_seats
    #print(booked_seats)
    sleep(0.5)
    for seat in booked_seats:
        passengers.append(passenger(pl, seat))
    results.append(pl.seat_passengers())
    del(bs)
    del(pl)
    del(all_seats)
print(results)

