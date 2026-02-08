import dash
from dash import dcc, html, callback_context
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import numpy as np
import threading
import video_renderer # Custom module

# Global State for Export
export_status = "Idle"
export_thread = None

# ==========================================
# 1. Physics Engine: Lorenz Simulator Class (RK4)
# ==========================================
class LorenzSimulator:
    def __init__(self, x0=0.1, y0=0.0, z0=0.0, sigma=10, rho=28, beta=8/3, dt=0.01):
        self.sigma = sigma
        self.rho = rho
        self.beta = beta
        self.dt = dt
        self.reset(x0, y0, z0)

    def reset(self, x0, y0, z0):
        self.x = [x0]
        self.y = [y0]
        self.z = [z0]
        self.t = [0]
    
    def perturb(self, epsilon=1e-2):
        if not self.x: return
        # Small random perturbation vector
        dx = np.random.uniform(-epsilon, epsilon)
        dy = np.random.uniform(-epsilon, epsilon)
        dz = np.random.uniform(-epsilon, epsilon)
        
        x0 = self.x[-1] + dx
        y0 = self.y[-1] + dy
        z0 = self.z[-1] + dz
        self.reset(x0, y0, z0)

    def _derivatives(self, x, y, z):
        dx = self.sigma * (y - x)
        dy = x * (self.rho - z) - y
        dz = x * y - self.beta * z
        return dx, dy, dz

    def step(self, steps=5):
        current_x = self.x[-1]
        current_y = self.y[-1]
        current_z = self.z[-1]
        current_t = self.t[-1]

        for _ in range(steps):
            # RK4 Integration Steps
            k1x, k1y, k1z = self._derivatives(current_x, current_y, current_z)
            
            k2x, k2y, k2z = self._derivatives(current_x + 0.5*self.dt*k1x, 
                                              current_y + 0.5*self.dt*k1y, 
                                              current_z + 0.5*self.dt*k1z)
            
            k3x, k3y, k3z = self._derivatives(current_x + 0.5*self.dt*k2x, 
                                              current_y + 0.5*self.dt*k2y, 
                                              current_z + 0.5*self.dt*k2z)
            
            k4x, k4y, k4z = self._derivatives(current_x + self.dt*k3x, 
                                              current_y + self.dt*k3y, 
                                              current_z + self.dt*k3z)

            current_x += (self.dt / 6.0) * (k1x + 2*k2x + 2*k3x + k4x)
            current_y += (self.dt / 6.0) * (k1y + 2*k2y + 2*k3y + k4y)
            current_z += (self.dt / 6.0) * (k1z + 2*k2z + 2*k3z + k4z)
            current_t += self.dt
            
            self.x.append(current_x)
            self.y.append(current_y)
            self.z.append(current_z)
            self.t.append(current_t)
            
        # Decimation: Keep last N points for LIVE view, but maybe full history for export?
        # If we decimate here, we lose history for export.
        # Solution: Keep full history in separate list? Or just let it grow (memory?)
        # 10k points is fine. 100k is fine.
        # Let's decouple "view" from "state".
        # But for long runs, memory is an issue.
        # For this demo, let's keep 10,000 max.
        max_points = 10000
        if len(self.x) > max_points:
            self.x = self.x[-max_points:]
            self.y = self.y[-max_points:]
            self.z = self.z[-max_points:]
            self.t = self.t[-max_points:]

simulator = LorenzSimulator()

# ==========================================
# 2. UI Layout (Dark Laboratory Theme)
# ==========================================
custom_css = {
    'background-color': '#0f0f13', 
    'color': '#e0e0e0',
    'font-family': 'Roboto, sans-serif'
}

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SLATE])
server = app.server

