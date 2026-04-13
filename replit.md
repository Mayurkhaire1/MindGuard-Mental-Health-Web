# Overview

MindGuard is a professional-grade mental health analysis system that uses AI-powered text analysis to detect depression indicators and provide crisis intervention support. The application analyzes user-submitted text to identify emotional patterns, depression risk levels, and potential crisis situations, offering immediate resources and support when needed. Built as an academic project with commercial-quality standards, it combines natural language processing, emotion detection, and clinical psychology principles to create a comprehensive mental health support tool.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Frontend Architecture
- **Flask Template Engine**: Server-side rendering using Jinja2 templates with a responsive Bootstrap 5 UI framework
- **Modern Design System**: Professional mental health-themed interface with calming color palette, consistent spacing, and accessibility features
- **Interactive Dashboard**: Real-time analytics with Chart.js visualizations for emotion trends and risk assessment
- **Crisis Intervention Interface**: Immediate response system with emergency contact integration and safety planning resources

## Backend Architecture
- **Flask Web Framework**: Lightweight Python web application with modular route handling and session management
- **Custom NLP Engine**: Text preprocessing, tokenization, and feature extraction without external NLP dependencies
- **Multi-Component Analysis**: Separate modules for emotion detection, depression prediction, and crisis intervention
- **Lexicon-Based Analysis**: Clinical depression indicators and emotion detection using comprehensive word databases

## Data Storage Solutions
- **SQLAlchemy ORM**: Database abstraction layer supporting both SQLite (development) and PostgreSQL (production)
- **Comprehensive Data Models**: User sessions, emotion lexicons, depression indicators, crisis keywords, and analysis metrics
- **Sample Data Management**: Automated database initialization with clinical-grade lexicons and test datasets
- **JSON Data Storage**: Static lexicons and configuration data stored in structured JSON files

## Core Analysis Components
- **Emotion Detector**: Lexicon-based emotion classification with intensity scoring and pattern recognition
- **Depression Predictor**: Multi-factor depression risk assessment using clinical indicators and cognitive patterns
- **Crisis Intervention System**: Real-time crisis detection with automated emergency resource provision
- **NLP Engine**: Custom text processing pipeline with contraction expansion, negation handling, and feature extraction

## External Dependencies

### Development Tools
- **Flask Framework**: Web application framework with SQLAlchemy for database operations
- **Bootstrap 5 & Font Awesome**: Frontend UI components and iconography for professional interface design
- **Chart.js**: Client-side data visualization for analytics dashboard and trend analysis

### Database Systems
- **SQLite**: Embedded database for development and standalone deployment
- **PostgreSQL**: Optional production database with connection pooling and performance optimization

### Testing Framework
- **Pytest**: Comprehensive test suite covering NLP engine, emotion detection, and depression prediction algorithms

### Static Assets
- **JSON Data Files**: Pre-built lexicons for emotions, depression indicators, and crisis keywords
- **CSS/JS Libraries**: Custom styling and interactive functionality for mental health-specific user experience

Note: The system is designed to operate entirely offline once deployed, with no external API dependencies for core functionality, ensuring privacy and reliability for sensitive mental health applications.