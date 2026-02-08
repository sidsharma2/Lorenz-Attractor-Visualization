from manim import *
import numpy as np

# ==========================================
# Lorenz System Physics (RK4)
# ==========================================
SIGMA = 10
RHO = 28
BETA = 8/3

def lorenz_derivatives(state):
    """Compute Lorenz system derivatives."""
    x, y, z = state
    return np.array([
        SIGMA * (y - x),
        x * (RHO - z) - y,
        x * y - BETA * z
    ])

def rk4_step(state, dt):
    """Single RK4 integration step."""
    k1 = lorenz_derivatives(state)
    k2 = lorenz_derivatives(state + 0.5*dt*k1)
    k3 = lorenz_derivatives(state + 0.5*dt*k2)
    k4 = lorenz_derivatives(state + dt*k3)
    return state + (dt/6) * (k1 + 2*k2 + 2*k3 + k4)

def generate_trajectory(initial, dt=0.005, steps=10000):
    """Generate full Lorenz trajectory."""
    trajectory = [initial.copy()]
    state = initial.copy()
    for _ in range(steps):
        state = rk4_step(state, dt)
        trajectory.append(state.copy())
    return np.array(trajectory)

# ==========================================
# Main Animation Scene
# ==========================================
class LorenzChaos(ThreeDScene):
    def construct(self):
        # === CONFIG ===
        self.camera.background_color = "#000000"  # Pure black for contrast
        
        # === PART 1: Title & Introduction (0-5s) ===
        title = Text("The Lorenz Attractor", font_size=72, color=WHITE)
        title.set_color_by_gradient("#4FC3F7", "#0288D1")  # Light blue gradient
        
        subtitle = Text("Deterministic Chaos", font_size=40, color=GRAY_A)
        subtitle.next_to(title, DOWN, buff=0.4)
        
        title_group = VGroup(title, subtitle)
        
        self.play(Write(title), run_time=2)
        self.play(FadeIn(subtitle, shift=UP*0.2), run_time=1)
        self.wait(2)
        
        # === PART 2: Chaos Explanation (5-10s) ===
        explanation = Text(
            '"A tiny change in initial conditions\nleads to dramatically different outcomes."',
            font_size=32,
            color=GRAY_B,
            line_spacing=1.5
        )
        explanation.next_to(title_group, DOWN, buff=1)
        
        self.play(FadeIn(explanation, shift=UP*0.3), run_time=1.5)
        self.wait(2.5)
        
        self.play(
            FadeOut(title_group, shift=UP*0.5),
            FadeOut(explanation, shift=UP*0.3),
            run_time=1
        )
        
        # === PART 3: Equations Display (FIXED IN 2D FRAME) ===
        equations = MathTex(
            r"\frac{dx}{dt} = \sigma(y - x)",
            font_size=44
        )
        eq2 = MathTex(r"\frac{dy}{dt} = x(\rho - z) - y", font_size=44)
        eq3 = MathTex(r"\frac{dz}{dt} = xy - \beta z", font_size=44)
        
        eq2.next_to(equations, DOWN, buff=0.3)
        eq3.next_to(eq2, DOWN, buff=0.3)
        
        eq_group = VGroup(equations, eq2, eq3)
        eq_group.set_color(WHITE)
        
        params = MathTex(
            r"\sigma = 10 \quad \rho = 28 \quad \beta = \tfrac{8}{3}",
            font_size=32,
            color=YELLOW_B
        )
        params.next_to(eq_group, DOWN, buff=0.5)
        
        self.add_fixed_in_frame_mobjects(eq_group, params)
        
        self.play(Write(eq_group), run_time=2.5)
        self.play(FadeIn(params, shift=UP*0.2), run_time=1)
        self.wait(1.5)
        
        eq_small = eq_group.copy().scale(0.3).to_corner(UL, buff=0.3)
        self.play(
            Transform(eq_group, eq_small),
            FadeOut(params),
            run_time=1.2
        )
        
        # === PART 4: Initial Conditions Display ===
        ic_title = Text("Initial Conditions:", font_size=22, color=GRAY_A)
        # Use CYAN for first trajectory (more visible)
        ic_cyan = MathTex(r"\text{Cyan: } x_0 = 0.1", font_size=20, color=TEAL_B)
        # Use ORANGE for second trajectory (high contrast)
        ic_orange = MathTex(r"\text{Orange: } x_0 = 0.1 + 10^{-5}", font_size=20, color=ORANGE)
        ic_diff = MathTex(r"\Delta x_0 = 0.00001", font_size=18, color=YELLOW)
        
        ic_cyan.next_to(ic_title, DOWN, buff=0.12, aligned_edge=LEFT)
        ic_orange.next_to(ic_cyan, DOWN, buff=0.08, aligned_edge=LEFT)
        ic_diff.next_to(ic_orange, DOWN, buff=0.12, aligned_edge=LEFT)
        
        ic_box = VGroup(ic_title, ic_cyan, ic_orange, ic_diff)
        ic_box.to_corner(UR, buff=0.3)
        
        self.add_fixed_in_frame_mobjects(ic_box)
        self.play(FadeIn(ic_box, shift=LEFT*0.3), run_time=1)
        self.wait(0.5)
        
        # === PART 5: 3D Simulation ===
        self.set_camera_orientation(phi=70*DEGREES, theta=-50*DEGREES, zoom=0.7)
        
        # Generate trajectories with LARGER initial difference for visible divergence
        ic_1 = np.array([0.1, 0.0, 0.0])
        ic_2 = np.array([0.1 + 1e-5, 0.0, 0.0])
        
        dt = 0.005
        steps = 10000
        
        traj_1 = generate_trajectory(ic_1, dt, steps)
        traj_2 = generate_trajectory(ic_2, dt, steps)
        
        scale = 0.085
        traj_1_scaled = traj_1 * scale
        traj_2_scaled = traj_2 * scale
        
        # Subtle 3D axes
        axes = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[0, 5, 1],
            x_length=6,
            y_length=6,
            z_length=5,
            axis_config={"color": GRAY_D, "stroke_width": 0.3}
        )
        axes.set_opacity(0.1)
        self.add(axes)
        
        # Evolution time display
        self.time_tracker = ValueTracker(0)
        time_label = always_redraw(
            lambda: Text(
                f"t = {self.time_tracker.get_value():.1f} s",
                font_size=26,
                color=WHITE
            ).to_corner(DR, buff=0.4)
        )
        self.add_fixed_in_frame_mobjects(time_label)
        self.add(time_label)
        
        # HIGH CONTRAST COLORS: CYAN and ORANGE
        # Add CYAN FIRST (will be underneath)
        cyan_path = VMobject(color=TEAL_B, stroke_width=2.5, stroke_opacity=0.95)
        # Add ORANGE SECOND (will be on top, more visible)
        orange_path = VMobject(color=ORANGE, stroke_width=2.5, stroke_opacity=0.95)
        
        # Dots
        cyan_dot = Dot3D(point=traj_1_scaled[0], color=TEAL_B, radius=0.10)
        orange_dot = Dot3D(point=traj_2_scaled[0], color=ORANGE, radius=0.10)
        
        # Add cyan first, orange on top
        self.add(cyan_path, orange_path, cyan_dot, orange_dot)
        
        anim_duration = 35
        
        def update_paths(mob, alpha):
            idx = int(alpha * (steps - 1))
            
            cyan_dot.move_to(traj_1_scaled[idx])
            orange_dot.move_to(traj_2_scaled[idx])
            
            sample_rate = 5
            cyan_points = [traj_1_scaled[i] for i in range(0, idx+1, sample_rate)]
            orange_points = [traj_2_scaled[i] for i in range(0, idx+1, sample_rate)]
            
            if len(cyan_points) > 1:
                cyan_path.set_points_smoothly(cyan_points)
                orange_path.set_points_smoothly(orange_points)
            
            self.time_tracker.set_value(alpha * steps * dt)
        
        # Slow camera pan
        self.begin_ambient_camera_rotation(rate=0.06)
        
        dummy = VMobject()
        self.play(
            UpdateFromAlphaFunc(dummy, update_paths),
            run_time=anim_duration,
            rate_func=linear
        )
        
        self.stop_ambient_camera_rotation()
        
        # === PART 6: Reflect on Divergence ===
        self.wait(1)
        
        divergence_text = Text(
            "Despite nearly identical starting points,",
            font_size=26,
            color=GRAY_A
        )
        divergence_text2 = Text(
            "the trajectories diverge completely.",
            font_size=26,
            color=GRAY_A
        )
        divergence_text2.next_to(divergence_text, DOWN, buff=0.15)
        div_group = VGroup(divergence_text, divergence_text2)
        div_group.to_edge(DOWN, buff=0.4)
        
        self.add_fixed_in_frame_mobjects(div_group)
        self.play(FadeIn(div_group, shift=UP*0.2), run_time=1)
        self.wait(2.5)
        
        # === PART 7: Grand Finale ===
        self.play(
            FadeOut(div_group),
            FadeOut(eq_group),
            FadeOut(ic_box),
            FadeOut(axes),
            run_time=1.2
        )
        
        self.remove(time_label)
        self.wait(1.5)
        
        self.play(
            FadeOut(cyan_path),
            FadeOut(orange_path),
            FadeOut(cyan_dot),
            FadeOut(orange_dot),
            run_time=1.5
        )
        
        # Final message
        chaos_title = Text("CHAOS", font_size=72, color=WHITE, weight=BOLD)
        chaos_subtitle = Text(
            "Sensitivity to Initial Conditions",
            font_size=32,
            color=TEAL_B
        )
        chaos_subtitle.next_to(chaos_title, DOWN, buff=0.4)
        
        chaos_group = VGroup(chaos_title, chaos_subtitle)
        chaos_group.move_to(ORIGIN)
        
        self.add_fixed_in_frame_mobjects(chaos_group)
        self.play(FadeIn(chaos_title, scale=1.1), run_time=1.2)
        self.play(FadeIn(chaos_subtitle, shift=UP*0.2), run_time=0.8)
        self.wait(2.5)
        
        self.play(FadeOut(chaos_group, shift=UP*0.3), run_time=1)
        
        # Creator credit
        credit = Text("Created by", font_size=28, color=GRAY_B)
        name = Text("Sid Sharma", font_size=48, color=WHITE)
        name.next_to(credit, DOWN, buff=0.3)
        
        credit_group = VGroup(credit, name)
        credit_group.move_to(ORIGIN)
        
        self.add_fixed_in_frame_mobjects(credit_group)
        self.play(FadeIn(credit_group, shift=UP*0.2), run_time=1.2)
        self.wait(3)
        self.play(FadeOut(credit_group), run_time=1.5)
        
        self.wait(1)


# Commands:
# Preview (low quality):  manim -pql lorenz_scene.py LorenzChaos
# Medium quality:         manim -pqm lorenz_scene.py LorenzChaos
# High quality (1080p):   manim -pqh lorenz_scene.py LorenzChaos
# 4K render:              manim -pq4k lorenz_scene.py LorenzChaos
