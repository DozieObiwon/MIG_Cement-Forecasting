import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error
import dash
from dash import dcc, html, dash_table, callback, Input, Output
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")

# Load the necessary data
DATA_DIR = Path(__file__).resolve().parents[1] / "data" / "processed"
kpi_summary = pd.read_csv(DATA_DIR / "MIG_kpi_summary.csv")
results_df = pd.read_parquet(DATA_DIR / "cement_forecast_results.parquet")

# Ensure correct data types
results_df["date"] = pd.to_datetime(results_df["date"])

# Initialize Dash app with Bootstrap styling
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "MIG Cement Operational Planner"

# Custom CSS for white theme with glass-morphism
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
        <style>
            * {
                font-family: 'Inter', sans-serif;
            }
            
            body {
                background: linear-gradient(135deg, #f0f4f8 0%, #e8edf3 50%, #dce4ed 100%);
                min-height: 100vh;
                margin: 0;
                padding: 0;
            }
            
            .main-container {
                min-height: 100vh;
                padding: 20px;
                background: rgba(255, 255, 255, 0.4);
                backdrop-filter: blur(10px);
            }
            
            .glass-card {
                background: rgba(255, 255, 255, 0.7);
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.8);
                border-radius: 20px;
                box-shadow: 0 8px 32px rgba(21, 99, 116, 0.08);
                transition: all 0.3s ease;
                overflow: hidden;
                position: relative;
            }
            
            .glass-card::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: linear-gradient(135deg, rgba(255, 255, 255, 0.4) 0%, transparent 100%);
                pointer-events: none;
            }
            
            .glass-card:hover {
                transform: translateY(-3px);
                box-shadow: 0 12px 40px rgba(21, 99, 116, 0.15);
                border-color: rgba(21, 99, 116, 0.2);
            }
            
            .kpi-card {
                background: rgba(255, 255, 255, 0.75);
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.9);
                border-radius: 16px;
                padding: 20px;
                transition: all 0.3s ease;
                position: relative;
                overflow: hidden;
                height: 130px;
                display: flex;
                flex-direction: column;
                justify-content: center;
                box-shadow: 0 4px 16px rgba(21, 99, 116, 0.06);
            }
            
            .kpi-card::after {
                content: '';
                position: absolute;
                top: -50%;
                right: -50%;
                width: 100%;
                height: 100%;
                background: radial-gradient(circle, rgba(21, 99, 116, 0.03) 0%, transparent 70%);
                pointer-events: none;
            }
            
            .kpi-card:hover {
                transform: translateY(-2px);
                box-shadow: 0 8px 24px rgba(21, 99, 116, 0.12);
                border-color: rgba(21, 99, 116, 0.2);
            }
            
            .kpi-value {
                font-size: 28px;
                font-weight: 700;
                color: #1a2a3a;
                margin: 4px 0;
                letter-spacing: -0.5px;
            }
            
            .kpi-label {
                font-size: 13px;
                font-weight: 500;
                color: #5a6a7a;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
            
            .kpi-accent {
                position: absolute;
                top: 0;
                left: 0;
                width: 4px;
                height: 100%;
                background: linear-gradient(180deg, #156374, #1a8a9e);
                border-radius: 4px 0 0 4px;
            }
            
            .title-primary {
                color: #1a2a3a;
                font-weight: 700;
                font-size: 2.2rem;
                letter-spacing: -1px;
            }
            
            .title-accent {
                color: #156374;
            }
            
            .subtitle {
                color: #5a6a7a;
                font-weight: 300;
                font-size: 16px;
            }
            
            .dropdown-container {
                background: rgba(255, 255, 255, 0.7);
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.8);
                border-radius: 12px;
                padding: 12px 16px;
                box-shadow: 0 4px 16px rgba(21, 99, 116, 0.06);
                position: relative;
                z-index: 1000;
            }
            
            .dropdown-container label {
                color: #2a3a4a;
                font-weight: 500;
                font-size: 14px;
                letter-spacing: 0.3px;
            }
            
            /* Fix for dropdown z-index */
            .Select {
                position: relative;
                z-index: 1000;
            }
            
            .Select-control {
                background: rgba(255, 255, 255, 0.8) !important;
                border: 1px solid rgba(21, 99, 116, 0.15) !important;
                border-radius: 8px !important;
                color: #1a2a3a !important;
                box-shadow: 0 2px 8px rgba(21, 99, 116, 0.04);
                position: relative;
                z-index: 1000;
            }
            
            .Select-control:hover {
                border-color: #156374 !important;
            }
            
            .Select-menu-outer {
                background: #ffffff !important;
                border: 1px solid rgba(21, 99, 116, 0.1) !important;
                backdrop-filter: blur(10px);
                box-shadow: 0 8px 24px rgba(21, 99, 116, 0.15);
                z-index: 9999 !important;
                position: absolute !important;
                max-height: 300px !important;
                overflow-y: auto !important;
            }
            
            .Select-menu {
                max-height: 280px !important;
                overflow-y: auto !important;
            }
            
            .Select-option {
                color: #1a2a3a !important;
                background: transparent !important;
                padding: 8px 12px !important;
                cursor: pointer !important;
            }
            
            .Select-option.is-focused {
                background: rgba(21, 99, 116, 0.08) !important;
                color: #156374 !important;
            }
            
            .Select-option.is-selected {
                background: rgba(21, 99, 116, 0.12) !important;
                color: #156374 !important;
            }
            
            .Select-value-label {
                color: #1a2a3a !important;
            }
            
            .Select-placeholder {
                color: #8a9aaa !important;
            }
            
            .Select-clear-zone, .Select-arrow-zone {
                color: #5a6a7a !important;
            }
            
            /* Fix for dropdown in modal/popup contexts */
            .is-open .Select-menu-outer {
                z-index: 9999 !important;
            }
            
            /* Ensure dropdown appears above all content */
            .Select.is-open {
                z-index: 9999 !important;
            }
            
            .chart-container {
                background: rgba(255, 255, 255, 0.7);
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.8);
                border-radius: 16px;
                padding: 20px;
                transition: all 0.3s ease;
                box-shadow: 0 4px 16px rgba(21, 99, 116, 0.06);
                position: relative;
                z-index: 1;
            }
            
            .chart-container:hover {
                border-color: rgba(21, 99, 116, 0.2);
                box-shadow: 0 8px 32px rgba(21, 99, 116, 0.1);
            }
            
            .table-container {
                background: rgba(255, 255, 255, 0.7);
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.8);
                border-radius: 16px;
                padding: 20px;
                max-height: 450px;
                overflow-y: auto;
                box-shadow: 0 4px 16px rgba(21, 99, 116, 0.06);
                position: relative;
                z-index: 1;
            }
            
            .table-container::-webkit-scrollbar {
                width: 8px;
            }
            
            .table-container::-webkit-scrollbar-track {
                background: rgba(21, 99, 116, 0.05);
                border-radius: 4px;
            }
            
            .table-container::-webkit-scrollbar-thumb {
                background: linear-gradient(180deg, #156374, #1a8a9e);
                border-radius: 4px;
            }
            
            .table-container::-webkit-scrollbar-thumb:hover {
                background: #156374;
            }
            
            .section-title {
                color: #1a2a3a;
                font-weight: 600;
                font-size: 1.1rem;
                margin-bottom: 16px;
                display: flex;
                align-items: center;
                gap: 10px;
            }
            
            .section-title::after {
                content: '';
                flex: 1;
                height: 2px;
                background: linear-gradient(90deg, rgba(21, 99, 116, 0.2), transparent);
            }
            
            .dash-table-container {
                background: transparent !important;
            }
            
            .dash-spreadsheet-container {
                background: transparent !important;
            }
            
            .dash-spreadsheet {
                background: transparent !important;
                color: #1a2a3a !important;
            }
            
            .dash-spreadsheet td {
                color: #2a3a4a !important;
                background: transparent !important;
                border-bottom: 1px solid rgba(21, 99, 116, 0.06) !important;
            }
            
            .dash-spreadsheet th {
                color: #1a2a3a !important;
                background: rgba(21, 99, 116, 0.06) !important;
                border-bottom: 2px solid rgba(21, 99, 116, 0.15) !important;
                font-weight: 600 !important;
            }
            
            .dash-spreadsheet tr:hover td {
                background: rgba(21, 99, 116, 0.04) !important;
            }
            
            .dash-spreadsheet tr:nth-child(even) td {
                background: rgba(21, 99, 116, 0.02) !important;
            }
            
            .section-spacing {
                margin-top: 24px;
            }
            
            @media (max-width: 768px) {
                .kpi-value {
                    font-size: 22px;
                }
                .title-primary {
                    font-size: 1.8rem;
                }
                .kpi-card {
                    height: 110px;
                    padding: 16px;
                }
                .Select-menu-outer {
                    max-width: 90vw !important;
                }
            }
            
            .status-badge {
                display: inline-block;
                padding: 3px 12px;
                border-radius: 20px;
                font-size: 11px;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.3px;
            }
            
            .badge-success { background: rgba(21, 99, 116, 0.1); color: #156374; }
            .badge-warning { background: rgba(255, 193, 7, 0.15); color: #856404; }
            .badge-danger { background: rgba(220, 53, 69, 0.1); color: #721c24; }
            
            .glass-divider {
                height: 1px;
                background: linear-gradient(90deg, transparent, rgba(21, 99, 116, 0.1), transparent);
                margin: 20px 0;
            }
            
            /* Loading spinner */
            .loading-spinner {
                border: 3px solid rgba(21, 99, 116, 0.1);
                border-top: 3px solid #156374;
                border-radius: 50%;
                width: 40px;
                height: 40px;
                animation: spin 1s linear infinite;
                margin: 20px auto;
            }
            
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            
            /* Ensure dropdown container has proper z-index context */
            .row:first-child {
                position: relative;
                z-index: 100;
            }
        </style>
    </head>
    <body>
        <div class="main-container">
            {%app_entry%}
        </div>
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# =======================
# App Layout
# =======================
app.layout = dbc.Container([
    # Header
    html.Div([
        html.H1([
            "MIG Cement ",
            html.Span("Operational Planner", className="title-accent")
        ], className="title-primary text-center mb-2"),
        html.P("Real-time inventory optimization and demand forecasting", 
               className="subtitle text-center mb-4")
    ], className="mb-4"),
    
    # Site Selection - With higher z-index context
    dbc.Row([
        dbc.Col([
            html.Div([
                html.Label("Select Site", className="mb-2 d-block"),
                dcc.Dropdown(
                    id="site-dropdown",
                    options=[{"label": s, "value": s} for s in sorted(results_df["site_id"].unique())],
                    value=sorted(results_df["site_id"].unique())[0],
                    clearable=False,
                    style={'position': 'relative', 'zIndex': 9999}
                )
            ], className="dropdown-container", style={'position': 'relative', 'zIndex': 9999})
        ], width=6, lg=4, xl=3)
    ], className="mb-4", style={'position': 'relative', 'zIndex': 1000}),
    
    # KPI Cards - Lower z-index
    dbc.Row(id="kpi-cards", className="mb-4 g-3", style={'position': 'relative', 'zIndex': 1}),
    
    # Forecast Model Comparison
    dbc.Row([
        dbc.Col([
            html.Div([
                html.Div("Forecast Model Comparison (Test Period)", className="section-title"),
                dash_table.DataTable(
                    id="model-comparison-table",
                    columns=[
                        {"name": "Model", "id": "model"},
                        {"name": "MAE (t)", "id": "mae"},
                        {"name": "RMSE (t)", "id": "rmse"}
                    ],
                    data=[],
                    style_table={"overflowX": "auto"},
                    style_cell={
                        "textAlign": "center",
                        "padding": "12px 16px",
                        "fontSize": "14px",
                        "color": "#2a3a4a",
                        "background": "transparent",
                        "border": "none"
                    },
                    style_header={
                        "backgroundColor": "rgba(21, 99, 116, 0.06)",
                        "fontWeight": "600",
                        "color": "#1a2a3a",
                        "borderBottom": "2px solid rgba(21, 99, 116, 0.15)",
                        "padding": "12px 16px"
                    }
                ),
                html.Div(id="model-comparison-note", className="subtitle mt-2")
            ], className="table-container")
        ], width=12)
    ], className="mb-4"),
    
    # Inventory Time Series
    dbc.Row([
        dbc.Col([
            html.Div([
                html.Div("Inventory and Demand Analysis", className="section-title"),
                dcc.Graph(id="inventory-timeseries", config={'displayModeBar': False})
            ], className="chart-container")
        ], width=12)
    ], className="mb-4"),
    
    # Reorder Recommendations
    dbc.Row([
        dbc.Col([
            html.Div([
                html.Div("Upcoming Reorder Recommendations", className="section-title"),
                html.Div(
                    dash_table.DataTable(
                        id="reorder-table",
                        columns=[
                            {"name": "Date", "id": "date"},
                            {"name": "Inventory (t)", "id": "sim_inventory"},
                            {"name": "Delivery Date", "id": "recommended_delivery_date"},
                            {"name": "Quantity (t)", "id": "recommended_delivery_quantity"},
                            {"name": "Rain Buffer", "id": "buffer_applied"}
                        ],
                        style_table={"overflowX": "auto"},
                        style_cell={
                            "textAlign": "center", 
                            "padding": "12px 16px",
                            "fontSize": "14px",
                            "color": "#2a3a4a",
                            "background": "transparent",
                            "border": "none"
                        },
                        style_header={
                            "backgroundColor": "rgba(21, 99, 116, 0.06)",
                            "fontWeight": "600",
                            "color": "#1a2a3a",
                            "borderBottom": "2px solid rgba(21, 99, 116, 0.15)",
                            "padding": "12px 16px"
                        },
                        page_size=5,
                        style_data_conditional=[
                            {
                                'if': {'row_index': 'odd'},
                                'backgroundColor': 'rgba(21, 99, 116, 0.02)'
                            },
                            {
                                'if': {'row_index': 'even'},
                                'backgroundColor': 'transparent'
                            }
                        ]
                    ),
                    className="table-container"
                )
            ])
        ], width=12)
    ])
], fluid=True, className="px-4 py-3")

# =======================
# Callbacks
# =======================
@app.callback(
    [Output("inventory-timeseries", "figure"),
     Output("reorder-table", "data"),
     Output("model-comparison-table", "data"),
     Output("model-comparison-note", "children"),
     Output("kpi-cards", "children")],
    [Input("site-dropdown", "value")]
)
def update_planner_dashboard(site_id):
    site_df = results_df[results_df["site_id"] == site_id].copy()
    has_model_comparison = "random_forest_forecast" in site_df.columns
    
    # KPI Calculations
    total_forecast = site_df["forecasted_consumption"].sum()
    total_reorders = site_df["reorder_flag"].sum()
    avg_inventory = site_df["sim_inventory"].mean()
    silo_capacity = kpi_summary[kpi_summary['site_id'] == site_id]['silo_capacity'].values[0]
    utilization = (avg_inventory/silo_capacity)*100
    
    # KPI Cards with glass-morphism and accent bars
    kpi_cards = [
        dbc.Col(
            html.Div([
                html.Div(className="kpi-accent"),
                html.Div(f"{total_forecast:,.0f}", className="kpi-value"),
                html.Div(
                    "Total CatBoost Forecasted Consumption" if has_model_comparison
                    else "Total Forecasted Consumption",
                    className="kpi-label"
                )
            ], className="kpi-card"),
            width=6, md=3
        ),
        dbc.Col(
            html.Div([
                html.Div(className="kpi-accent", style={'background': 'linear-gradient(180deg, #1a8a9e, #156374)'}),
                html.Div(f"{total_reorders}", className="kpi-value"),
                html.Div("Planned Reorders", className="kpi-label")
            ], className="kpi-card"),
            width=6, md=3
        ),
        dbc.Col(
            html.Div([
                html.Div(className="kpi-accent", style={'background': 'linear-gradient(180deg, #2a9aae, #1a7a8e)'}),
                html.Div(f"{avg_inventory:,.0f}", className="kpi-value"),
                html.Div("Average Inventory (t)", className="kpi-label")
            ], className="kpi-card"),
            width=6, md=3
        ),
        dbc.Col(
            html.Div([
                html.Div(className="kpi-accent", style={'background': 'linear-gradient(180deg, #3aaaaa, #2a8a9e)'}),
                html.Div(f"{utilization:.1f}%", className="kpi-value"),
                html.Div("Capacity Utilization", className="kpi-label")
            ], className="kpi-card"),
            width=6, md=3
        )
    ]

    if has_model_comparison:
        actual = site_df["consumed_tonnes"]
        model_comparison = []
        for model_name, prediction_column in [
            ("CatBoost", "forecasted_consumption"),
            ("Random Forest", "random_forest_forecast")
        ]:
            predictions = site_df[prediction_column]
            model_comparison.append({
                "model": model_name,
                "mae": f"{mean_absolute_error(actual, predictions):.2f}",
                "rmse": f"{np.sqrt(mean_squared_error(actual, predictions)):.2f}"
            })
        comparison_note = "Lower MAE and RMSE indicate more accurate forecasts."
    else:
        model_comparison = []
        comparison_note = (
            "Comparison data is not available in the current results file. "
            "Re-run the forecasting pipeline and save the results to enable it."
        )
    
    # Time Series Plot - Enhanced with clean white theme
    fig = go.Figure()
    
    # Inventory area with gradient
    fig.add_trace(go.Scatter(
        x=site_df["date"], 
        y=site_df["sim_inventory"],
        mode="lines", 
        name="Inventory Level",
        line=dict(color="#156374", width=2.5),
        fill='tozeroy',
        fillcolor='rgba(21, 99, 116, 0.1)',
        hovertemplate='<b>%{x|%Y-%m-%d}</b><br>Inventory: %{y:,.0f} t<extra></extra>'
    ))
    
    # Capacity line
    fig.add_hline(
        y=silo_capacity, 
        line_dash="dash", 
        line_color="#dc3545",
        line_width=1.5,
        annotation_text=f"Capacity: {silo_capacity:,.0f} t",
        annotation_position="top right",
        annotation_font=dict(color="#dc3545", size=11)
    )
    
    # Forecasted consumption bars
    fig.add_trace(go.Bar(
        x=site_df["date"], 
        y=site_df["forecasted_consumption"],
        name="CatBoost Forecast" if has_model_comparison else "Forecasted Demand",
        yaxis="y2",
        opacity=0.4,
        marker_color='rgba(255, 193, 7, 0.5)',
        marker_line_color='rgba(255, 193, 7, 0.3)',
        marker_line_width=1,
        hovertemplate='<b>%{x|%Y-%m-%d}</b><br>Demand: %{y:,.0f} t<extra></extra>'
    ))
    
    # Reorder points
    reorder_points = site_df[site_df["reorder_flag"] == True]
    fig.add_trace(go.Scatter(
        x=reorder_points["date"], 
        y=reorder_points["sim_inventory"],
        mode="markers", 
        name="Reorder Trigger",
        marker=dict(
            color="#dc3545", 
            size=10, 
            symbol="diamond",
            line=dict(color="white", width=1.5)
        ),
        hovertemplate='<b>%{x|%Y-%m-%d}</b><br>Reorder Trigger<br>Inventory: %{y:,.0f} t<extra></extra>'
    ))
    
    fig.update_layout(
        template="plotly_white",
        title=dict(
            text=f"<b>{site_id}</b> - Inventory and Demand Forecast",
            font=dict(size=16, color="#1a2a3a"),
            x=0.5,
            xanchor="center"
        ),
       xaxis=dict(
        title=dict(
            text="Date",
            font=dict(color="#5a6a7a", size=12)
        ),
        gridcolor="rgba(21, 99, 116, 0.06)",
        tickfont=dict(color="#5a6a7a"),
        zeroline=False
    ),
    yaxis=dict(
        title=dict(
            text="Inventory (t)",
            font=dict(color="#5a6a7a", size=12)
        ),
        gridcolor="rgba(21, 99, 116, 0.06)",
        tickfont=dict(color="#5a6a7a"),
        zeroline=False
    ),
    yaxis2=dict(
        title=dict(
            text="Demand (t)",
            font=dict(color="#5a6a7a", size=12)
        ),
        overlaying="y",
        side="right",
        gridcolor="rgba(21, 99, 116, 0.06)",
        tickfont=dict(color="#5a6a7a"),
        zeroline=False
    ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color="#2a3a4a", size=11),
            bgcolor="rgba(255,255,255,0.8)",
            bordercolor="rgba(21, 99, 116, 0.1)",
            borderwidth=1
        ),
        hovermode="x unified",
        plot_bgcolor="rgba(255,255,255,0.3)",
        paper_bgcolor="rgba(255,255,255,0)",
        margin=dict(l=60, r=60, t=80, b=50),
        height=450,
        font=dict(color="#2a3a4a")
    )
    
    # Reorder Table Data
    reorder_data = site_df[site_df["reorder_flag"] == True][[
        "date", "sim_inventory", "recommended_delivery_date",
        "recommended_delivery_quantity", "buffer_applied"
    ]].copy()
    reorder_data['date'] = reorder_data['date'].dt.strftime('%Y-%m-%d')
    
    return (
        fig,
        reorder_data.to_dict("records"),
        model_comparison,
        comparison_note,
        kpi_cards
    )

# =======================
# Run the app
# =======================
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8050)