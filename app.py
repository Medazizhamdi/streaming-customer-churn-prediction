import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import joblib
import base64
import sys
from pathlib import Path

# Add src to system path to import feature engineering functions
ROOT = Path(__file__).resolve().parent
sys.path.append(str(ROOT / "src"))

try:
    from feature_engineering import add_behavioral_features, adapt_telco_to_streaming
except ImportError:
    # If not found directly, add src to PYTHONPATH in app
    sys.path.append(str(ROOT))
    from src.feature_engineering import add_behavioral_features, adapt_telco_to_streaming

# Page configuration
st.set_page_config(
    page_title="StreamRisk - Streaming Churn Analytics",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Netflix/Prime-style Dark Theme with Glassmorphism
custom_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #0F0F10;
        color: #FFFFFF;
        font-family: 'Outfit', sans-serif;
    }
    
    [data-testid="stHeader"] {
        background-color: rgba(15, 15, 16, 0.8) !important;
        backdrop-filter: blur(10px);
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #161618 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* Header brand */
    .brand-title {
        color: #E50914;
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0.1rem;
        letter-spacing: -0.5px;
    }
    .brand-subtitle {
        color: #8C8C9A;
        font-size: 0.9rem;
        margin-bottom: 2rem;
    }
    
    /* Glassmorphic KPI Cards */
    .kpi-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.03) 0%, rgba(255, 255, 255, 0.01) 100%);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 24px;
        text-align: center;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.2);
    }
    .kpi-card:hover {
        transform: translateY(-5px);
        border-color: rgba(229, 9, 20, 0.4);
        box-shadow: 0 10px 30px rgba(229, 9, 20, 0.15);
        background: linear-gradient(135deg, rgba(229, 9, 20, 0.05) 0%, rgba(255, 255, 255, 0.01) 100%);
    }
    .kpi-value {
        font-size: 2.4rem;
        font-weight: 700;
        color: #FFFFFF;
        margin: 8px 0;
        letter-spacing: -0.5px;
    }
    .kpi-label {
        font-size: 0.85rem;
        color: #8C8C9A;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-weight: 600;
    }
    
    /* Tabs custom styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    }
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border: none;
        color: #8C8C9A;
        font-weight: 600;
        font-size: 1.05rem;
        padding: 12px 20px;
        transition: all 0.2s ease;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: #E50914;
    }
    .stTabs [aria-selected="true"] {
        color: #E50914 !important;
        border-bottom: 3px solid #E50914 !important;
    }
    
    /* Form fields and selectors */
    div[data-baseweb="select"] > div, div[data-baseweb="input"] > div {
        background-color: #1C1C1E !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 8px !important;
        color: #FFFFFF !important;
    }
    
    /* Streamlit button overwrite */
    .stButton>button {
        background: linear-gradient(90deg, #E50914 0%, #B80710 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        font-size: 1.05rem !important;
        letter-spacing: 0.5px !important;
        box-shadow: 0 4px 15px rgba(229, 9, 20, 0.3) !important;
        transition: all 0.3s ease !important;
        width: 100%;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #F40A16 0%, #CE0812 100%) !important;
        box-shadow: 0 6px 20px rgba(229, 9, 20, 0.4) !important;
        transform: translateY(-2px);
    }
    .stButton>button:active {
        transform: translateY(0);
    }
    
    /* Box alerts */
    .risk-banner {
        border-radius: 12px;
        padding: 18px;
        margin-bottom: 20px;
        border: 1px solid transparent;
    }
    .risk-high {
        background-color: rgba(229, 9, 20, 0.08);
        border-color: rgba(229, 9, 20, 0.3);
        color: #FF5252;
    }
    .risk-medium {
        background-color: rgba(255, 179, 0, 0.08);
        border-color: rgba(255, 179, 0, 0.3);
        color: #FFD54F;
    }
    .risk-low {
        background-color: rgba(0, 200, 83, 0.08);
        border-color: rgba(0, 200, 83, 0.3);
        color: #69F0AE;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# 3. Cache Model and Data
@st.cache_resource
def load_model():
    try:
        model_path = ROOT / "models" / "best_model.pkl"
        if model_path.exists():
            return joblib.load(model_path)
        else:
            return joblib.load("models/best_model.pkl")
    except Exception as e:
        st.error(f"Erreur de chargement du modèle : {e}")
        return None

@st.cache_data
def load_dashboard_data():
    dataset_path = ROOT / "outputs" / "powerbi_streaming_churn_dataset.csv"
    if dataset_path.exists():
        return pd.read_csv(dataset_path)
    else:
        raw_path = ROOT / "data" / "raw" / "IBM_Telco_Customer_Churn.csv"
        if raw_path.exists():
            try:
                return load_streaming_dataset(str(raw_path))
            except Exception as e:
                st.warning(f"Impossible de traiter les données brutes : {e}")
        return None

model = load_model()
df_dashboard = load_dashboard_data()

# 4. Sidebar Branding & Info
with st.sidebar:
    st.markdown('<div class="brand-title">🎬 StreamRisk</div>', unsafe_allow_html=True)
    st.markdown('<div class="brand-subtitle">Console Marketing & Rétention Client</div>', unsafe_allow_html=True)
    
    st.subheader("Paramètres Globaux")
    threshold = st.slider("Seuil de décision Churn", min_value=0.1, max_value=0.9, value=0.4, step=0.05)
    
    st.markdown("---")
    st.markdown("### À propos du Projet")
    st.info("Ce projet de Data Science suit la méthodologie CRISP-DM adaptée à une plateforme de streaming vidéo type Netflix / Shahid / Prime Video.")
    
    st.markdown("### Équipe & Support")
    st.markdown("""
    - Équipe Marketing & Rétention Client
    - Console de pilotage prédictif du Churn
    """)

# 5. Main Title & Header
st.markdown('<div class="main-title">Prédiction du Churn Client</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Analysez les comportements d\'abonnement, estimez les risques de résiliation et activez des leviers de rétention personnalisés.</div>', unsafe_allow_html=True)

# 6. Tab Navigation Setup
tab1, tab2, tab3 = st.tabs(["📊 Tableau de Bord Rétention", "🔍 Simulateur Individuel", "📂 Prédictions Batch"])

# TAB 1: DASHBOARD
with tab1:
    if df_dashboard is not None:
        # Re-apply threshold to the cached dataset predictions dynamically
        df_dashboard['predicted_class'] = (df_dashboard['churn_probability'] >= threshold).astype(int)
        df_dashboard['risk_level'] = df_dashboard['churn_probability'].apply(
            lambda p: "High" if p >= 0.70 else ("Medium" if p >= 0.40 else "Low")
        )
        
        # KPI calculations
        total_subscribers = len(df_dashboard)
        historic_churn_rate = df_dashboard['churn'].mean() * 100 if 'churn' in df_dashboard.columns else 26.54
        predicted_churn_rate = df_dashboard['predicted_class'].mean() * 100
        
        # Calculate revenue at risk (only for predicted churners)
        revenue_at_risk = df_dashboard[df_dashboard['predicted_class'] == 1]['monthly_subscription_fee'].sum()
        
        # Display KPIs in columns
        kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
        
        with kpi_col1:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Abonnés Totaux</div>
                <div class="kpi-value">{total_subscribers:,}</div>
                <div style="font-size: 0.8rem; color: #8C8C9A;">Taille du dataset évalué</div>
            </div>
            """, unsafe_allow_html=True)
            
        with kpi_col2:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Taux Churn Réel</div>
                <div class="kpi-value" style="color: #8C8C9A;">{historic_churn_rate:.2f}%</div>
                <div style="font-size: 0.8rem; color: #8C8C9A;">Historique initial</div>
            </div>
            """, unsafe_allow_html=True)
            
        with kpi_col3:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Taux Churn Prédit</div>
                <div class="kpi-value">{predicted_churn_rate:.2f}%</div>
                <div style="font-size: 0.8rem; color: #E50914;">Au seuil de {threshold}</div>
            </div>
            """, unsafe_allow_html=True)
            
        with kpi_col4:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Revenu Mensuel à Risque</div>
                <div class="kpi-value" style="color: #FFB300;">{revenue_at_risk:,.2f} $</div>
                <div style="font-size: 0.8rem; color: #8C8C9A;">Cumul des frais mensuels à risque</div>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Charts section
        chart_col1, chart_col2 = st.columns(2)
        
        with chart_col1:
            st.subheader("Distribution des Niveaux de Risque de Churn")
            risk_counts = df_dashboard['risk_level'].value_counts().reset_index()
            risk_counts.columns = ['Niveau de Risque', 'Nombre d\'Abonnés']
            
            # Map colors
            color_map = {'Low': '#00C853', 'Medium': '#FFB300', 'High': '#E50914'}
            fig_risk = px.pie(
                risk_counts, 
                names='Niveau de Risque', 
                values='Nombre d\'Abonnés',
                color='Niveau de Risque',
                color_discrete_map=color_map,
                hole=0.4
            )
            fig_risk.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_color='#FFFFFF',
                legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
            )
            st.plotly_chart(fig_risk, use_container_width=True)
            
        with chart_col2:
            st.subheader("Taux de Churn par Plan d'Abonnement")
            plan_churn = df_dashboard.groupby('subscription_plan')['predicted_class'].mean().reset_index()
            plan_churn.columns = ['Plan d\'Abonnement', 'Taux de Churn Prédit']
            plan_churn['Taux de Churn Prédit'] *= 100
            
            fig_plan = px.bar(
                plan_churn, 
                x='Plan d\'Abonnement', 
                y='Taux de Churn Prédit',
                color='Plan d\'Abonnement',
                color_discrete_sequence=['#E50914', '#E15A60', '#564d4d']
            )
            fig_plan.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_color='#FFFFFF',
                yaxis_ticksuffix="%",
                showlegend=False
            )
            st.plotly_chart(fig_plan, use_container_width=True)
            
        chart_col3, chart_col4 = st.columns(2)
        
        with chart_col3:
            st.subheader("Relation entre l'Ancienneté et la Probabilité de Churn")
            fig_tenure = px.histogram(
                df_dashboard, 
                x='subscription_months', 
                y='predicted_class', 
                histfunc='avg', 
                nbins=12,
                labels={'subscription_months': 'Ancienneté (mois)', 'predicted_class': 'Taux de Churn'},
                color_discrete_sequence=['#E50914']
            )
            fig_tenure.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_color='#FFFFFF',
                yaxis_tickformat='.0%'
            )
            st.plotly_chart(fig_tenure, use_container_width=True)
            
        with chart_col4:
            st.subheader("Importance des Variables Clés (Random Forest)")
            fi_path = ROOT / "outputs" / "random_forest_feature_importance.csv"
            if fi_path.exists():
                fi_df = pd.read_csv(fi_path)
                fig_fi = px.bar(
                    fi_df.head(10), 
                    x='importance', 
                    y='feature',
                    orientation='h',
                    color='importance',
                    color_continuous_scale=[[0, '#564d4d'], [1, '#E50914']]
                )
                fig_fi.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font_color='#FFFFFF',
                    coloraxis_showscale=False,
                    yaxis={'categoryorder': 'total ascending'}
                )
                st.plotly_chart(fig_fi, use_container_width=True)
            else:
                st.info("Le fichier d'importance des variables n'a pas pu être chargé. Lancez l'entraînement dans l'onglet Batch ou via train.py pour le générer.")
                
    else:
        st.warning("Aucune donnée de tableau de bord n'a pu être chargée. Veuillez exécuter l'entraînement des modèles pour générer les fichiers nécessaires.")

# TAB 2: INDIVIDUAL SIMULATOR
with tab2:
    if model is None:
        st.error("Le modèle de prédiction n'est pas chargé. Impossible de simuler.")
    else:
        col_form, col_result = st.columns([2, 1.5], gap="large")
        
        with col_form:
            st.subheader("📝 Fiche de l'Abonné")
            
            # Sub-layouts
            c1, c2 = st.columns(2)
            with c1:
                gender = st.selectbox("Genre", ["Male", "Female"])
                senior_subscriber = st.selectbox("Abonné Senior", ["Non", "Oui"])
                senior_val = 1 if senior_subscriber == "Oui" else 0
                family_account = st.selectbox("Compte Famille (Partner)", ["Oui", "Non"])
                kids_profile = st.selectbox("Profil Enfants (Dependents)", ["Oui", "Non"])
                subscription_months = st.slider("Ancienneté de l'abonnement (Mois)", min_value=1, max_value=72, value=12)
                payment_method = st.selectbox("Moyen de Paiement", [
                    "Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"
                ])
                favorite_genre = st.selectbox("Genre favori", [
                    "Drama", "Comedy", "Sports", "Kids", "Documentary", "Action", "Reality"
                ])
                
            with c2:
                subscription_plan = st.selectbox("Type d'Abonnement", ["Monthly", "Annual", "Two-Year"])
                monthly_subscription_fee = st.number_input("Frais mensuels ($)", min_value=5.0, max_value=150.0, value=25.0, step=0.5)
                total_spent = st.number_input("Dépenses totales accumulées ($)", min_value=0.0, max_value=10000.0, value=300.0, step=5.0)
                streaming_quality = st.selectbox("Qualité maximale de streaming", ["Mobile only", "Standard HD", "Ultra HD"])
                shared_profiles = st.selectbox("Profils partagés (MultipleLines)", ["Single", "Multiple"])
                offline_downloads = st.selectbox("Téléchargements hors-ligne (OnlineBackup)", ["Oui", "Non"])
                mobile_access = st.selectbox("Accès Mobile (PhoneService)", ["Oui", "Non"])
                digital_billing = st.selectbox("Facturation dématérialisée (PaperlessBilling)", ["Oui", "Non"])
            
            st.markdown("---")
            st.subheader("📈 Métriques comportementales & Support")
            c3, c4 = st.columns(2)
            with c3:
                views_per_week = st.slider("Nombre de sessions de visionnage / semaine", min_value=1, max_value=50, value=15)
                average_watch_time = st.slider("Temps moyen de visionnage / session (Heures)", min_value=0.1, max_value=8.0, value=2.0, step=0.1)
                number_of_devices = st.slider("Nombre d'écrans enregistrés", min_value=1, max_value=6, value=3)
            with c4:
                account_security = st.selectbox("Sécurité renforcée du compte", ["Oui", "Non"])
                device_protection = st.selectbox("Protection de l'appareil (DeviceProtection)", ["Oui", "Non"])
                premium_support = st.selectbox("Support Client Premium (TechSupport)", ["Oui", "Non"])
                live_tv_package = st.selectbox("Bouquet TV en direct", ["Oui", "Non"])
                movie_package = st.selectbox("Bouquet Cinéma (StreamingMovies)", ["Oui", "Non"])
                
            # Auto-calculate derived variables
            engagement_score = round((views_per_week * average_watch_time) / number_of_devices, 2)
            subscription_value_ratio = round(total_spent / monthly_subscription_fee, 2) if monthly_subscription_fee > 0 else 0.0
            
            # Map French 'Oui'/'Non' to Model expected 'Yes'/'No'
            map_yn = lambda val: "Yes" if val == "Oui" else "No"
            
            input_dict = {
                'gender': [gender],
                'senior_subscriber': [senior_val],
                'family_account': [map_yn(family_account)],
                'kids_profile': [map_yn(kids_profile)],
                'subscription_months': [subscription_months],
                'mobile_access': [map_yn(mobile_access)],
                'shared_profiles': [shared_profiles],
                'streaming_quality': [streaming_quality],
                'account_security': [map_yn(account_security)],
                'offline_downloads': [map_yn(offline_downloads)],
                'device_protection': [map_yn(device_protection)],
                'premium_support': [map_yn(premium_support)],
                'live_tv_package': [map_yn(live_tv_package)],
                'movie_package': [map_yn(movie_package)],
                'subscription_plan': [subscription_plan],
                'digital_billing': [map_yn(digital_billing)],
                'payment_method': [payment_method],
                'monthly_subscription_fee': [monthly_subscription_fee],
                'total_spent': [total_spent],
                'views_per_week': [views_per_week],
                'average_watch_time': [average_watch_time],
                'number_of_devices': [number_of_devices],
                'favorite_genre': [favorite_genre],
                'engagement_score': [engagement_score],
                'subscription_value_ratio': [subscription_value_ratio]
            }
            
            input_df = pd.DataFrame(input_dict)
            
        with col_result:
            st.subheader("🎯 Score de Risque & Recommandations")
            
            # Trigger prediction directly on input change for dynamic feeling
            prob_churn = model.predict_proba(input_df)[0, 1]
            
            # Color mapping & HTML Banner
            if prob_churn >= 0.70:
                risk_class = "HIGH RISK"
                banner_style = "risk-high"
                action_color = "#FF5252"
            elif prob_churn >= threshold:
                risk_class = "MEDIUM RISK"
                banner_style = "risk-medium"
                action_color = "#FFD54F"
            else:
                risk_class = "LOW RISK"
                banner_style = "risk-low"
                action_color = "#69F0AE"
                
            st.markdown(f"""
            <div class="risk-banner {banner_style}">
                <div style="font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1px; font-weight: bold;">Statut de Risque</div>
                <div style="font-size: 1.8rem; font-weight: 700;">{risk_class} ({prob_churn*100:.1f}%)</div>
                <div style="font-size: 0.85rem; margin-top: 5px;">Seuil de décision : {threshold}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Gauge Chart
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=prob_churn * 100,
                domain={'x': [0, 1], 'y': [0, 1]},
                gauge={
                    'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#FFFFFF"},
                    'bar': {'color': "#E50914"},
                    'bgcolor': "rgba(255, 255, 255, 0.05)",
                    'borderwidth': 1,
                    'bordercolor': "rgba(255, 255, 255, 0.1)",
                    'steps': [
                        {'range': [0, threshold*100], 'color': 'rgba(0, 200, 83, 0.15)'},
                        {'range': [threshold*100, 70], 'color': 'rgba(255, 179, 0, 0.15)'},
                        {'range': [70, 100], 'color': 'rgba(229, 9, 20, 0.15)'}
                    ]
                }
            ))
            fig_gauge.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_color='#FFFFFF',
                height=220,
                margin=dict(l=10, r=10, t=10, b=10)
            )
            st.plotly_chart(fig_gauge, use_container_width=True)
            
            # Display computed scores
            st.markdown(f"""
            * **Engagement Score** : `{engagement_score}` (heures visualisées par écran)
            * **Subscription Value Ratio** : `{subscription_value_ratio}` (ancienneté financière relative)
            """)
            
            # Actionable Retention Recommendations
            st.markdown("### 🛠️ Actions de Rétention Recommandées")
            recs = []
            
            if prob_churn >= threshold:
                if subscription_plan == "Monthly":
                    recs.append("💡 **Upgrade d'engagement** : Proposer une réduction de 20% sur un plan Annuel pour sécuriser l'abonné sur 12 mois.")
                if premium_support == "Non":
                    recs.append("💡 **Support Premium** : Offrir l'option Premium Support gratuitement pendant 3 mois pour l'aider à résoudre ses bugs ou difficultés techniques.")
                if account_security == "Non":
                    recs.append("💡 **Sécurisation du Compte** : Envoyer une notification push suggérant d'activer la double authentification (MFA).")
                if views_per_week < 10:
                    recs.append("💡 **Baisse d'engagement** : Déclencher une newsletter personnalisée avec les nouveautés de son genre favori : **" + favorite_genre + "**.")
                if streaming_quality == "Ultra HD" and monthly_subscription_fee > 60:
                    recs.append("💡 **Optimisation Tarifaire** : Proposer de repasser sur le plan Standard HD pour réduire son coût mensuel s'il exprime une insatisfaction liée aux tarifs.")
                    
                if not recs:
                    recs.append("💡 **Campagne Directe** : Envoyer un bon promotionnel (1 mois gratuit) ou un accès anticipé à des contenus exclusifs.")
            else:
                recs.append("✅ **Abonné Loyal** : Maintenir le contact régulier avec des suggestions de contenus et des fonctionnalités bêta.")
                
            for rec in recs:
                st.markdown(f'<div class="recommendation-box">{rec}</div>', unsafe_allow_html=True)

