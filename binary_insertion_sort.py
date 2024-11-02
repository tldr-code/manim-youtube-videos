from manim import *
import random

class BinaryInsertionSortVisualization(Scene):
    def construct(self):
        # Use your provided array or generate a random one
        array = [13, 3, 72, 10, 91, 22, 51]

        self.sort_animation(array)

    def sort_animation(self, array):
        box_height = 1  # The side length of the squares
        spacing = 1.2   # Spacing between squares

        # Visual representation of the array
        squares = []
        numbers = []
        for i, num in enumerate(array):
            square = Square(side_length=box_height)
            square.shift(RIGHT * i * spacing)
            squares.append(square)
            number = Text(str(num), font_size=36)
            number.move_to(square.get_center())
            numbers.append(number)

        # Group squares and numbers
        array_group = VGroup(*squares, *numbers)
        array_group.move_to(DOWN * 1.1)
        self.play(FadeIn(array_group))

        # Add a title to the scene
        title = Text("Binary Insertion Sort", font_size=48)
        title.to_edge(UP )
        title.shift(DOWN * 0.5)
        self.play(Write(title), run_time=0.8)

        # Perform binary insertion sort with animation
        for i in range(1, len(array)):
            key = array[i]
            key_square = squares[i]
            key_number = numbers[i]

            # Highlight the key element
            self.play(Indicate(key_square, color=YELLOW))
            self.wait(0.6)

            # Display explanatory text instantly with a 0.4-second delay
            explanation = Text(f"Inserting {key} into the sorted portion", font_size=24)
            explanation.next_to(title, DOWN)
            self.add(explanation)
            self.wait(0.8)

            # Find the insertion point using binary search
            insertion_index = self.binary_search(
                array, key, 0, i - 1,
                squares, numbers, explanation,
                box_height, spacing
            )
            SHIFT_FACTOR = 1.25

            # Move the key element to the insertion point
            ANIMATE_BOX_TIME = 0.25
            if insertion_index != i:
                # Move the key element up
                self.play(
                    key_square.animate.shift(UP * box_height * SHIFT_FACTOR),
                    key_number.animate.shift(UP * box_height * SHIFT_FACTOR),
                    run_time=ANIMATE_BOX_TIME
                )

                # Shift elements to the right
                for j in range(i, insertion_index, -1):
                    array[j] = array[j - 1]

                    square_to_move = squares[j - 1]
                    number_to_move = numbers[j - 1]

                    # Shift right
                    self.play(
                        square_to_move.animate.shift(RIGHT * spacing),
                        number_to_move.animate.shift(RIGHT * spacing),
                        run_time=ANIMATE_BOX_TIME
                    )

                    # Update the squares and numbers lists after moving
                    squares[j] = square_to_move
                    numbers[j] = number_to_move

                # Move the key element left to its insertion point
                shift_amount = LEFT * (i - insertion_index) * spacing
                self.play(
                    key_square.animate.shift(shift_amount),
                    key_number.animate.shift(shift_amount),
                    run_time=ANIMATE_BOX_TIME
                )

                # Move the key element down
                self.play(
                    key_square.animate.shift(DOWN * box_height * SHIFT_FACTOR),
                    key_number.animate.shift(DOWN * box_height * SHIFT_FACTOR),
                    run_time=ANIMATE_BOX_TIME
                )

                # Update the squares and numbers lists at the insertion index
                squares[insertion_index] = key_square
                numbers[insertion_index] = key_number
                array[insertion_index] = key

            # Highlight the sorted portion
            for k in range(i + 1):
                squares[k].set_fill(BLUE, opacity=0.5)
            self.wait(0.5)

            # Remove the explanation text without animation
            self.remove(explanation)

        # Final sorted array
        final_text = Text("Array is now sorted!", font_size=32, color=GREEN)
        final_text.next_to(title, DOWN)
        self.add(final_text)
        self.wait(0.8)
        self.play(
            *[Indicate(squares[i], color=GREEN) for i in range(len(array))],
            run_time=1
        )
        self.wait(2)

    def binary_search(self, array, key, start, end, squares, numbers, explanation, box_height, spacing):
        # Define arrow length
        arrow_length = box_height 
        buffd = 0.2
        shift_origin_down = ORIGIN - (DOWN * 0.5)
        # Create pointers with upward arrows
        label_size = 24
        start_pointer = Arrow(start=DOWN * arrow_length, 
                              end=shift_origin_down, 
                              buff=buffd,
                              max_stroke_width_to_length_ratio=2
                              ).set_color(RED)
        start_label = Text("Start", font_size=label_size, color=RED)

        end_pointer = Arrow(start=DOWN * arrow_length, 
                            end=shift_origin_down, 
                            buff=buffd,
                            max_stroke_width_to_length_ratio=2).set_color(BLUE)
        end_label = Text("End", font_size=label_size, color=BLUE)

        mid_pointer = Arrow(start=DOWN * arrow_length, 
                            end=shift_origin_down, 
                            buff=buffd,
                            max_stroke_width_to_length_ratio=2).set_color(ORANGE)
        mid_label = Text("Mid", font_size=label_size, color=ORANGE)

        # Add start and end pointers to the scene
        self.add(start_pointer, start_label, end_pointer, end_label)

        while start <= end:
            mid = (start + end) // 2
            EXPLANATION_TIME = 0.8
            # Position pointers
            self.position_pointers(
                start, end, mid,
                start_pointer, start_label,
                end_pointer, end_label,
                mid_pointer, mid_label,
                squares, spacing
            )

            # Highlight the mid element
            mid_square = squares[mid]
            self.play(Indicate(mid_square, color=ORANGE), run_time=0.8)

            # Display comparison text
            comparison_text = Text(f"Comparing {key} with {array[mid]}", font_size=24)
            comparison_text.next_to(explanation, DOWN * 1.2)
            self.add(comparison_text)
            self.wait(EXPLANATION_TIME)

            if key < array[mid]:
                end = mid - 1
                self.remove(comparison_text)
                direction_text = Text(f"{key} is less than {array[mid]}", font_size=24)
                direction_text.next_to(explanation, DOWN * 1.2)
                self.add(direction_text)
                self.wait(EXPLANATION_TIME)
                self.remove(direction_text)
            else:
                start = mid + 1
                self.remove(comparison_text)
                direction_text = Text(f"{key} is greater than {array[mid]}", font_size=24)
                direction_text.next_to(explanation, DOWN * 1.2)
                self.add(direction_text)
                self.wait(EXPLANATION_TIME)
                self.remove(direction_text)

            # Remove mid pointer after each iteration
            self.remove(mid_pointer, mid_label)

        # Show insertion position
        insertion_text = Text(f"Insert at position {start}", font_size=24)
        insertion_text.next_to(explanation, DOWN)
        self.add(insertion_text)
        self.wait(EXPLANATION_TIME)
        self.remove(insertion_text)

        # Remove pointers
        self.remove(start_pointer, start_label, end_pointer, end_label)

        return start

    def position_pointers(self, start, end, mid,
                          start_pointer, start_label,
                          end_pointer, end_label,
                          mid_pointer, mid_label,
                          squares, spacing):
        # Function to position the pointers with arrowheads under the boxes

        # Helper function to position a pointer and label
        def position_pointer(pointer, label, index):
            # Calculate the shift needed to place the arrowhead at the bottom of the square
            target_point = squares[index].get_bottom()
            shift_vector = target_point - pointer.get_end()
            pointer.shift(shift_vector)
            # Position the label at the tail of the arrow
            label.next_to(pointer.get_start(), DOWN, buff=0.05)

        # Position the start pointer and label
        position_pointer(start_pointer, start_label, start)

        # Position the end pointer and label
        position_pointer(end_pointer, end_label, end)

        # Position the mid pointer and label
        position_pointer(mid_pointer, mid_label, mid)
        self.add(mid_pointer, mid_label)

        # Adjust labels if pointers overlap
        pointers = [
            (start_pointer, start_label),
            (end_pointer, end_label),
            (mid_pointer, mid_label)
        ]

        # Create a dictionary to track occupied positions
        occupied_positions = {}

        for pointer, label in pointers:
            pos = np.round(pointer.get_end()[0], decimals=2)
            if pos in occupied_positions:
                # Shift label down to avoid overlap
                overlap_count = occupied_positions[pos]
                label.shift(DOWN * 0.32 * overlap_count)
                occupied_positions[pos] += 1
            else:
                occupied_positions[pos] = 1
