from constants import DEADLOCK_FILTER_2_BY_2, DEADLOCK_FILTER_3_BY_3_1_BOX, DEADLOCK_FILTER_3_BY_3_2_BOX, DEADLOCK_FILTER_3_BY_3_3_BOX, DEADLOCK_FILTER_3_BY_3_4_BOX, DEADLOCK_FILTER_3_BY_3_5_BOX
import numpy as np
import copy


def make_filters_from_list(the_list):
    to_return = []

    for each_filter in the_list:
        to_return.append(np.array([np.array(xi) for xi in each_filter]))
    return to_return

def is_same(region, filter):
    return (region==filter).all()

def generate_permutations(region):
    to_return = []

    normal = region
    flipped_lr = np.fliplr(region)
    flipped_ud = np.flipud(region)

    for i in range(0,4):
        to_return.append(normal)
        to_return.append(flipped_lr)
        to_return.append(flipped_ud)

        normal = np.rot90(normal)
        flipped_lr = np.rot90(flipped_lr)
        flipped_ud = np.rot90(flipped_ud)
    return to_return

class deadlock_detector:
    def __init__(self, number_of_rows, number_of_cols):
        self.number_of_rows = number_of_rows
        self.number_of_cols = number_of_cols

        #2x2 deadlocks:
        self.deadlock_filters_2_by_2 = make_filters_from_list(DEADLOCK_FILTER_2_BY_2)

        #3x3 deadlocks:
        self.deadlock_filter_3_by_3_with_1_box = make_filters_from_list(DEADLOCK_FILTER_3_BY_3_1_BOX)
        self.deadlock_filter_3_by_3_with_2_boxes = make_filters_from_list(DEADLOCK_FILTER_3_BY_3_2_BOX)
        self.deadlock_filter_3_by_3_with_3_boxes = make_filters_from_list(DEADLOCK_FILTER_3_BY_3_3_BOX)
        self.deadlock_filter_3_by_3_with_4_boxes = make_filters_from_list(DEADLOCK_FILTER_3_BY_3_4_BOX)
        self.deadlock_filter_3_by_3_with_5_boxes = make_filters_from_list(DEADLOCK_FILTER_3_BY_3_5_BOX)

        self.box_map_3_by_3 = {1:self.deadlock_filter_3_by_3_with_1_box,
                               2:self.deadlock_filter_3_by_3_with_2_boxes,
                               3:self.deadlock_filter_3_by_3_with_3_boxes,
                               4:self.deadlock_filter_3_by_3_with_4_boxes,
                               5:self.deadlock_filter_3_by_3_with_5_boxes}

    def is_filter_area_in_board(self,top_left_position,bottom_right_position):
        (top_left_i,top_left_j) = top_left_position
        (bottom_right_i, bottom_right_j) = bottom_right_position

        is_top_left_i_in_range = top_left_i >= 0 and top_left_i < self.number_of_rows
        is_top_left_j_in_range  = top_left_j >= 0 and top_left_j < self.number_of_cols
        is_bottom_right_i_in_range = bottom_right_i >= 0 and bottom_right_i < self.number_of_rows
        is_bottom_right_j_in_range = bottom_right_j >= 0 and bottom_right_j < self.number_of_cols

        return is_top_left_i_in_range and is_top_left_j_in_range and is_bottom_right_i_in_range and is_bottom_right_j_in_range

    def check_region_of_board_for_deadlock(self,board,top_left_position,bottom_right_position):
        #1) Get (i,j):
        (top_left_i, top_left_j) = top_left_position
        (bottom_right_i, bottom_right_j) = bottom_right_position

        #2) Get region:
        region = copy.deepcopy(board[top_left_i:bottom_right_i+1,top_left_j:bottom_right_j+1])

        #3) Get size of board and number of boxes:
        region_shape = region.shape
        number_of_boxes = sum(sum(region == 2))
        number_of_boxes_on_storage = sum(sum(region == 5))

        #4) If no boxes in region (i.e. all in region are stored):
        if number_of_boxes == 0:
            return False

        #5) Normalize region:
        region[region == 5] = 2 #make box_on_storage a box
        region[region == 4] = 0 #make player open_space
        region[region == 6] = 3 #make player_on_storage a storage

        #6) Generate permutations (rotation + flips):
        permutations_of_region = generate_permutations(region)

        if region_shape == (2,2):
            filters_to_check = self.deadlock_filters_2_by_2

        elif region_shape == (3,3):
            total_boxes = number_of_boxes + number_of_boxes_on_storage

            if total_boxes in self.box_map_3_by_3.keys():
                filters_to_check = self.box_map_3_by_3[total_boxes]
            else:
                return False
        else:
            print(region_shape)
            print("Warning: Filter is not (2,2) or (3,3)")
            return False

        for each_permutation in permutations_of_region:
            for each_filter in filters_to_check:
                if is_same(region,each_filter):
                    return True
        return False


    def check_deadlock(self,board,position_of_focus):
        """returns True is deadlock is detected, returns false is no deadlock"""

        """
        #Say you have the following grid:
        
        A B C D E F
        G H I J K L
        M N O P Q R
        S T U V W X
        Y Z a b c d
        
        ## Where each letter represents a different tile, i.e. (a box, empty_space, etc.)
        
        ## You need to check all possible deadlock configurations after a box push, so 
        ##  you need to check all 2x2 and 3x3 areas that contain your poisition_of_focus (i.e. box just pushed)
        
        ## ex: Say if O if your position of focus. Do the following checks:
        
        #Check 1: 2x2 where position_of_focus is bottom_right
            H I
            N O

        #Check 2: 2x2 where position of focus is bottom left
            I J
            O P
        
        #Check 3: 2x2 where position_of_focus is top_right
            N O
            T U
        
        #Check 4: 2x2 where position of focus is top left
            O P
            U V
        
        #Check 5: 3x3 where position_of_focus is top left
            O P Q
            U V W
            a b c
        
        #Check 6: 3x3 where position of focus is top middle
            N O P
            U V W
            Z a b
        
        #Check 7: 3x3 where position of focus is top right
            M N O
            S T U
            Y Z a
        
        #Check 8: 3x3 where position_of_focus is middle left
            I J K
            O P Q
            U V W
        
        #Check 9:3x3 where position of focus is middle middle
            H I J
            N O P
            T U V 
        
        #Check 10: 3x3 where position of focus is middle right
            G H I
            M N O
            S T U 
      
        #Check 11: 3x3 where position_of_focus is bottom left
            C D E
            I J K
            O P Q 
        
        #Check 12:3x3 where position of focus is bottom middle
            B C D
            H I J
            N O P
        
        #Check 13: 3x3 where position of focus is bottom right 
            A B C 
            G H I 
            M N O
            
        If none of these checks are deadlocks, then there are no deadlocks in this area.
        """

        (i,j) = position_of_focus #this should be where the crate was pushed to

        #Check 1: 2x2 where position_of_focus is bottom_right
        if self.is_filter_area_in_board((i-1,j-1),(i,j)) and self.check_region_of_board_for_deadlock(board,(i-1,j-1),(i,j)):
            return True

        #Check 2: 2x2 where position of focus is bottom left
        if self.is_filter_area_in_board((i-1,j),(i,j-1)) and self.check_region_of_board_for_deadlock(board,(i-1,j),(i,j-1)):
            return True

        #Check 3: 2x2 where position_of_focus is top_right
        if self.is_filter_area_in_board((i,j-1),(i+1,j)) and self.check_region_of_board_for_deadlock(board,(i,j-1),(i+1,j)):
            return True

        #Check 4: 2x2 where position of focus is top left
        if self.is_filter_area_in_board((i,j),(i+1,j+1)) and self.check_region_of_board_for_deadlock(board,(i,j),(i+1,j+1)):
            return True

        #Check 5: 3x3 where position_of_focus is top left
        if self.is_filter_area_in_board((i,j),(i+2,j+2)) and self.check_region_of_board_for_deadlock(board,(i,j),(i+2,j+2)):
            return True

        #Check 6: 3x3 where position of focus is top middle
        if self.is_filter_area_in_board((i,j-1),(i+2,j+1)) and self.check_region_of_board_for_deadlock(board,(i,j-1),(i+2,j+1)):
            return True

        #Check 7: 3x3 where position of focus is top right
        if self.is_filter_area_in_board((i,j-2),(i+2,j)) and self.check_region_of_board_for_deadlock(board,(i,j-2),(i+2,j)):
            return True

        #Check 8: 3x3 where position_of_focus is middle left
        if self.is_filter_area_in_board((i-1,j),(i+1,j+2)) and self.check_region_of_board_for_deadlock(board,(i-1,j),(i+1,j+2)):
            return True

        #Check 9:3x3 where position of focus is middle middle
        if self.is_filter_area_in_board((i-1,j-1),(i+1,j+1)) and self.check_region_of_board_for_deadlock(board,(i-1,j-1),(i+1,j+1)):
            return True

        #Check 10: 3x3 where position of focus is middle right
        if self.is_filter_area_in_board((i-1,j-2),(i+1,j)) and self.check_region_of_board_for_deadlock(board,(i-1,j-2),(i+1,j)):
            return True

        #Check 11: 3x3 where position_of_focus is bottom left
        if self.is_filter_area_in_board((i-2,j),(i,j+2)) and self.check_region_of_board_for_deadlock(board,(i-2,j),(i,j+2)):
            return True

        #Check 12:3x3 where position of focus is bottom middle
        if self.is_filter_area_in_board((i-2,j-1),(i,j+1)) and self.check_region_of_board_for_deadlock(board,(i-2,j-1),(i,j+1)):
            return True

        #Check 13: 3x2 where position of focus is bottom right
        if self.is_filter_area_in_board((i-2,j-2),(i,j)) and self.check_region_of_board_for_deadlock(board,(i-2,j-2),(i,j)):
            return True

        #if pass all checks return False (no deadlock):
        return False
