# Design Document: Crop Disease Detection System

## Overview

The AI-Powered Crop Disease Detection and Recommendation System is a comprehensive web application that enables farmers and agricultural professionals to identify crop diseases through image analysis. The system leverages machine learning models or external AI APIs to analyze uploaded crop images, detect diseases, and provide actionable recommendations including treatment plans, prevention strategies, and fertilizer suggestions.

The application follows a modern three-tier architecture with a Python Flask backend, vanilla JavaScript frontend, and SQLite database. It supports user authentication, scan history tracking, administrative controls, and comprehensive disease reporting. The system is designed to be lightweight and deployable on PythonAnywhere's free hosting tier while maintaining robust security, performance, and user experience standards.

## Architecture

### System Architecture Overview

```mermaid
graph TB
    subgraph "Client Layer"
        UI[Web Browser]
        UI_HTML[HTML5 Templates]
        UI_CSS[CSS3 Styling]
        UI_JS[Vanilla JavaScript]
    end
    
    subgraph "Application Layer"
        Flask[Flask Application]
        Auth[Authentication Service]
        Scanner[Disease Detection Service]
        History[History Service]
        Admin[Admin Service]
        API[REST API Endpoints]
    end
    
    subgraph "Data Layer"
        DB[(SQLite Database)]
        FileStore[File Storage]
    end
    
    subgraph "External Services"
        ML_API[AI Detection API]
        TF[TensorFlow Model]
    end
    
    UI --> Flask
    Flask --> Auth
    Flask --> Scanner
    Flask --> History
    Flask --> Admin
    Flask --> API
    
    Auth --> DB
    Scanner --> DB
    Scanner --> FileStore
    Scanner --> ML_API
    Scanner --> TF
    History --> DB
    Admin --> DB
    
    style Flask fill:#2ecc71
    style DB fill:#3498db
    style ML_API fill:#e74c3c