app.layout = dbc.Container([
    # Header
    dbc.Row([
        dbc.Col([
            html.H1("LORENZ ATTRACTOR // CHAOS LAB", className="display-4 text-center mt-4", style={'letter-spacing': '4px', 'font-weight': '300'}),
            html.H5("High-Fidelity RK4 Simulation + Cinematic Export", className="text-center text-info mb-4", style={'opacity': '0.8'}),
            html.Hr(className="my-2")
        ])
    ]),

    dbc.Row([
        # Sidebar Controls
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("SYSTEM CONTROLS", className="bg-dark text-white font-weight-bold"),
                dbc.CardBody([
                    html.Label("Initial Coordinates (x₀, y₀, z₀)", className="text-muted"),
                    dbc.InputGroup([
                        dbc.Input(id='input-x0', type='number', value=0.1, step=0.1, className="bg-secondary text-white border-0"),
                        dbc.Input(id='input-y0', type='number', value=0.0, step=0.1, className="bg-secondary text-white border-0"),
                        dbc.Input(id='input-z0', type='number', value=0.0, step=0.1, className="bg-secondary text-white border-0"),
                    ], className="mb-4"),

                    html.Label("Perturbation Level (log₁₀ ε)", className="text-muted"),
                    dcc.Slider(
                        id='slider-epsilon',
                        min=-5, max=-1, step=1,
                        marks={i: {'label': f'10^{i}', 'style': {'color': '#aaa'}} for i in range(-5, 0)},
                        value=-2,
                        className="mb-4"
                    ),

                    dbc.ButtonGroup([
                        dbc.Button("▶ RUN / ⏸ PAUSE", id='btn-run', n_clicks=0, color="success", outline=True, className="me-1"),
                        dbc.Button("↺ RESET", id='btn-reset', n_clicks=0, color="danger", outline=True, className="me-1"),
                    ], className="d-grid gap-2 mb-3"),
                    
                    dbc.Button("⚡ PERTURB & RERUN", id='btn-perturb', n_clicks=0, color="warning", className="w-100 font-weight-bold mb-3"),
                    
                    html.Hr(),
                    dbc.Button("🎥 EXPORT VIDEO (MP4)", id='btn-export', n_clicks=0, color="info", className="w-100"),
                    html.Div(id='export-status', className="text-center mt-2 small text-warning")
                ], className="bg-dark")
            ], className="border-secondary mb-3 shadow"),
            
            dbc.Card([
                dbc.CardBody([
                    html.H6("ACADEMIC CONTEXT", className="text-info"),
                    html.P("Exploration of deterministic chaos and sensitivity.", className="small text-muted mb-0"),
                ], className="bg-dark")
            ], className="border-secondary shadow")

        ], width=3),

        # Main Visualization
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='lorenz-plot', style={'height': '75vh'}, config={'scrollZoom': True, 'displayModeBar': True}),
                ], className="p-1 bg-black")
            ], className="border-secondary shadow"),
            
            dcc.Interval(id='interval-component', interval=30, n_intervals=0, disabled=True),
            dcc.Interval(id='export-interval', interval=1000, n_intervals=0) # Check export status
        ], width=9)
    ])
], fluid=True, style=custom_css)

# ==========================================
# 3. Logic & Callbacks
# ==========================================

def run_export_thread(x, y, z):
    global export_status
    export_status = "Rendering 3D Video... (See Console)"
    try:
        success = video_renderer.render_video_from_data(x, y, z, "lorenz_dashboard_export.mp4", duration_sec=10, fps=30)
        if success:
            export_status = "Export Complete: lorenz_dashboard_export.mp4"
        else:
            export_status = "Export Failed"
    except Exception as e:
        export_status = f"Error: {str(e)}"

