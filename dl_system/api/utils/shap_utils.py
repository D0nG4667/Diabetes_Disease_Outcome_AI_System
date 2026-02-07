import base64
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.io as pio

# Ensure kaleido is available (it should be if installed)
# pio.kaleido.scope.mathjax = None

def generate_shap_summary_plot_base64(shap_values, X, feature_names=None) -> str:
    """
    Generates a SHAP summary plot using Plotly (Strip Plot) and returns it as a base64 string.
    """
    try:
        # 1. Prepare Feature Names
        if feature_names is None:
            if hasattr(X, "columns"):
                feature_names = list(X.columns)
            else:
                feature_names = [f"Feature {i}" for i in range(X.shape[1] if hasattr(X, "shape") else len(X[0]))]
        
        # 2. Handle SHAP values input (ensure it's 1D for single instance or handle multiple)
        # ExplainerService passes shap_vals_target which is typically (n_features,) for single prediction
        vals = shap_values
        if isinstance(vals, list):
             # For multi-class, typically index 1 is positive class
             vals = vals[1] if len(vals) > 1 else vals[0]
        
        if hasattr(vals, "shape"):
             if len(vals.shape) == 2 and vals.shape[0] == 1:
                 vals = vals[0] # Flatten (1, features) -> (features,)
        
        # 3. Create DataFrame
        # If vals is 1D (n,), we treat it as 1 sample.
        
        df_plot = pd.DataFrame({
            "Feature": feature_names,
            "SHAP": vals
        })
        
        # Add coloring based on impact direction (Risk/Protective)
        df_plot["Type"] = ["Risk (Positive)" if v > 0 else "Protective (Negative)" for v in vals]
        
        # Sort features by absolute SHAP value (Importance)
        df_plot["AbsSHAP"] = df_plot["SHAP"].abs()
        df_plot = df_plot.sort_values("AbsSHAP", ascending=True) # Ascending for correct Y-axis order in Plotly
        
        # 4. Generate Plotly Strip Plot
        fig = px.strip(
            df_plot, 
            x='SHAP', 
            y='Feature', 
            color='Type', 
            stripmode='overlay', 
            color_discrete_map={
                "Risk (Positive)": "#ef4444", 
                "Protective (Negative)": "#10b981"
            },
            title="SHAP Value Distribution"
        )
        
        fig.update_layout(
            xaxis=dict(
                title="SHAP Value (Impact on Model Output)",
                showgrid=True, 
                gridcolor='WhiteSmoke', 
                zerolinecolor='Gainsboro'
            ),
            yaxis=dict(
                title="Feature",
                showgrid=True, 
                gridcolor='WhiteSmoke', 
                zerolinecolor='Gainsboro'
            ),
            plot_bgcolor='white',
            height=max(500, len(feature_names) * 40),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        fig.update_traces(jitter=1, marker=dict(size=12, opacity=0.9, line=dict(width=1, color='DarkSlateGrey')))

        # 5. Export to Base64 Image
        # Requires 'kaleido' package installed
        img_bytes = fig.to_image(format="png", engine="kaleido", scale=2)
        return base64.b64encode(img_bytes).decode("utf-8")
        
    except Exception as e:
        print(f"Error generating Plotly SHAP image: {e}")
        return None
