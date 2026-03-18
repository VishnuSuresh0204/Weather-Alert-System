# Weather Alert System

A Django-based web application designed to provide real-time weather alerts and emergency SOS services for fishermen and marine rescue operations.

## Features

- **Weather Alerts**: Real-time updates and alerts for coastal regions.
- **SOS Emergency System**: Fishermen can send instant SOS signals with location details.
- **Marine Rescue Dashboard**: Dedicated interface for rescue teams to monitor and respond to SOS signals.
- **Port Management**: Centralized management of coastal ports and rescue teams.
- **Admin Control**: Comprehensive admin dashboard for managing users, ports, and weather alerts.

## Technology Stack

- **Backend**: Django (Python)
- **Database**: SQLite3
- **Frontend**: HTML5, CSS3, JavaScript
- **Icons**: SVG-based system

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/VishnuSuresh0204/Weather-Alert-System.git
   cd Weather-Alert-System
   ```

2. **Set up a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install django
   ```

4. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Start the development server**:
   ```bash
   python manage.py runserver
   ```

## Usage

- **Public**: View public weather alerts and information.
- **Fisherman**: Register/Login to send SOS signals and view personalized weather alerts.
- **Rescue Team**: Specialized access to respond to emergencies.
- **Admin**: Access via `/admin/` or `/admin_home/` to manage the entire system.

## License

This project is open-source and available under the MIT License.