@app.callback(
    Output('export-status', 'children'),
    [Input('btn-export', 'n_clicks'),
     Input('export-interval', 'n_intervals')],
    [State('btn-run', 'n_clicks')] # To check if running
)
def handle_export(n_clicks, n_intervals, run_clicks):
    global export_status, export_thread
    
    ctx = callback_context
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0] if ctx.triggered else 'export-interval'
    
    if trigger_id == 'btn-export' and n_clicks > 0:
        if export_thread and export_thread.is_alive():
            return "Export already in progress..."
        
        # Start Export Thread
        # Copy data carefully
        x_data = list(simulator.x)
        y_data = list(simulator.y)
        z_data = list(simulator.z)
        
        export_thread = threading.Thread(target=run_export_thread, args=(x_data, y_data, z_data))
        export_thread.start()
        export_status = "Starting Render..."
        
    return export_status

@app.callback(
    [Output('lorenz-plot', 'figure'),
     Output('interval-component', 'disabled')],
    [Input('interval-component', 'n_intervals'),
     Input('btn-run', 'n_clicks'),
     Input('btn-reset', 'n_clicks'),
     Input('btn-perturb', 'n_clicks')],
    [State('lorenz-plot', 'figure'),
     State('interval-component', 'disabled'),
     State('input-x0', 'value'),
     State('input-y0', 'value'),
     State('input-z0', 'value'),
     State('slider-epsilon', 'value')]
)
def update_simulation(n_intervals, run_clicks, reset_clicks, perturb_clicks, 
                      current_fig, is_disabled, x0, y0, z0, log_epsilon):
    
    ctx = callback_context
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0] if ctx.triggered else 'interval-component'

    # Initial Figure Setup (Only run once at start or explicit reset)
    if current_fig is None:
        layout = go.Layout(
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            scene=dict(
                xaxis=dict(visible=False),
                yaxis=dict(visible=False),
                zaxis=dict(visible=False),
                aspectmode='cube',
                camera=dict(eye=dict(x=1.8, y=1.8, z=1.8))
            ),
            margin=dict(l=0, r=0, b=0, t=0),
            showlegend=False
        )
        # Empty trace to start
        return go.Figure(layout=layout), True

    # Controls
    if trigger_id == 'btn-run':
        return dash.no_update, not is_disabled
    
    if trigger_id == 'btn-reset':
        simulator.reset(x0 or 0.1, y0 or 0, z0 or 0)
        fig = go.Figure(layout=current_fig['layout'])
        return fig, True
        
    if trigger_id == 'btn-perturb':
        epsilon = 10**log_epsilon
        simulator.perturb(epsilon)
        fig = go.Figure(layout=current_fig['layout'])
        return fig, False

    # Simulation Step (If interval triggered and not disabled)
    # OR if we just hit 'Run', wait for next interval? No, 'Run' returns 'not disabled', next interval ticks.
    
    if not is_disabled:
        simulator.step(steps=5) # RK4 steps per frame
        
        # Display Decimation (Show only last 2000 for speed)
        # But we KEEP 10000 in simulator.x for export
        view_window = 2000
        x = np.array(simulator.x[-view_window:])
        y = np.array(simulator.y[-view_window:])
        z = np.array(simulator.z[-view_window:])
        
        velocity = np.sqrt(x**2 + y**2 + z**2)
        
        trace = go.Scatter3d(
            x=x, y=y, z=z,
            mode='lines',
            line=dict(
                color=velocity,
                colorscale='Turbo',  # Vibrant gradient
                width=8,  # Thicker line for better visibility
            ),
            opacity=0.95,
            hoverinfo='skip'
        )
        
        head_trace = go.Scatter3d(
            x=[x[-1]], y=[y[-1]], z=[z[-1]],
            mode='markers',
            marker=dict(color='cyan', size=8, symbol='circle'),
            hoverinfo='text',
            text=f"Pos: ({x[-1]:.1f}, {y[-1]:.1f}, {z[-1]:.1f})"
        )
        
        fig = go.Figure(data=[trace, head_trace], layout=current_fig['layout'])
        fig.update_layout(uirevision='constant')
        
        return fig, False

    return dash.no_update, is_disabled

if __name__ == '__main__':
    print("Starting Integrated Lorenz Dashboard...")
    app.run(debug=True)
