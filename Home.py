import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

# Set page config
st.set_page_config(
    page_title="Oil Palm Plantation Dashboard",
    page_icon="🌴",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load data
@st.cache_data
def load_data():
    # Read the Excel file
    df = pd.read_excel("intern data.xlsx", sheet_name="Sheet1")
    
    # Clean column names (remove extra spaces)
    df.columns = df.columns.str.strip()
    
    # Convert date column to datetime
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Extract year and month for easier filtering
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month_name()
    
    # Clean up YearPlanted column
    df['YearPlanted'] = df['YearPlanted'].astype(str)
    
    return df

df = load_data()

# Sidebar filters
st.sidebar.markdown(
    """
    <div style="
        background: linear-gradient(135deg, #1e5f2c, #3cb371);
        padding: 16px;
        border-radius: 10px;
        margin-bottom: 25px;
        text-align: center;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.2);
    ">
        <div style="
            display: flex; 
            justify-content: center; 
            align-items: center; 
            gap: 12px;
            filter: drop-shadow(0 2px 2px rgba(0,0,0,0.2));
        ">
            <span style="font-size: 2em; color: #f8f8f8">🌴</span>
            <div>
                <h2 style="
                    color: white;
                    margin: 0;
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    letter-spacing: 1px;
                    font-weight: 600;
                    text-shadow: 0 1px 3px rgba(0,0,0,0.3);
                    line-height: 1.2;
                ">
                    LADANG MELINTANG MAJU
                </h2>
                <p style="
                    color: rgba(255,255,255,0.9);
                    margin: 4px 0 0;
                    font-size: 0.8em;
                    font-weight: 300;
                ">
                    Plantation Analytics
                </p>
            </div>
            <span style="font-size: 2em; color: #f8f8f8">🌴</span>
        </div>
        <div style="
            margin-top: 12px;
            height: 2px;
            background: linear-gradient(to right, transparent, rgba(255,255,255,0.5), transparent);
        "></div>
    </div>
    """,
    unsafe_allow_html=True
)

# Sidebar filters
st.sidebar.header("Filter Data")

# Initialize all filter variables first
fields = df['Field'].unique()
years = df['Year'].unique()
months = df['Month'].unique()
fertilizer_types = df['TypeOfFetilizer'].unique()

# Field selection with individual reset
col1_field, col2_field = st.sidebar.columns([4, 1])
with col1_field:
    selected_fields = st.multiselect(
        "Select Fields",
        options=fields,
        default=fields[:2]
    )

# Year selection with individual reset
col1_year, col2_year = st.sidebar.columns([4, 1])
with col1_year:
    selected_years = st.multiselect(
        "Select Years",
        options=years,
        default=years
    )

# Month selection with individual reset
col1_month, col2_month = st.sidebar.columns([4, 1])
with col1_month:
    selected_months = st.multiselect(
        "Select Months",
        options=months,
        default=months
    )

# Fertilizer Type Filter with individual reset
col1_fert, col2_fert = st.sidebar.columns([4, 1])
with col1_fert:
    selected_fertilizer = st.multiselect(
        "Type of Fertilizer",
        options=fertilizer_types,
        default=fertilizer_types,
        help="Filter by fertilizer type"
    )

# Filter data based on selections
filtered_df = df[
    (df['Field'].isin(selected_fields)) &
    (df['Year'].isin(selected_years)) &
    (df['Month'].isin(selected_months)) &
    (df['TypeOfFetilizer'].isin(selected_fertilizer))
]

# Main dashboard
st.title("🌴 Oil Palm Plantation Performance Dashboard")
st.markdown("### Interactive analysis of plantation mt and productivity")

# Function to display no data message
def show_no_data_message():
    st.warning("⚠️ No data available for the selected filters. Please adjust your filter criteria.")
    st.info("ℹ️ Try selecting different fields, years, or months to view data.")

# Check if filtered data is empty
if filtered_df.empty:
    show_no_data_message()
else:
# KPI cards with equal sizing
 col1, col2, col3, col4 = st.columns(4)
 with col1:
    field_count = filtered_df['Field'].nunique()
    st.metric(
        label="🌿 Total Fields", 
        value=f"{field_count:,}",
        delta="",  # Empty delta to maintain same height
        help="Number of unique plantation fields"
    )
with col2:
    total_yield = round(filtered_df['MT'].sum())
    yield_per_field = round(total_yield/max(1, field_count)) if field_count > 0 else 0
    st.metric(
        label="📈 Total Yield", 
        value=f"{total_yield:,} MT",
        delta=f"~{yield_per_field:,} MT/field" if field_count > 0 else "",
        help="Total production"
    )
with col3:
    total_bunches = int(filtered_df['Bunches'].sum())
    bunches_per_field = round(total_bunches/max(1, field_count)) if field_count > 0 else 0
    st.metric(
        label="🌴 Total Bunches", 
        value=f"{total_bunches:,}",
        delta=f"~{bunches_per_field:,}/field" if field_count > 0 else "",
        help="Total bunches"
    )
with col4:
    total_fert = round(filtered_df['Usage of fertilizer'].sum())
    fert_per_field = round(total_fert/max(1, field_count)) if field_count > 0 else 0
    st.metric(
        label="🧴 Total Fertilizer", 
        value=f"{total_fert:,} bags",
        delta=f"~{fert_per_field:,} bags/field" if field_count > 0 else "",
        help="Total fertilizer"
    )

# CSS for equal card sizes
st.markdown("""
<style>
    div[data-testid="stMetric"] {
        background-color: rgba(46, 139, 87, 0.1);
        border-radius: 8px;
        padding: 20px 10px;
        min-height: 135px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    div[data-testid="stMetric"] > div:first-child {
        justify-content: center;
    }
    div[data-testid="stMetric"] label {
        font-size: 0.95rem !important;
        font-weight: 600 !important;
        color: #2e8b57 !important;
        margin-bottom: 8px !important;
    }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        font-size: 1.5rem !important;
        margin-top: 0 !important;
        margin-bottom: 4px !important;
    }
    div[data-testid="stMetric"] div[data-testid="stMetricDelta"] {
        min-height: 24px;
    }
</style>
""", unsafe_allow_html=True)

# Add to your existing tabs definition
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Yield Analysis", "Fertilizer Impact", "WeedControl Analysis", "Pest&Disease", "Raw Data", "Yield Forecast"])

with tab1:
    st.header("🌴 Yield Analysis Dashboard")
    
    # Overview Tabs
    overview_tab1, overview_tab2 = st.tabs(["📈 Monthly Yield (MT)", "🍌 Monthly Bunches Count"])
    
    with overview_tab1:
        # Yield (MT) chart
        monthly_total = filtered_df.groupby(pd.Grouper(key='Date', freq='MS'))['MT'].sum().reset_index()
        
        fig_total = px.line(
            monthly_total,
            x='Date',
            y='MT',
            title='<b>Monthly Fresh Fruit Bunch Yield (MT)</b>',
            labels={'MT': 'Yield (MT)'},
            markers=True,
            line_shape='spline',
            color_discrete_sequence=['#1f77b4']
        ).update_layout(
            hovermode="x unified",
            plot_bgcolor='rgba(0,0,0,0)',
            height=450,
            xaxis_title="Month",
            yaxis_title="Yield (Metric Tons)"
        )
        
        avg_yield = monthly_total['MT'].mean()
        fig_total.add_hline(
            y=avg_yield,
            line_dash="dot",
            annotation_text=f'Average: {avg_yield:,.1f} MT',
            annotation_position="bottom right",
            line_color="orange"
        )
        
        st.plotly_chart(fig_total, use_container_width=True)

    with overview_tab2:
        # Bunches chart
        monthly_bunches = filtered_df.groupby(pd.Grouper(key='Date', freq='MS'))['Bunches'].sum().reset_index()
        
        fig_bunches = px.line(
            monthly_bunches,
            x='Date',
            y='Bunches',
            title='<b>Monthly Fresh Fruit Bunches Count</b>',
            labels={'Bunches': 'Bunches Count'},
            markers=True,
            line_shape='spline',
            color_discrete_sequence=['#ff7f0e']
        ).update_layout(
            hovermode="x unified",
            plot_bgcolor='rgba(0,0,0,0)',
            height=450,
            xaxis_title="Month",
            yaxis_title="Number of Bunches"
        )
        
        avg_bunches = monthly_bunches['Bunches'].mean()
        fig_bunches.add_hline(
            y=avg_bunches,
            line_dash="dot",
            annotation_text=f'Average: {avg_bunches:,.0f}',
            annotation_position="bottom right",
            line_color="green"
        )
        
        st.plotly_chart(fig_bunches, use_container_width=True)
    
    # Performance Summary Section
    st.subheader("📊 Performance Summary Statistics")
    
    # Calculate key metrics
    max_mt = monthly_total['MT'].max()
    min_mt = monthly_total['MT'].min()
    avg_mt = monthly_total['MT'].mean()
    growth = (monthly_total['MT'].iloc[-1] - monthly_total['MT'].iloc[0]) / monthly_total['MT'].iloc[0] * 100 \
            if monthly_total['MT'].iloc[0] != 0 else 0

    max_bunches = monthly_bunches['Bunches'].max()
    min_bunches = monthly_bunches['Bunches'].min()
    avg_bunches = monthly_bunches['Bunches'].mean()
    growth_bunches = (monthly_bunches['Bunches'].iloc[-1] - monthly_bunches['Bunches'].iloc[0]) / monthly_bunches['Bunches'].iloc[0] * 100 \
            if monthly_bunches['Bunches'].iloc[0] != 0 else 0

    # Metrics Cards
    st.markdown("##### 🏆 Yield (MT) Performance")
    col_mt1, col_mt2, col_mt3, col_mt4 = st.columns(4)
    with col_mt1:
        st.metric("Peak Yield", f"{max_mt:,.1f} MT", 
                 help="Highest monthly yield achieved")
    with col_mt2:
        st.metric("Lowest Yield", f"{min_mt:,.1f} MT", 
                 help="Lowest monthly yield recorded")
    with col_mt3:
        st.metric("Average Yield", f"{avg_mt:,.1f} MT", 
                 help="Mean monthly production")
    with col_mt4:
        st.metric("Growth Trend", f"{growth:.1f}%", 
                 delta_color="inverse" if growth < 0 else "normal",
                 help="Percentage change from first to last month")

    st.markdown("##### 🍌 Bunches Performance")
    col_bun1, col_bun2, col_bun3, col_bun4 = st.columns(4)
    with col_bun1:
        st.metric("Peak Bunches", f"{max_bunches:,.0f}", 
                 help="Highest monthly count")
    with col_bun2:
        st.metric("Lowest Bunches", f"{min_bunches:,.0f}", 
                 help="Lowest monthly count")
    with col_bun3:
        st.metric("Average Bunches", f"{avg_bunches:,.0f}", 
                 help="Mean monthly count")
    with col_bun4:
        st.metric("Growth Trend", f"{growth_bunches:.1f}%",
                 delta_color="inverse" if growth_bunches < 0 else "normal",
                 help="Percentage change in bunches")

    # Field Comparison Section
    st.subheader("🌿 Field Performance Comparison")
    field_tab1, field_tab2 = st.tabs(["Yield by Field", "Bunches by Field"])
    
    with field_tab1:
        fig_fields_mt = px.line(
            filtered_df,
            x='Date',
            y='MT',
            color='Field',
            title='<b>Monthly Yield (MT) by Field</b>',
            labels={'MT': 'Yield (MT)'},
            markers=True,
            line_shape='spline'
        ).update_layout(
            height=500, 
            hovermode="x unified",
            plot_bgcolor='rgba(0,0,0,0)',
            legend_title="Field Code"
        )
        st.plotly_chart(fig_fields_mt, use_container_width=True)
    
    with field_tab2:
        fig_fields_bunches = px.line(
            filtered_df,
            x='Date',
            y='Bunches',
            color='Field',
            title='<b>Monthly Bunches Count by Field</b>',
            labels={'Bunches': 'Bunches Count'},
            markers=True,
            line_shape='spline'
        ).update_layout(
            height=500, 
            hovermode="x unified",
            plot_bgcolor='rgba(0,0,0,0)',
            legend_title="Field Code"
        )
        st.plotly_chart(fig_fields_bunches, use_container_width=True)
        
    # Efficiency Analysis Section
    st.subheader("⚡ Production Efficiency Metrics")
    
    # Calculate efficiency metrics
    efficiency_df = filtered_df.copy()
    efficiency_df['Bunches_per_MT'] = efficiency_df['Bunches'] / efficiency_df['MT']
    efficiency_df['KG_per_Bunch'] = (efficiency_df['MT'] * 1000) / efficiency_df['Bunches']
    
    monthly_efficiency = efficiency_df.groupby(pd.Grouper(key='Date', freq='MS')).agg({
        'Bunches_per_MT': 'mean',
        'KG_per_Bunch': 'mean'
    }).reset_index()

    # Efficiency Tabs
    eff_tab1, eff_tab2 = st.tabs(["Bunches per MT Analysis", "KG per Bunch Analysis"])

    with eff_tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            fig_bunches_mt = px.line(
                monthly_efficiency,
                x='Date',
                y='Bunches_per_MT',
                title='<b>Bunches Required per Metric Ton</b>',
                labels={'Bunches_per_MT': 'Bunches/MT'},
                markers=True,
                line_shape='spline',
                color_discrete_sequence=['#2ca02c']
            ).update_layout(
                hovermode="x unified",
                plot_bgcolor='rgba(0,0,0,0)',
                height=400,
                yaxis_title="Bunches per MT"
            )
            
            avg_bunches_mt = monthly_efficiency['Bunches_per_MT'].mean()
            fig_bunches_mt.add_hline(
                y=avg_bunches_mt,
                line_dash="dot",
                annotation_text=f'Average: {avg_bunches_mt:,.1f}',
                annotation_position="bottom right",
                line_color="orange"
            )
            st.plotly_chart(fig_bunches_mt, use_container_width=True)
        
        with col2:
        # Field comparison for KG/Bunch
            field_kg_bunch = efficiency_df.groupby('Field')['Bunches_per_MT'].mean().reset_index().sort_values('Bunches_per_MT')
            fig_field_kg = px.bar(
                field_kg_bunch,
                x='Field',
                y='Bunches_per_MT',
             title='<b>Average Bunches_per_MT by Field</b>',
                labels={'Bunches_per_MT': 'Weight (Bunches_per_MT)'},
                color='Bunches_per_MT',
                color_continuous_scale='Reds'
            )
        
            fig_field_kg.update_layout(height=400)
            st.plotly_chart(fig_field_kg, use_container_width=True)
            
        # Field trend analysis
        st.markdown("##### 📅 Field Efficiency Trends Over Time")
        fig_field_trend = px.line(
            efficiency_df,
            x='Date',
            y='Bunches_per_MT',
            color='Field',
            title='<b>Bunches/MT Efficiency by Field Over Time</b>',
            markers=True,
            line_shape='spline'
        ).update_layout(
            height=500,
            hovermode="x unified",
            plot_bgcolor='rgba(0,0,0,0)',
            yaxis_title="Bunches per MT",
            legend_title="Field Code"
        )
        st.plotly_chart(fig_field_trend, use_container_width=True)

    with eff_tab2:
        col1, col2 = st.columns(2)
        
        with col1:
            fig_kg_bunch = px.line(
                monthly_efficiency,
                x='Date',
                y='KG_per_Bunch',
                title='<b>Average Bunch Weight (kg)</b>',
                labels={'KG_per_Bunch': 'Weight (kg)'},
                markers=True,
                line_shape='spline',
                color_discrete_sequence=['#d62728']
            ).update_layout(
                hovermode="x unified",
                plot_bgcolor='rgba(0,0,0,0)',
                height=400,
                yaxis_title="Kilograms per Bunch"
            )
            
            avg_kg_bunch = monthly_efficiency['KG_per_Bunch'].mean()
            fig_kg_bunch.add_hline(
                y=avg_kg_bunch,
                line_dash="dot",
                annotation_text=f'Average: {avg_kg_bunch:,.1f} kg',
                annotation_position="bottom right",
                line_color="green"
            )
            st.plotly_chart(fig_kg_bunch, use_container_width=True)
        
        with col2:
        # Field comparison for KG/Bunch
            field_kg_bunch = efficiency_df.groupby('Field')['KG_per_Bunch'].mean().reset_index().sort_values('KG_per_Bunch')
            fig_field_kg = px.bar(
                field_kg_bunch,
                x='Field',
                y='KG_per_Bunch',
             title='<b>Average KG/Bunch by Field</b>',
                labels={'KG_per_Bunch': 'Weight (kg/bunch)'},
                color='KG_per_Bunch',
                color_continuous_scale='Reds'
            )
        
            fig_field_kg.update_layout(height=400)
            st.plotly_chart(fig_field_kg, use_container_width=True)
            
        # Field trend analysis
        st.markdown("##### 📅 Bunch Weight Trends Over Time")
        fig_weight_trend = px.line(
            efficiency_df,
            x='Date',
            y='KG_per_Bunch',
            color='Field',
            title='<b>Bunch Weight by Field Over Time</b>',
            markers=True,
            line_shape='spline'
        ).update_layout(
            height=500,
            hovermode="x unified",
            plot_bgcolor='rgba(0,0,0,0)',
            yaxis_title="Kilograms per Bunch",
            legend_title="Field Code"
        )
        st.plotly_chart(fig_weight_trend, use_container_width=True)

    # Efficiency Metrics Cards
    st.subheader("🏆 Efficiency Performance Indicators")
    
    # Calculate additional metrics
    min_bunches_mt = monthly_efficiency['Bunches_per_MT'].min()
    max_bunches_mt = monthly_efficiency['Bunches_per_MT'].max()
    min_kg_bunch = monthly_efficiency['KG_per_Bunch'].min()
    max_kg_bunch = monthly_efficiency['KG_per_Bunch'].max()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Avg Bunches/MT", 
            f"{avg_bunches_mt:,.1f}",
            help="Average number of bunches needed to produce 1 metric ton",
            delta=f"Range: {min_bunches_mt:,.1f}-{max_bunches_mt:,.1f}"
        )
    
    with col2:
        st.metric(
            "Avg Bunch Weight",
            f"{avg_kg_bunch:,.1f} kg",
            help="Average weight of each fruit bunch",
            delta=f"Range: {min_kg_bunch:,.1f}-{max_kg_bunch:,.1f} kg"
        )
    
    with col3:
        best_month_bunches = monthly_efficiency.loc[monthly_efficiency['Bunches_per_MT'].idxmax(), 'Date'].strftime('%b %Y')
        st.metric(
            "Most Efficient Month",
            best_month_bunches,
            help=f"Month with lowest bunches/MT ratio: {min_bunches_mt:,.1f}",
            delta_color="off"
        )
    
    with col4:
        best_month_weight = monthly_efficiency.loc[monthly_efficiency['KG_per_Bunch'].idxmax(), 'Date'].strftime('%b %Y')
        st.metric(
            "Heaviest Bunches Month",
            best_month_weight,
            help=f"Month with highest average bunch weight: {max_kg_bunch:,.1f} kg",
            delta_color="off"
        )

