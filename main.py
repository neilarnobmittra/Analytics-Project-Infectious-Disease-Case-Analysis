# =============================================
# HEALTHGUARD ANALYTICS - COVID-19 DASHBOARD
# ARTIFICIAL INTELLIGENCE MINOR PROJECT
# Submitted by: Neilarnob Mittra | March 2026
# =============================================

from kivy.app import App
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelHeader
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
import os
import warnings
warnings.filterwarnings('ignore')

Window.size = (1480, 960)
Window.title = "HealthGuard Analytics - COVID-19 Early Case Dashboard"

class CovidDashboardApp(App):
    def build(self):
        self.df = None
        self.model_summary = ""
        self.r2 = 0.0
        self.plots_dir = "plots"
        os.makedirs(self.plots_dir, exist_ok=True)

        self.main_layout = BoxLayout(orientation='vertical')

        with self.main_layout.canvas.before:
            Color(0.0, 0.12, 0.25, 1)
            self.bg = Rectangle(size=self.main_layout.size, pos=self.main_layout.pos)
        self.main_layout.bind(size=self.update_bg, pos=self.update_bg)

        self.header = Label(
            text="COVID-19 Early Case Trend Analysis & Recovery Insights\nHealthGuard Analytics Pvt. Ltd.",
            font_size=29, bold=True, size_hint_y=0.13, color=(0.95, 0.40, 0.05, 1), halign='center'
        )
        with self.header.canvas.before:
            Color(0.0, 0.08, 0.18, 1)
            self.header_bg = Rectangle(size=self.header.size, pos=self.header.pos)

        btn_row = BoxLayout(size_hint_y=0.11, spacing=30, padding=40)

        
        self.upload_btn = Button(
            text="UPLOAD CSV FILE",
            font_size=26,
            bold=True,
            background_color=(0.0, 0.62, 0.72, 1),   # Premium bright teal
            size_hint_x=0.48,
            height=98
        )
        self.run_btn = Button(
            text="RUN FULL ANALYSIS",
            font_size=26,
            bold=True,
            background_color=(0.0, 0.48, 0.78, 1),   # Slightly deeper teal
            size_hint_x=0.48,
            height=98
        )

        # Thin white border for premium look
        with self.upload_btn.canvas.before:
            Color(1, 1, 1, 0.35)
            self.upload_border = Rectangle(pos=self.upload_btn.pos, size=self.upload_btn.size)
        with self.run_btn.canvas.before:
            Color(1, 1, 1, 0.35)
            self.run_border = Rectangle(pos=self.run_btn.pos, size=self.run_btn.size)

        self.upload_btn.bind(on_press=self.show_upload)
        self.run_btn.bind(on_press=self.show_processing_popup)

        self.run_btn.disabled = True

        btn_row.add_widget(self.upload_btn)
        btn_row.add_widget(self.run_btn)

        self.tabs = TabbedPanel(do_default_tab=False, tab_width=255, tab_height=62)
        tab_list = ["Dashboard", "Demographics", "Infection Spread", "Recovery Trends", "Regression Model"]
        self.tab_content = {}

        for name in tab_list:
            tab = TabbedPanelHeader(text=name)
            scroll = ScrollView()
            box = BoxLayout(orientation='vertical', padding=30, spacing=25)
            scroll.add_widget(box)
            tab.content = scroll
            self.tabs.add_widget(tab)
            self.tab_content[name] = box

        self.update_tab("Dashboard", "Welcome!\n\nClick UPLOAD CSV FILE to begin")

        self.main_layout.add_widget(self.header)
        self.main_layout.add_widget(btn_row)
        self.main_layout.add_widget(self.tabs)

        footer = Label(
            text="Developed by Neilarnob Mittra | Artificial Intelligence Minor Project | March 2026",
            font_size=13, size_hint_y=0.04, color=(0.95, 0.40, 0.05, 1)
        )
        self.main_layout.add_widget(footer)

        return self.main_layout

    
    def update_bg(self, *args):
        self.bg.pos = self.main_layout.pos
        self.bg.size = self.main_layout.size

    def show_upload(self, instance):
        content = BoxLayout(orientation='vertical', padding=20)
        fc = FileChooserListView(path=os.getcwd(), filters=['*.csv'])
        content.add_widget(fc)
        select = Button(text="UPLOAD SELECTED FILE", size_hint_y=0.15, background_color=(0.0, 0.55, 0.65, 1))
        content.add_widget(select)
        popup = Popup(title='Upload CSV File', content=content, size_hint=(0.78, 0.85))
        def load(*args):
            if fc.selection:
                self.load_csv(fc.selection[0])
                popup.dismiss()
        select.bind(on_press=load)
        popup.open()

    def load_csv(self, path):
        try:
            self.df = pd.read_csv(path)
            self.show_popup("Success", f"CSV Uploaded Successfully!\nRows: {len(self.df):,}")
            self.run_btn.disabled = False
        except Exception as e:
            self.show_popup("Error", f"Failed:\n{str(e)}")

    def show_processing_popup(self, instance):
        content = Label(text="Processing...\nPlease wait", font_size=22, halign='center')
        self.processing_popup = Popup(title='Running Analysis', content=content, size_hint=(0.5, 0.3))
        self.processing_popup.open()
        Clock.schedule_once(self.do_analysis, 0.2)

    def do_analysis(self, dt):
        self.run_analysis(None)
        self.processing_popup.dismiss()

    def show_popup(self, title, msg):
        Popup(title=title, content=Label(text=msg, font_size=20, halign='center'), size_hint=(0.6, 0.42)).open()

    def run_analysis(self, instance):
        if self.df is None:
            self.show_popup("Error", "Please upload CSV file first!")
            return
        for f in os.listdir(self.plots_dir):
            if f.endswith((".png", ".txt")):
                os.remove(os.path.join(self.plots_dir, f))
        df = self.df.copy()
        date_cols = ['confirmed_date', 'released_date', 'deceased_date']
        for col in date_cols:
            df[col] = pd.to_datetime(df[col], errors='coerce')
        df['birth_year'] = pd.to_numeric(df['birth_year'], errors='coerce')
        df['age'] = 2020 - df['birth_year']
        df['recovery_days'] = np.nan
        mask = (df['state'] == 'released') & df['released_date'].notna() & df['confirmed_date'].notna()
        df.loc[mask, 'recovery_days'] = (df.loc[mask, 'released_date'] - df.loc[mask, 'confirmed_date']).dt.days
        plt.rcParams['figure.facecolor'] = '#001F3F'
        plt.rcParams['axes.facecolor'] = '#001F3F'
        plt.rcParams['text.color'] = '#FF8C00'
        plt.rcParams['axes.labelcolor'] = '#FF8C00'
        plt.rcParams['xtick.color'] = 'white'
        plt.rcParams['ytick.color'] = 'white'
        plt.style.use('seaborn-v0_8')
        def save_plot(name, title):
            plt.title(title, fontsize=16, pad=15, color='#FF8C00')
            plt.tight_layout()
            plt.savefig(os.path.join(self.plots_dir, name), dpi=120)
            plt.close()
        plt.figure(figsize=(7,4.5)); sns.countplot(x='sex', data=df, palette='pastel'); save_plot('gender.png', 'Gender Distribution')
        plt.figure(figsize=(7,4.5)); sns.histplot(df['age'].dropna(), bins=20, kde=True, color='#00A8A8'); save_plot('age.png', 'Age Distribution')
        plt.figure(figsize=(7,4.5)); top_r = df['region'].value_counts().head(12); sns.barplot(x=top_r.values, y=top_r.index, palette='viridis'); save_plot('region.png', 'Regional Cases')
        plt.figure(figsize=(7,4.5)); top_reason = df['infection_reason'].value_counts().head(10); sns.barplot(y=top_reason.index, x=top_reason.values, palette='magma'); save_plot('infection.png', 'Infection Reasons')
        released = df[df['state']=='released']
        plt.figure(figsize=(7,4.5)); sns.histplot(released['recovery_days'].dropna(), bins=25, kde=True, color='#00A8A8'); save_plot('recovery.png', 'Recovery Days')
        region_out = df.groupby('region').agg(Confirmed=('id','count'), Released=('state', lambda x: (x=='released').sum())).head(8)
        plt.figure(figsize=(7,4.5)); region_out.plot(kind='bar', color=['#002B5B', '#00A8A8']); save_plot('region_outcomes.png', 'Confirmed vs Released')
        num = ['age','contact_number','infection_order','recovery_days']
        plt.figure(figsize=(7,4.5)); sns.heatmap(df[num].corr(), annot=True, cmap='coolwarm', fmt='.2f'); save_plot('correlation.png', 'Correlation')
        df['age_group'] = pd.cut(df['age'], bins=[0,20,40,60,80,100], labels=['0-20','21-40','41-60','61-80','81+'])
        plt.figure(figsize=(7,4.5)); sns.boxplot(x='age_group', y='recovery_days', data=df, palette='Set2'); save_plot('age_recovery.png', 'Recovery by Age')
        try:
            reg_df = df.dropna(subset=['age','contact_number','infection_order','recovery_days']).copy()
            if len(reg_df) < 10:
                self.model_summary = "Not enough data for regression."
                self.r2 = 0.0
            else:
                X = sm.add_constant(reg_df[['age','contact_number','infection_order']])
                model = sm.OLS(reg_df['recovery_days'], X).fit()
                self.model_summary = str(model.summary())
                self.r2 = model.rsquared
                residuals = model.resid
                plt.figure(figsize=(7,4.5)); sns.histplot(residuals, kde=True, color='#00A8A8'); save_plot('residual_hist.png', 'Residual Distribution')
                plt.figure(figsize=(7,4.5)); sns.scatterplot(x=model.fittedvalues, y=residuals); plt.axhline(0, color='red', linestyle='--'); save_plot('residual_scatter.png', 'Residuals vs Fitted Values')
        except:
            self.model_summary = "Regression skipped."
            self.r2 = 0.0
            plt.figure(figsize=(7,4.5)); plt.text(0.5, 0.5, "No data", ha='center', color='white'); save_plot('residual_hist.png', '')
            plt.figure(figsize=(7,4.5)); plt.text(0.5, 0.5, "No data", ha='center', color='white'); save_plot('residual_scatter.png', '')
        with open(os.path.join(self.plots_dir, 'regression_summary.txt'), 'w') as f:
            f.write(self.model_summary)
        self.update_tabs(df)
        self.show_popup("Success", "Analysis Complete!")

    def update_tabs(self, df):
        d = self.tab_content["Dashboard"]
        d.clear_widgets()
        insights = BoxLayout(orientation='vertical', size_hint_y=None, height=180)
        insights.add_widget(Label(text="KEY INSIGHTS", font_size=24, bold=True, color=(0.95, 0.40, 0.05, 1), halign='center'))
        insights.add_widget(Label(text=f"High-Risk Age Group: 60+ years", font_size=18, color=(0.95, 0.40, 0.05, 1)))
        insights.add_widget(Label(text=f"Average Recovery Time: {df[df['state']=='released']['recovery_days'].mean():.1f} days", font_size=18, color=(0.95, 0.40, 0.05, 1)))
        insights.add_widget(Label(text=f"Total Deceased: {(df['state']=='deceased').sum():,}", font_size=18, color=(0.95, 0.40, 0.05, 1)))
        d.add_widget(insights)
        d.add_widget(Image(source=os.path.join(self.plots_dir, 'gender.png'), size_hint_y=None, height=410))
        self.fill_tab("Demographics", "Who is getting infected?", ['gender.png','age.png','region.png'])
        self.fill_tab("Infection Spread", "How are infections spreading?", ['infection.png','region_outcomes.png'])
        self.fill_tab("Recovery Trends", "What are the recovery trends?", ['recovery.png','age_recovery.png','correlation.png'])
       
        r = self.tab_content["Regression Model"]
        r.clear_widgets()
        r.add_widget(Label(text="Linear Regression - Recovery Time Prediction", font_size=24, bold=True, color=(0.95, 0.40, 0.05, 1), halign='center', size_hint_y=None, height=60))
        r.add_widget(Label(text=f"R² Score: {self.r2:.4f}", font_size=23, color=(0.95, 0.40, 0.05, 1), halign='center', size_hint_y=None, height=40))
        r.add_widget(Label(text="", size_hint_y=None, height=20))
        reg_scroll = ScrollView(size_hint_y=None, height=650)
        reg_content = BoxLayout(orientation='vertical', padding=20, spacing=20, size_hint_y=None)
        hbox = BoxLayout(orientation='horizontal', spacing=30, size_hint_y=None, height=800)
        hbox.add_widget(Image(source=os.path.join(self.plots_dir, 'residual_hist.png'), size_hint_x=0.5))
        hbox.add_widget(Image(source=os.path.join(self.plots_dir, 'residual_scatter.png'), size_hint_x=0.5))
        reg_content.add_widget(hbox)
        reg_content.add_widget(Label(text="Scroll Down for Full Regression Summary ", font_size=17, color=(0.95, 0.40, 0.05, 1), halign='center', size_hint_y=None, height=10))
        summary_label = Label(
            text=self.model_summary[:3000] + "\n\n(Full summary also saved in plots/regression_summary.txt)",
            font_size=13,
            color=(0.95, 0.40, 0.05, 1),
            halign='center',
            size_hint_y=None,
            height=900
        )
        summary_label.bind(size=lambda *args: setattr(summary_label, 'text_size', (summary_label.width - 50, None)))
        reg_content.add_widget(summary_label)
        reg_content.height = 1950
        reg_scroll.add_widget(reg_content)
        r.add_widget(reg_scroll)

    def fill_tab(self, name, title, imgs):
        c = self.tab_content[name]
        c.clear_widgets()
        c.add_widget(Label(text=title, font_size=24, bold=True, color=(0.95, 0.40, 0.05, 1), halign='center', size_hint_y=None, height=55))
        hbox = BoxLayout(orientation='horizontal', spacing=20, size_hint_y=None, height=430)
        for img_name in imgs:
            hbox.add_widget(Image(source=os.path.join(self.plots_dir, img_name), size_hint_x=0.5))
        c.add_widget(hbox)

    def update_tab(self, name, text):
        self.tab_content[name].clear_widgets()
        self.tab_content[name].add_widget(Label(text=text, font_size=19, color=(0.95, 0.40, 0.05, 1), halign='center'))

if __name__ == '__main__':
    CovidDashboardApp().run()
