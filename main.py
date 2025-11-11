from click.core import V
from manim import *
import numpy as np

class RadarToScreen(Scene):
    def construct(self):
        words = [
            ("radio", {'ra': RED}),
            ("detection", {'d': RED}),
            ("and", {'a': RED}),
            ("ranging", {'r': RED}),
        ]
        texts = [Text(word, t2c=t2c, font_size=48) for word, t2c in words]

        # Position each text below the previous, aligned left
        for i in range(1, len(texts)):
            texts[i].next_to(texts[i-1], DOWN, aligned_edge=LEFT)

        text_group = VGroup(*texts).move_to(ORIGIN).shift(LEFT * 1.5)

        for txt in texts:
            self.play(Write(txt), run_time=0.5)
        self.wait(0.3)

        self.play(FadeOut(text_group), run_time=0.7)
        self.wait(2)

class RadarSpectrum(Scene):
    def construct(self):
        radiowave = Text("Radio waves", font_size=48, slant=ITALIC)

        self.play(FadeIn(radiowave, shift=UP))
        self.wait(0.7)

        # Move radiowave down and start drawing the chirp...
        self.play(radiowave.animate.shift(DOWN * 2), run_time=0.7, rate_func=rate_functions.smooth)

        f_0 = 0                # start frequency
        k   = 2                # chirp rate (Hz/s)
        t_max = 3.0            # <-- change this to see more/less of the chirp

        # Build the graph within t_max
        chirp_graph = FunctionGraph(
            lambda t: np.sin(2 * np.pi * (f_0 * t + k/2 * t**2)),
            x_range=[0, t_max, 0.01],   # start, stop, step
            color=RED
        )

        chirp_graph.move_to(ORIGIN)

        # Create the frequency range line above the graph
        line_start = chirp_graph.get_start() + LEFT * 0.1
        line_end = chirp_graph.get_end() + RIGHT * 0.1
        frequency_line = Line(line_start + UP * 1.5, line_end + UP * 1.5, color=WHITE)

        left_label = Text("3 kHz", font_size=24).next_to(frequency_line.get_start(), LEFT, buff=0.2)
        right_label = Text("300 GHz", font_size=24).next_to(frequency_line.get_end(), RIGHT, buff=0.2)

        label_group = VGroup(left_label, right_label)

        self.play(Create(frequency_line), FadeIn(label_group), run_time=0.5)
        self.wait(0.3)
        self.play(Create(chirp_graph), run_time=2)
        self.wait(1)
        self.play(FadeOut(chirp_graph), FadeOut(frequency_line), FadeOut(label_group) , FadeOut(radiowave), run_time=0.7)
        self.wait(1)