with tab2:
    # ---- Header with description ----
    st.header("🌱 Fertilizer Impact Analysis")
    st.markdown("""
    <style>
        .header-style { font-size:18px; color:#2e6e7c; }
        .divider { border-top: 2px solid #f0f2f6; margin: 1rem 0; }
    </style>
    <p class="header-style">Comprehensive analysis of fertilizer types by usage, labor, and coverage metrics</p>
    <div class="divider"></div>
    """, unsafe_allow_html=True)
    
    # ---- Main KPI Chart ----
    st.subheader("Production Impact")
    grouped_df = filtered_df.groupby('TypeOfFetilizer').agg({'MT': 'sum', 'Bunches': 'sum'}).reset_index()
    
    fig4 = px.bar(
        grouped_df,
        x='TypeOfFetilizer',
        y='MT',
        color='TypeOfFetilizer',
        title='<b>Total Production by Fertilizer Type</b>',
        template='plotly_white',
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    
    fig4.add_trace(
        px.line(
            grouped_df, 
            x='TypeOfFetilizer', 
            y='Bunches',
            text='Bunches'
        ).update_traces(
            line=dict(color='#2e6e7c', width=3),
            texttemplate='%{y:,.0f}',
            textposition='top center',
            name='Bunches',
            yaxis='y2',
            showlegend=False
        ).data[0]
    )
    
    fig4.update_layout(
        yaxis=dict(title='<b>Metric Tons (MT)</b>', gridcolor='#f0f2f6'),
        yaxis2=dict(title='<b>Bunches Count</b>', overlaying='y', side='right', gridcolor='#f0f2f6'),
        xaxis=dict(title='<b>Fertilizer Type</b>'),
        hovermode='x unified',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False  # Disabled legend
    )
    
    st.plotly_chart(fig4, use_container_width=True)
    
    # ---- Usage Metrics ----
    st.subheader("Usage Patterns")
    col1, col2 = st.columns(2)
    
    with col1:
        fig5 = px.pie(
            filtered_df[filtered_df['Usage of fertilizer'] > 0],
            names='TypeOfFetilizer',
            values='Usage of fertilizer',
            title='<b>Fertilizer Usage Distribution</b>',
            hole=0.4,
            color='TypeOfFetilizer',
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig5.update_traces(textposition='inside', textinfo='percent+label', showlegend=False)
        st.plotly_chart(fig5, use_container_width=True)
    
    with col2:
        fig6 = px.bar(
            filtered_df[filtered_df['No.OfRound Fertilizer'] > 0].groupby('TypeOfFetilizer')['No.OfRound Fertilizer'].sum().reset_index(),
            x='TypeOfFetilizer',
            y='No.OfRound Fertilizer',
            color='TypeOfFetilizer',
            title='<b>Total Application Rounds</b>',
            text_auto=True,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig6.update_layout(
            xaxis_title='',
            yaxis_title='<b>Number of Rounds</b>',
            showlegend=False  # Disabled legend
        )
        st.plotly_chart(fig6, use_container_width=True)
    
    # ---- Tabs for Detailed Analysis ----
    tab2_1, tab2_2, tab2_3 = st.tabs(["📍 Area Coverage", "👷 Labor Analysis", "🌴 Palm Coverage"])
    
    with tab2_1:
        st.subheader("Area Coverage Metrics")
        col1, col2 = st.columns(2)
        
        with col1:
            fig7 = px.bar(
                filtered_df[filtered_df['Fertilized Acres'] > 0].groupby('TypeOfFetilizer')['Fertilized Acres'].mean().reset_index(),
                x='TypeOfFetilizer',
                y='Fertilized Acres',
                color='TypeOfFetilizer',
                title='<b>Average Acres per Application</b>',
                text_auto='.2f',
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig7.update_layout(showlegend=False)  # Disabled legend
            st.plotly_chart(fig7, use_container_width=True)
        
        with col2:
            fig8 = px.bar(
                filtered_df[filtered_df['Fertilized Lorong'] > 0].groupby('TypeOfFetilizer')['Fertilized Lorong'].mean().reset_index(),
                x='TypeOfFetilizer',
                y='Fertilized Lorong',
                color='TypeOfFetilizer',
                title='<b>Average Lorong per Application</b>',
                text_auto='.2f',
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig8.update_layout(showlegend=False)  # Disabled legend
            st.plotly_chart(fig8, use_container_width=True)
    
    with tab2_2:
        st.subheader("Labor Utilization for Fertilizer")
    
        # Calculate statistics
        labor_stats = filtered_df.groupby('TypeOfFetilizer').agg({
            'Number of worker for fertilizer': ['sum', 'mean'],
            'Mandays for fertilizer': ['sum', 'mean']
        }).reset_index()
    
        # Flatten multi-index columns
        labor_stats.columns = ['TypeOfFetilizer', 
                         'Total Workers', 'Avg Workers',
                         'Total Mandays', 'Avg Mandays']
    
        # Create the visualization with both total and average metrics
        fig7 = px.bar(
            labor_stats,
            x='TypeOfFetilizer',
            y=['Total Workers', 'Total Mandays'],
            title='<b>Labor Utilization by Weed Control Type</b>',
            barmode='group',
            color_discrete_sequence=['#636EFA', '#EF553B'],
            labels={'value': 'Count/Days', 'variable': 'Metric'}
        )
    
        # Add average lines
        fig7.add_trace(
            px.line(
                labor_stats, 
                x='TypeOfFetilizer', 
                y='Avg Workers',
                text='Avg Workers'
            ).update_traces(
                line=dict(color='#636EFA', width=3, dash='dot'),
                texttemplate='%{y:.1f}',
                textposition='top center',
                name='Avg Workers',
                yaxis='y2',
                showlegend=True
            ).data[0]
        )
    
        fig7.add_trace(
            px.line(
                labor_stats, 
                x='TypeOfFetilizer', 
                y='Avg Mandays',
                text='Avg Mandays'
            ).update_traces(
                line=dict(color='#EF553B', width=3, dash='dot'),
                texttemplate='%{y:.1f}',
                textposition='top center',
                name='Avg Mandays',
                yaxis='y2',
                showlegend=True
            ).data[0]
        )
    
        fig7.update_layout(
            yaxis=dict(title='<b>Total Count/Days</b>', gridcolor='#f0f2f6'),
            yaxis2=dict(title='<b>Average per Application</b>', overlaying='y', side='right', gridcolor='#f0f2f6'),
            xaxis=dict(title='<b>Weed Control Type</b>'),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            hovermode='x unified'
        )
    
        st.plotly_chart(fig7, use_container_width=True)
    
        # Display the data table
        st.markdown("**Detailed Labor Statistics by Weed Control Type**")
        st.dataframe(
            labor_stats.style
                .format({'Avg Workers': '{:.1f}', 'Avg Mandays': '{:.1f}'})
                .set_properties(**{'text-align': 'center'})
                .highlight_max(color='lightgreen', subset=['Total Workers', 'Total Mandays'])
                .highlight_min(color='#ffcccb', subset=['Total Workers', 'Total Mandays']),
            use_container_width=True
        )
    
    with tab2_3:
        st.subheader("Palm Coverage Analysis")
        col1, col2 = st.columns(2)
        
        with col1:
            fig11 = px.bar(
                filtered_df[filtered_df['Fertilized Standing Palms'] > 0].groupby('TypeOfFetilizer')['Fertilized Standing Palms'].mean().reset_index(),
                x='TypeOfFetilizer',
                y='Fertilized Standing Palms',
                color='TypeOfFetilizer',
                title='<b>Average Palms per Application</b>',
                text_auto='.0f',
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig11.update_layout(showlegend=False)  # Disabled legend
            st.plotly_chart(fig11, use_container_width=True)
        
        with col2:
            fig12 = px.bar(
                filtered_df[filtered_df['Fertilized Standing Palms'] > 0].groupby('TypeOfFetilizer')['Fertilized Standing Palms'].sum().reset_index(),
                x='TypeOfFetilizer',
                y='Fertilized Standing Palms',
                color='TypeOfFetilizer',
                title='<b>Total Palms Fertilized</b>',
                text_auto='.0f',
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig12.update_layout(showlegend=False)  # Disabled legend
            st.plotly_chart(fig12, use_container_width=True)

with tab3:
    st.header("WeedControl Analysis")
    st.markdown("""
    <style>
        .header-style { font-size:18px; color:#2e6e7c; }
        .divider { border-top: 2px solid #f0f2f6; margin: 1rem 0; }
    </style>
    <p class="header-style">Comprehensive analysis of WeedControl types by frequency, labor impact, and production effects
    <div class="divider"></div>
    """, unsafe_allow_html=True)
    
    # ---- Main KPI Chart ----
    st.subheader("Production Impact")
    grouped_df = filtered_df.groupby('TypeOfWeedControl').agg({'MT': 'sum', 'Bunches': 'sum'}).reset_index()
    
    fig4 = px.bar(
        grouped_df,
        x='TypeOfWeedControl',
        y='MT',
        color='TypeOfWeedControl',
        title='<b>Total Production by WeedControl Type</b>',
        template='plotly_white',
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    
    fig4.add_trace(
        px.line(
            grouped_df, 
            x='TypeOfWeedControl', 
            y='Bunches',
            text='Bunches'
        ).update_traces(
            line=dict(color='#2e6e7c', width=3),
            texttemplate='%{y:,.0f}',
            textposition='top center',
            name='Bunches',
            yaxis='y2',
            showlegend=False
        ).data[0]
    )
    
    fig4.update_layout(
        yaxis=dict(title='<b>Metric Tons (MT)</b>', gridcolor='#f0f2f6'),
        yaxis2=dict(title='<b>Bunches Count</b>', overlaying='y', side='right', gridcolor='#f0f2f6'),
        xaxis=dict(title='<b>WeedControl Type</b>'),
        hovermode='x unified',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False  # Disabled legend
    )
    
    st.plotly_chart(fig4, use_container_width=True)
        # ---- Weed Control Type Distribution ----
    st.subheader("Weed Control Type Distribution")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Count of each weed control type
        weed_counts = filtered_df['TypeOfWeedControl'].value_counts().reset_index()
        weed_counts.columns = ['TypeOfWeedControl', 'Count']
        
        fig5 = px.pie(
            weed_counts,
            names='TypeOfWeedControl',
            values='Count',
            title='<b>Weed Control Type Distribution</b>',
            color_discrete_sequence=px.colors.qualitative.Pastel,
            hole=0.4
        )
        fig5.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig5, use_container_width=True)
    
    with col2:
        # Max number of rounds for each weed control type
        max_rounds = filtered_df.groupby('TypeOfWeedControl')['No.OfRound WeedControl'].max().reset_index()
        
        fig6 = px.bar(
            max_rounds,
            x='TypeOfWeedControl',
            y='No.OfRound WeedControl',
            color='TypeOfWeedControl',
            title='<b>Maximum Rounds by Weed Control Type</b>',
            text='No.OfRound WeedControl',
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig6.update_traces(texttemplate='%{y}', textposition='outside')
        fig6.update_layout(
            yaxis=dict(title='<b>Maximum Rounds</b>', gridcolor='#f0f2f6'),
            xaxis=dict(title='<b>Weed Control Type</b>'),
            showlegend=False
        )
        st.plotly_chart(fig6, use_container_width=True)

        # ---- Labor Analysis ----
    st.subheader("Labor Utilization for Weed Control")
    
    # Calculate statistics
    labor_stats = filtered_df.groupby('TypeOfWeedControl').agg({
        'Number of workers for weed control': ['sum', 'mean'],
        'Mandays for weed control': ['sum', 'mean']
    }).reset_index()
    
    # Flatten multi-index columns
    labor_stats.columns = ['TypeOfWeedControl', 
                         'Total Workers', 'Avg Workers',
                         'Total Mandays', 'Avg Mandays']
    
    # Create the visualization with both total and average metrics
    fig7 = px.bar(
        labor_stats,
        x='TypeOfWeedControl',
        y=['Total Workers', 'Total Mandays'],
        title='<b>Labor Utilization by Weed Control Type</b>',
        barmode='group',
        color_discrete_sequence=['#636EFA', '#EF553B'],
        labels={'value': 'Count/Days', 'variable': 'Metric'}
    )
    
    # Add average lines
    fig7.add_trace(
        px.line(
            labor_stats, 
            x='TypeOfWeedControl', 
            y='Avg Workers',
            text='Avg Workers'
        ).update_traces(
            line=dict(color='#636EFA', width=3, dash='dot'),
            texttemplate='%{y:.1f}',
            textposition='top center',
            name='Avg Workers',
            yaxis='y2',
            showlegend=True
        ).data[0]
    )
    
    fig7.add_trace(
        px.line(
            labor_stats, 
            x='TypeOfWeedControl', 
            y='Avg Mandays',
            text='Avg Mandays'
        ).update_traces(
            line=dict(color='#EF553B', width=3, dash='dot'),
            texttemplate='%{y:.1f}',
            textposition='top center',
            name='Avg Mandays',
            yaxis='y2',
            showlegend=True
        ).data[0]
    )
    
    fig7.update_layout(
        yaxis=dict(title='<b>Total Count/Days</b>', gridcolor='#f0f2f6'),
        yaxis2=dict(title='<b>Average per Application</b>', overlaying='y', side='right', gridcolor='#f0f2f6'),
        xaxis=dict(title='<b>Weed Control Type</b>'),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        hovermode='x unified'
    )
    
    st.plotly_chart(fig7, use_container_width=True)
    
    # Display the data table
    st.markdown("**Detailed Labor Statistics by Weed Control Type**")
    st.dataframe(
        labor_stats.style
            .format({'Avg Workers': '{:.1f}', 'Avg Mandays': '{:.1f}'})
            .set_properties(**{'text-align': 'center'})
            .highlight_max(color='lightgreen', subset=['Total Workers', 'Total Mandays'])
            .highlight_min(color='#ffcccb', subset=['Total Workers', 'Total Mandays']),
        use_container_width=True
    )
    
with tab4:
    st.header("Pest&Disease Analysis")
    st.markdown("""
    <style>
        .header-style { font-size:18px; color:#2e6e7c; }
        .divider { border-top: 2px solid #f0f2f6; margin: 1rem 0; }
    </style>
    <p class="header-style">Comprehensive analysis of Pest&Disease types by frequency, labor impact, and production effects
    <div class="divider"></div>
    """, unsafe_allow_html=True)
    
    # ---- Main KPI Chart ----
    st.subheader("Production Impact")
    grouped_df = filtered_df.groupby('Type of pest and disease').agg({'MT': 'sum', 'Bunches': 'sum'}).reset_index()
    
    fig4 = px.bar(
        grouped_df,
        x='Type of pest and disease',
        y='MT',
        color='Type of pest and disease',
        title='<b>Total Production by Pest&Disease Type</b>',
        template='plotly_white',
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    
    fig4.add_trace(
        px.line(
            grouped_df, 
            x='Type of pest and disease', 
            y='Bunches',
            text='Bunches'
        ).update_traces(
            line=dict(color='#2e6e7c', width=3),
            texttemplate='%{y:,.0f}',
            textposition='top center',
            name='Bunches',
            yaxis='y2',
            showlegend=False
        ).data[0]
    )
    
    fig4.update_layout(
        yaxis=dict(title='<b>Metric Tons (MT)</b>', gridcolor='#f0f2f6'),
        yaxis2=dict(title='<b>Bunches Count</b>', overlaying='y', side='right', gridcolor='#f0f2f6'),
        xaxis=dict(title='<b>Pest&Disease Type</b>'),
        hovermode='x unified',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False
    )
    
    st.plotly_chart(fig4, use_container_width=True)
    
    # ---- Pest&Disease Type Distribution ----
    st.subheader("Pest&Disease Type Distribution")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Count of each pest type
        pest_counts = filtered_df['Type of pest and disease'].value_counts().reset_index()
        pest_counts.columns = ['Type of pest and disease', 'Count']
        
        fig5 = px.pie(
            pest_counts,
            names='Type of pest and disease',
            values='Count',
            title='<b>Pest&Disease Type Distribution</b>',
            color_discrete_sequence=px.colors.qualitative.Pastel,
            hole=0.4
        )
        fig5.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig5, use_container_width=True)
    
    with col2:
        # Max number of rounds for each pest type
        max_rounds = filtered_df.groupby('Type of pest and disease')['No.OfRound P&D'].max().reset_index()
        
        fig6 = px.bar(
            max_rounds,
            x='Type of pest and disease',
            y='No.OfRound P&D',
            color='Type of pest and disease',
            title='<b>Maximum Rounds by Pest&Disease Type</b>',
            text='No.OfRound P&D',
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig6.update_traces(texttemplate='%{y}', textposition='outside')
        fig6.update_layout(
            yaxis=dict(title='<b>Maximum Rounds</b>', gridcolor='#f0f2f6'),
            xaxis=dict(title='<b>Pest&Disease Type</b>'),
            showlegend=False
        )
        st.plotly_chart(fig6, use_container_width=True)

    # ---- Labor Analysis ----
    st.subheader("Labor Utilization for Pest&Disease Control")
    
    # Calculate statistics
    labor_stats = filtered_df.groupby('Type of pest and disease').agg({
        'Number of workers for pest and disease': ['sum', 'mean'],
        'Mandays for pest and disease': ['sum', 'mean']
    }).reset_index()
    
    # Flatten multi-index columns
    labor_stats.columns = ['Type of pest and disease', 
                         'Total Workers', 'Avg Workers',
                         'Total Mandays', 'Avg Mandays']
    
    # Create the visualization with both total and average metrics
    fig7 = px.bar(
        labor_stats,
        x='Type of pest and disease',
        y=['Total Workers', 'Total Mandays'],
        title='<b>Labor Utilization by Pest&Disease Type</b>',
        barmode='group',
        color_discrete_sequence=['#636EFA', '#EF553B'],
        labels={'value': 'Count/Days', 'variable': 'Metric'}
    )
    
    # Add average lines
    fig7.add_trace(
        px.line(
            labor_stats, 
            x='Type of pest and disease', 
            y='Avg Workers',
            text='Avg Workers'
        ).update_traces(
            line=dict(color='#636EFA', width=3, dash='dot'),
            texttemplate='%{y:.1f}',
            textposition='top center',
            name='Avg Workers',
            yaxis='y2',
            showlegend=True
        ).data[0]
    )
    
    fig7.add_trace(
        px.line(
            labor_stats, 
            x='Type of pest and disease', 
            y='Avg Mandays',
            text='Avg Mandays'
        ).update_traces(
            line=dict(color='#EF553B', width=3, dash='dot'),
            texttemplate='%{y:.1f}',
            textposition='top center',
            name='Avg Mandays',
            yaxis='y2',
            showlegend=True
        ).data[0]
    )
    
    fig7.update_layout(
        yaxis=dict(title='<b>Total Count/Days</b>', gridcolor='#f0f2f6'),
        yaxis2=dict(title='<b>Average per Application</b>', overlaying='y', side='right', gridcolor='#f0f2f6'),
        xaxis=dict(title='<b>Pest&Disease Type</b>'),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        hovermode='x unified'
    )
    
    st.plotly_chart(fig7, use_container_width=True)
    
    # Display the data table
    st.markdown("**Detailed Labor Statistics by Pest&Disease Type**")
    st.dataframe(
        labor_stats.style
            .format({'Avg Workers': '{:.1f}', 'Avg Mandays': '{:.1f}'})
            .set_properties(**{'text-align': 'center'})
            .highlight_max(color='lightgreen', subset=['Total Workers', 'Total Mandays'])
            .highlight_min(color='#ffcccb', subset=['Total Workers', 'Total Mandays']),
        use_container_width=True
    )


with tab5:
    st.header("Raw Data View")
    st.dataframe(filtered_df, use_container_width=True)
    
    # Download button
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Filtered Data as CSV",
        data=csv,
        file_name='filtered_plantation_data.csv',
        mime='text/csv'
    )

with tab6:
    st.header("Yield Forecasting")
    
    if len(filtered_df) < 3:
        st.warning("Insufficient data for forecasting. Please select at least 3 months of historical data.")
    else:
        # Main slider
        forecast_period = st.select_slider(
            "Select forecast duration:",
            options=list(range(1, 61)),
            value=12,
            format_func=lambda x: (
                f"1 month" if x == 1 else
                f"{x} months" if x < 12 else
                f"1 year" if x == 12 else
                f"{x//12} years, {x%12} months" if x%12 != 0 else
                f"{x//12} years"
            ),
            help="Drag to select months (1-60) or click for precise entry"
        )
        
        # Prepare data - aggregate by month and ensure complete series
        forecast_df = filtered_df.groupby(pd.Grouper(key='Date', freq='MS'))['MT'].sum().reset_index()
        forecast_df = forecast_df.set_index('Date').asfreq('MS').fillna(method='ffill').reset_index()
        
        # Create time features for trend calculation
        forecast_df['month_num'] = forecast_df['Date'].dt.month
        forecast_df['time_index'] = np.arange(len(forecast_df))
        
        # Calculate seasonal components (12-month pattern)
        monthly_avg = forecast_df.groupby('month_num')['MT'].mean()
        seasonal_component = monthly_avg / monthly_avg.mean()
        
        # Calculate trend component (linear regression)
        X = forecast_df['time_index'].values.reshape(-1, 1)
        y = forecast_df['MT'].values
        trend_slope = np.polyfit(forecast_df['time_index'], forecast_df['MT'], 1)[0]
        
        # Generate future dates
        last_date = forecast_df['Date'].iloc[-1]
        future_dates = pd.date_range(
            start=last_date + pd.DateOffset(months=1),
            periods=forecast_period,
            freq='MS'
        )
        
        # Create future predictions with trend + seasonality
        future_df = pd.DataFrame({
            'Date': future_dates,
            'month_num': future_dates.month,
            'time_index': np.arange(len(forecast_df), len(forecast_df)+forecast_period)
        })
        
        # Apply trend and seasonality
        base_value = forecast_df['MT'].iloc[-1]
        future_df['MT'] = base_value + (future_df['time_index'] - len(forecast_df)) * trend_slope
        future_df['MT'] = future_df.apply(
            lambda row: row['MT'] * seasonal_component[row['month_num']], 
            axis=1
        )
        
        # Create plot
        fig = go.Figure()
        
        # Historical data
        fig.add_trace(go.Scatter(
            x=forecast_df['Date'],
            y=forecast_df['MT'],
            name='Historical Yield',
            line=dict(color='#2e8b57', width=3),
            mode='lines+markers'
        ))
        
        # Forecast data
        fig.add_trace(go.Scatter(
            x=future_df['Date'],
            y=future_df['MT'],
            name='Forecasted Yield',
            line=dict(color='#FFA500', width=3, dash='dot'),
            mode='lines+markers'
        ))
        
        # Style the plot
        fig.update_layout(
            title=f'Yield Forecast - Next {forecast_period} Months',
            xaxis_title='Date',
            yaxis_title='Yield (MT)',
            hovermode="x unified",
            plot_bgcolor='rgba(0,0,0,0)',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            shapes=[
                dict(
                    type='line',
                    x0=last_date,
                    x1=future_dates[0],
                    y0=forecast_df['MT'].iloc[-1],
                    y1=future_df['MT'].iloc[0],
                    line=dict(color='#FFA500', width=3, dash='dot')
                )
            ]
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Forecast summary
        st.subheader("Forecast Summary")
        
        total_growth = future_df['MT'].iloc[-1] - forecast_df['MT'].iloc[-1]
        avg_growth_pct = (total_growth / forecast_df['MT'].iloc[-1]) * 100 if forecast_df['MT'].iloc[-1] != 0 else 0
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric(
                "Projected Total Yield",
                f"{round(future_df['MT'].sum(), 1):,} MT",
                help=f"Total projected yield over next {forecast_period} months"
            )
            st.metric(
                "Projected Growth",
                f"{round(total_growth, 1):,} MT",
                f"{round(avg_growth_pct, 1)}%",
                help="Absolute and percentage growth projected"
            )
        
        with col2:
            st.metric(
                "Peak Forecast Month",
                f"{future_df.loc[future_df['MT'].idxmax(), 'Date'].strftime('%b %Y')}",
                f"{round(future_df['MT'].max(), 1):,} MT",
                help="Month with highest projected yield"
            )
            st.metric(
                "Last Historical Value",
                f"{round(forecast_df['MT'].iloc[-1], 1):,} MT",
                help="Most recent actual yield value"
            )

# Add some explanatory text
st.sidebar.markdown("""
### Dashboard Guide
- Use the filters to select specific fields, years, and months
- Explore different tabs for various analyses
- Hover over charts for detailed information
- Download filtered data from the Raw Data tab
""")