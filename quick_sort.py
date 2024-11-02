from manim import *
import random

RUNTIME = 0.01
ARRAY_SIZE = 50
SORTED_COLOR = [TEAL_D, GREEN_D]
BASED_COLOR = [BLUE, BLUE_D]
class QuickSortVisualization(Scene):
    def construct(self):
        # Generate a list of unique integers from 1 to 100
        array = list(range(1, ARRAY_SIZE + 1))
        random.shuffle(array)
        # Add title
        title = Text("Quick Sort", font_size=40)
        title.to_edge(UP)
        self.add(title)
        # Create rectangles for each integer
        rectangles = []
        max_value = max(array)
        width = 14.0 / len(array)  # Total width fits within the frame
        bottom_y = -3  # Set the bottom y-coordinate for all rectangles
        for i, value in enumerate(array):
            rect_height = value / max_value * 6  # Normalize height to fit in frame
            rect = Rectangle(width=width, height=rect_height)
            rect.set_fill(BASED_COLOR, opacity=0.9)
            rect.set_stroke(BLUE_E)
            x_position = -7 + width/2 + i * width
            # Align the bottom edge of the rectangle to bottom_y
            rect.move_to(np.array([x_position, bottom_y, 0]), aligned_edge=DOWN)
            rectangles.append(rect)

        rects = VGroup(*rectangles)
        self.add(rects)

        # Start the Quick Sort animation
        self.wait(1)
        self.quick_sort(array, rectangles, 0, len(array)-1)
        self.wait(0.5)
        # set the rectangles to the final color
        # Show finised text
        finished_text = Text("Finished", font_size=32)
        
        
        finished_text.to_edge(DOWN)
        # add offset to the text
        finished_text.shift(DOWN * 0.2)
        self.play(Write(finished_text), run_time=1)

        for rect in rectangles:
            rect.set_fill(GREEN_C)
            rect.set_stroke(None)
        # remove border of the rectangles

            
        self.wait(0.4)


    def quick_sort(self, array, rectangles, low, high):
        if low < high:
            pi = self.partition(array, rectangles, low, high)
            # if the element is in the correct position
            # The sorted element is colored green
            self.quick_sort(array, rectangles, low, pi - 1)
            self.quick_sort(array, rectangles, pi + 1, high)
        
        

    def partition(self, array, rectangles, low, high):
        pivot_value = array[high]
        pivot_rect = rectangles[high]
        i = low - 1

        # Highlight the pivot
        self.play(pivot_rect.animate.set_fill(RED))

        for j in range(low, high):
            # Highlight the current element being compared
            self.play(rectangles[j].animate.set_fill(YELLOW), run_time=RUNTIME)
            if array[j] < pivot_value:
                i += 1
                if i != j:
                    # Swap the elements in the array
                    array[i], array[j] = array[j], array[i]
                    # Swap the rectangles
                    rectangles[i], rectangles[j] = rectangles[j], rectangles[i]
                    # Animate the swap
                    self.swap_rectangles(rectangles, i, j)
                self.play(rectangles[i].animate.set_fill(BASED_COLOR), run_time=RUNTIME)
            else:
                self.play(rectangles[j].animate.set_fill(BASED_COLOR), run_time=RUNTIME)

        # Swap the pivot to the correct position
        i += 1
        if i != high:
            array[i], array[high] = array[high], array[i]
            rectangles[i], rectangles[high] = rectangles[high], rectangles[i]
            self.swap_rectangles(rectangles, i, high)

        # Reset the pivot color
        self.play(rectangles[i].animate.set_fill(BASED_COLOR), run_time=RUNTIME)
        return i

    def swap_rectangles(self, rectangles, i, j):
        rect_i = rectangles[i]
        rect_j = rectangles[j]
        

        rect_i_target = rect_j#.get_center()
        rect_j_target = rect_i#.get_center()
        
        self.play(
            rect_i.animate.move_to(rect_i_target, aligned_edge=DOWN),
            rect_j.animate.move_to(rect_j_target, aligned_edge=DOWN),
            run_time=RUNTIME
        )

    
