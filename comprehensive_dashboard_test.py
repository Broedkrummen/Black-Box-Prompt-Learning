"""
Comprehensive Dashboard Testing Script
Tests all 4 SEO dashboard versions thoroughly
"""

import subprocess
import time
import requests
import threading
import os
import sys
from tkinter import Tk
import signal

class DashboardTester:
    def __init__(self):
        self.test_results = {}
        self.test_domain = "simplybeyond.dk"
        self.test_location = "DK"
        self.test_language = "da"

    def test_streamlit_dashboard(self):
        """Test Streamlit dashboard"""
        print("🧪 Testing Streamlit Dashboard...")
        results = {
            "name": "Streamlit Dashboard",
            "status": "pending",
            "issues": [],
            "features_tested": []
        }

        try:
            # Check if streamlit is installed
            import streamlit
            results["features_tested"].append("✅ Streamlit installed")

            # Test basic functionality
            results["features_tested"].append("✅ Basic import successful")

            # Test if we can run the dashboard (without actually starting server)
            try:
                # Just check if the file can be imported
                spec = importlib.util.spec_from_file_location("streamlit_dashboard", "seo_dashboard_streamlit.py")
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                results["features_tested"].append("✅ Dashboard script loads without errors")
            except Exception as e:
                results["issues"].append(f"❌ Script loading error: {e}")

            results["status"] = "completed"

        except ImportError:
            results["issues"].append("❌ Streamlit not installed")
            results["status"] = "failed"

        self.test_results["streamlit"] = results
        return results

    def test_flask_dashboard(self):
        """Test Flask dashboard"""
        print("🧪 Testing Flask Dashboard...")
        results = {
            "name": "Flask Dashboard",
            "status": "pending",
            "issues": [],
            "features_tested": []
        }

        try:
            # Check if flask is installed
            import flask
            results["features_tested"].append("✅ Flask installed")

            # Test basic functionality
            from flask import Flask
            app = Flask(__name__)

            @app.route('/')
            def test_route():
                return "Test route working"

            results["features_tested"].append("✅ Flask app creation successful")

            # Test if dashboard script can be imported
            try:
                spec = importlib.util.spec_from_file_location("flask_dashboard", "seo_dashboard_flask.py")
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                results["features_tested"].append("✅ Dashboard script loads without errors")
            except Exception as e:
                results["issues"].append(f"❌ Script loading error: {e}")

            results["status"] = "completed"

        except ImportError:
            results["issues"].append("❌ Flask not installed")
            results["status"] = "failed"

        self.test_results["flask"] = results
        return results

    def test_dash_dashboard(self):
        """Test Dash dashboard"""
        print("🧪 Testing Dash Dashboard...")
        results = {
            "name": "Dash Dashboard",
            "status": "pending",
            "issues": [],
            "features_tested": []
        }

        try:
            # Check if dash is installed
            import dash
            results["features_tested"].append("✅ Dash installed")

            # Test basic functionality
            from dash import Dash, html
            app = Dash(__name__)
            app.layout = html.Div([html.H1("Test Dash App")])
            results["features_tested"].append("✅ Dash app creation successful")

            # Test if dashboard script can be imported
            try:
                spec = importlib.util.spec_from_file_location("dash_dashboard", "seo_dashboard_dash.py")
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                results["features_tested"].append("✅ Dashboard script loads without errors")
            except Exception as e:
                results["issues"].append(f"❌ Script loading error: {e}")

            results["status"] = "completed"

        except ImportError:
            results["issues"].append("❌ Dash not installed")
            results["status"] = "failed"

        self.test_results["dash"] = results
        return results

    def test_tkinter_dashboard(self):
        """Test Tkinter dashboard"""
        print("🧪 Testing Tkinter Dashboard...")
        results = {
            "name": "Tkinter Dashboard",
            "status": "pending",
            "issues": [],
            "features_tested": []
        }

        try:
            # Check if tkinter is available
            import tkinter as tk
            results["features_tested"].append("✅ Tkinter available")

            # Test basic functionality
            root = tk.Tk()
            root.title("Test Tkinter Window")
            label = tk.Label(root, text="Test Label")
            label.pack()
            results["features_tested"].append("✅ Tkinter window creation successful")

            # Test if matplotlib is available for charts
            try:
                import matplotlib.pyplot as plt
                results["features_tested"].append("✅ Matplotlib available for charts")
            except ImportError:
                results["issues"].append("⚠️ Matplotlib not available - charts will not work")

            # Test if dashboard script can be imported
            try:
                spec = importlib.util.spec_from_file_location("tkinter_dashboard", "simple_tkinter_dashboard.py")
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                results["features_tested"].append("✅ Dashboard script loads without errors")
            except Exception as e:
                results["issues"].append(f"❌ Script loading error: {e}")

            results["status"] = "completed"

        except ImportError:
            results["issues"].append("❌ Tkinter not available")
            results["status"] = "failed"

        self.test_results["tkinter"] = results
        return results

    def test_dependencies(self):
        """Test all required dependencies"""
        print("🧪 Testing Dependencies...")
        dependencies = {
            "streamlit": ["streamlit"],
            "flask": ["flask"],
            "dash": ["dash", "plotly"],
            "tkinter": ["tkinter"],
            "common": ["requests", "pandas", "beautifulsoup4"]
        }

        dep_results = {}

        for category, packages in dependencies.items():
            dep_results[category] = {}
            for package in packages:
                try:
                    if package == "tkinter":
                        import tkinter
                    else:
                        __import__(package)
                    dep_results[category][package] = "✅ Installed"
                except ImportError:
                    dep_results[category][package] = "❌ Missing"

        return dep_results

    def run_comprehensive_tests(self):
        """Run all comprehensive tests"""
        print("🚀 Starting Comprehensive Dashboard Testing\n")
        print("=" * 60)

        # Test dependencies first
        print("📦 Testing Dependencies...")
        dep_results = self.test_dependencies()

        print("\nDependency Status:")
        for category, packages in dep_results.items():
            print(f"\n{category.upper()}:")
            for package, status in packages.items():
                print(f"  {package}: {status}")

        print("\n" + "=" * 60)

        # Test each dashboard
        self.test_streamlit_dashboard()
        print()
        self.test_flask_dashboard()
        print()
        self.test_dash_dashboard()
        print()
        self.test_tkinter_dashboard()

        print("\n" + "=" * 60)
        print("📊 TEST RESULTS SUMMARY")
        print("=" * 60)

        all_passed = True
        for dashboard, results in self.test_results.items():
            status_icon = "✅" if results["status"] == "completed" else "❌"
            print(f"\n{dashboard.upper()} DASHBOARD: {status_icon} {results['status'].upper()}")

            if results["features_tested"]:
                print("Features tested:")
                for feature in results["features_tested"]:
                    print(f"  {feature}")

            if results["issues"]:
                print("Issues found:")
                for issue in results["issues"]:
                    print(f"  {issue}")
                all_passed = False

        print("\n" + "=" * 60)
        if all_passed:
            print("🎉 ALL DASHBOARDS PASSED TESTING!")
        else:
            print("⚠️ SOME ISSUES FOUND - SEE DETAILS ABOVE")

        return self.test_results

def main():
    tester = DashboardTester()
    results = tester.run_comprehensive_tests()

    # Save results to file
    with open("dashboard_test_results.txt", "w", encoding="utf-8") as f:
        f.write("COMPREHENSIVE DASHBOARD TEST RESULTS\n")
        f.write("=" * 50 + "\n\n")

        for dashboard, result in results.items():
            f.write(f"{dashboard.upper()} DASHBOARD\n")
            f.write(f"Status: {result['status']}\n")
            f.write(f"Features Tested: {len(result['features_tested'])}\n")
            f.write(f"Issues Found: {len(result['issues'])}\n")

            if result['features_tested']:
                f.write("Features:\n")
                for feature in result['features_tested']:
                    f.write(f"  {feature}\n")

            if result['issues']:
                f.write("Issues:\n")
                for issue in result['issues']:
                    f.write(f"  {issue}\n")

            f.write("\n" + "-" * 30 + "\n")

    print("\n📄 Results saved to dashboard_test_results.txt")

if __name__ == "__main__":
    import importlib.util
    main()