class PlaneRadar(Scene):
    def construct(self):
        # Create the vertical rod (antenna mast)
        rod_height = 1
        rod = Line(ORIGIN, UP * rod_height, color=WHITE, stroke_width=8)

        # Create the hollow circle at the top of the antenna mast
        circle_radius = 0.2
        circle = Circle(radius=circle_radius, color=WHITE, stroke_width=8, fill_opacity=0)
        circle.move_to(rod.get_end() + UP * circle_radius)

        antenna = VGroup(rod, circle)
        antenna.move_to(LEFT * 5)

        plane_img = ImageMobject("plane.png")
        plane_img.scale(0.5)
        plane_img.move_to(RIGHT * 5)

        self.play(
            Create(rod),
            FadeIn(plane_img),
            run_time=1
        )
        self.play(Create(circle), run_time=0.4)

        # Create a propagating sine wave that moves toward the plane
        wave_freq = 7  
        wave_length = 3 * (2 * np.pi / wave_freq)  # 3 periods

        leading_edge = ValueTracker(-1)  
        trailing_edge = ValueTracker(-1 - wave_length)  
        wave_opacity = ValueTracker(0) 

        def create_propagating_wave():
            lead = leading_edge.get_value()
            trail = trailing_edge.get_value()

            if lead > trail:
                wave = FunctionGraph(
                    lambda x: np.sin(wave_freq * x), 
                    x_range=[trail, lead, 0.01],
                    color=BLUE,
                    stroke_width=3,
                    fill_opacity=0
                )
                wave.set_stroke(opacity=wave_opacity.get_value())
                return wave
            else:
                # Return empty group if no wave to show
                return VGroup()

        propagating_wave = always_redraw(create_propagating_wave)

        self.add(propagating_wave)

        final_position = 4  

        self.play(
            leading_edge.animate.set_value(final_position),
            trailing_edge.animate.set_value(final_position - wave_length),
            wave_opacity.animate.set_value(1).set_rate_func(rate_functions.ease_out_expo),
            run_time=1.5,
            rate_func=rate_functions.linear
        )

        self.remove(propagating_wave) 

        echo_leading = ValueTracker(4)  
        echo_trailing = ValueTracker(4 - wave_length)  
        echo_opacity = ValueTracker(1)  

        def create_echo_wave():
            lead = echo_leading.get_value()
            trail = echo_trailing.get_value()

            if lead > trail:
                wave = FunctionGraph(
                    lambda x: np.sin(wave_freq * x),  
                    x_range=[trail, lead, 0.01],
                    color=RED,  
                    stroke_width=3,
                    fill_opacity=0  
                )
                wave.set_stroke(opacity=echo_opacity.get_value())
                return wave
            else:
                return VGroup()

        echo_wave = always_redraw(create_echo_wave)
        self.add(echo_wave)

        self.play(
            echo_leading.animate.set_value(-1.8),  
            echo_trailing.animate.set_value(-1.8 - wave_length),  
            run_time=2,
            rate_func=rate_functions.ease_out_sine
        )

        self.wait(1)

        self.play(
            FadeOut(antenna),
            FadeOut(plane_img),
            FadeOut(echo_wave),
            run_time=1.5
        )

        self.wait(1)