# TAB 3: BATCH PREDICTION
with tab3:
    st.subheader("📂 Traiter des listes de clients (Fichier CSV)")
    st.write("Uploadez un fichier client au format IBM Telco Churn initial (avec les colonnes originales comme `tenure`, `MonthlyCharges`) ou déjà adapté pour lancer des prédictions en masse.")
    
    uploaded_file = st.file_uploader("Sélectionner un fichier CSV", type=['csv'])
    
    if uploaded_file is not None:
        try:
            # Read CSV
            df_input = pd.read_csv(uploaded_file)
            st.success("Fichier chargé avec succès !")
            st.dataframe(df_input.head(5))
            
            if st.button("Lancer les prédictions batch"):
                with st.spinner("Exécution du pipeline de prédiction..."):
                    # Check and transform columns if raw
                    if "customerID" in df_input.columns:
                        df_processed = add_behavioral_features(adapt_telco_to_streaming(df_input))
                    elif "customer_id" in df_input.columns:
                        df_processed = df_input.copy()
                    else:
                        st.error("Le format du CSV n'est pas reconnu (le fichier doit contenir au moins la colonne 'customerID' ou 'customer_id').")
                        st.stop()
                    
                    customer_ids = df_processed["customer_id"]
                    X = df_processed.drop(columns=["customer_id", "churn"], errors="ignore")
                    
                    # Ensure exact model columns
                    expected_features = model.named_steps['preprocessor'].feature_names_in_
                    X = X[expected_features]
                    
                    # Run predictions
                    probs = model.predict_proba(X)[:, 1]
                    
                    # Construct results dataframe
                    df_results = pd.DataFrame({
                        "customer_id": customer_ids,
                        "churn_probability": probs.round(4),
                        "predicted_class": (probs >= threshold).astype(int),
                        "risk_level": ["High" if p >= 0.70 else ("Medium" if p >= threshold else "Low") for p in probs]
                    })
                    
                    st.success("Traitement batch terminé !")
                    
                    # Visualizations
                    c_b1, c_b2 = st.columns(2)
                    
                    with c_b1:
                        st.subheader("Répartition des Prédictions")
                        pred_counts = df_results['risk_level'].value_counts().reset_index()
                        pred_counts.columns = ['Statut', 'Nombre']
                        fig_b_risk = px.bar(
                            pred_counts, 
                            x='Statut', 
                            y='Nombre', 
                            color='Statut',
                            color_discrete_map={'Low': '#00C853', 'Medium': '#FFB300', 'High': '#E50914'}
                        )
                        fig_b_risk.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#FFFFFF')
                        st.plotly_chart(fig_b_risk, use_container_width=True)
                        
                    with c_b2:
                        st.subheader("Distribution Globale des Probabilités")
                        fig_b_dist = px.histogram(
                            df_results, 
                            x='churn_probability', 
                            nbins=20,
                            color_discrete_sequence=['#E50914']
                        )
                        fig_b_dist.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#FFFFFF')
                        st.plotly_chart(fig_b_dist, use_container_width=True)
                    
                    # Download CSV setup
                    csv = df_results.to_csv(index=False)
                    b64 = base64.b64encode(csv.encode()).decode()
                    href = f'<a href="data:file/csv;base64,{b64}" download="predictions_batch_churn.csv" style="text-decoration:none;"><button style="background-color:#E50914; color:white; padding: 12px 20px; border:none; border-radius:8px; font-weight:bold; cursor:pointer; width:100%;">📥 Télécharger les prédictions (.csv)</button></a>'
                    st.markdown(href, unsafe_allow_html=True)
                    
                    st.dataframe(df_results.head(100))
                    
        except Exception as e:
            st.error(f"Une erreur est survenue lors de la prédiction batch : {e}")
