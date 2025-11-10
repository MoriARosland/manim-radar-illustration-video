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