class SimpleRangeCalculation(Scene):
    def construct(self):
        eq = MathTex(
            r"R = c \times \frac{t}{2}",
        )
        eq.move_to(ORIGIN)

        self.play(Write(eq))
        self.wait(0.5)

        self.play(eq[0][0].animate.set_color(RED), run_time=0.2)
        self.wait(0.5)
        self.play(eq[0][0].animate.set_color(WHITE), run_time=0.2)
        self.wait(0.3)
        self.play(eq[0][2].animate.set_color(RED), run_time=0.2)
        self.wait(0.5)
        self.play(eq[0][2].animate.set_color(WHITE), run_time=0.2)
        self.wait(0.3)
        self.play(eq[0][4].animate.set_color(RED), run_time=0.2)
        self.wait(0.6)
        self.play(eq[0][4].animate.set_color(WHITE), run_time=0.2)
        self.wait(2)

        rod_height = 1
        rod = Line(ORIGIN, UP * rod_height, color=WHITE, stroke_width=8)

        circle_radius = 0.2
        circle = Circle(radius=circle_radius, color=WHITE, stroke_width=8, fill_opacity=0)
        circle.move_to(rod.get_end() + UP * circle_radius)

        antenna = VGroup(rod, circle)
        antenna.move_to(LEFT * 5 + DOWN * 2) 

        plane_img = ImageMobject("plane.png")
        plane_img.scale(0.5)
        plane_img.move_to(RIGHT * 5 + DOWN * 2) 

        self.play(
            eq.animate.shift(UP * 2),
            FadeIn(antenna),
            FadeIn(plane_img),
            run_time=1.5
        )

        time_tracker = ValueTracker(0)

        def create_time_display():
            current_time = time_tracker.get_value()
            time_text = f"{current_time:.0f} µs"
            display = Text(time_text, font_size=36, color=YELLOW)
            display.move_to(RIGHT * 4 + UP * 1.5) 
            return display

        time_display = always_redraw(create_time_display)
        self.add(time_display)

    
        wave_freq = 7
        wave_length = 3 * (2 * np.pi / wave_freq) 

        leading_edge = ValueTracker(-1)
        trailing_edge = ValueTracker(-1 - wave_length)
        wave_opacity = ValueTracker(0)

        def create_propagating_wave():
            lead = leading_edge.get_value()
            trail = trailing_edge.get_value()

            if lead > trail:
                wave = FunctionGraph(
                    lambda x: np.sin(wave_freq * x),
                    x_range=[trail, lead, 0.01],
                    color=BLUE,
                    stroke_width=3,
                    fill_opacity=0
                )
                wave.set_stroke(opacity=wave_opacity.get_value())
                wave.shift(DOWN * 2)  # Position below the equation
                return wave
            else:
                # Return empty group if no wave to show
                return VGroup()

        propagating_wave = always_redraw(create_propagating_wave)

        self.add(propagating_wave)

        final_position = 4

        self.play(
            leading_edge.animate.set_value(final_position),
            trailing_edge.animate.set_value(final_position - wave_length),
            wave_opacity.animate.set_value(1).set_rate_func(rate_functions.ease_out_expo),
            time_tracker.animate.set_value(142.67),
            run_time=1.5,
            rate_func=rate_functions.linear
        )

        self.remove(propagating_wave)

        echo_leading = ValueTracker(4)
        echo_trailing = ValueTracker(4 - wave_length)
        echo_opacity = ValueTracker(1)

        def create_echo_wave():
            lead = echo_leading.get_value()
            trail = echo_trailing.get_value()

            if lead > trail:
                wave = FunctionGraph(
                    lambda x: np.sin(wave_freq * x),
                    x_range=[trail, lead, 0.01],
                    color=RED,
                    stroke_width=3,
                    fill_opacity=0
                )
                wave.set_stroke(opacity=echo_opacity.get_value())
                wave.shift(DOWN * 2)  # Position below the equation
                return wave
            else:
                return VGroup()

        echo_wave = always_redraw(create_echo_wave)
        self.add(echo_wave)

        self.play(
            echo_leading.animate.set_value(-1.8),
            echo_trailing.animate.set_value(-1.8 - wave_length),
            time_tracker.animate.set_value(333),
            run_time=2,
            rate_func=rate_functions.ease_out_sine
        )

        self.wait(1)

        self.play(eq.animate.move_to(ORIGIN),
                  FadeOut(antenna),
                  FadeOut(plane_img),
                  FadeOut(echo_wave),
                  FadeOut(time_display),
                  run_time=0.5)

        eq2 = MathTex(
            r"R &= c \times \frac{t}{2}\\ &=3 \times 10^8 \times \frac{333 \mu s}{2}\\ &=50 \text{km}",
        )
        self.play(Transform(eq, eq2))
        self.wait(1)

        eq3 = MathTex(
            r"R = \sqrt[4]{ \frac{P_t G^2 \sigma_{rcs} }{ (4 \pi)^2 P_r} }"
        )

        self.play(Transform(eq, eq3))
        self.wait(1)
        self.play(Unwrite(eq), run_time=0.8)
        self.wait(0.5)

class DopplerEffectText(Scene):
    def construct(self):
        text = Text("Doppler Effect", font_size=48, slant=ITALIC)
        text.move_to(ORIGIN)

        self.play(Write(text))
        self.wait(1)
        self.play(Unwrite(text), run_time=0.8)
        self.wait(0.5)

class DopplerFormula(Scene):
    def construct(self):
        eq = MathTex(
            r"v = \dfrac{\Delta f \cdot c}{2 f_t}"
        )
        eq.move_to(ORIGIN)

        self.play(Write(eq))
        self.wait(1)
        self.play(Unwrite(eq), run_time=0.8)
        self.wait(0.5)