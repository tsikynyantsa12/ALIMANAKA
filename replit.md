# Alimanaka - Liturgical and Agricultural Calendar Generator

## Overview

This project is a professional PDF calendar generator for the Malagasy Lutheran Church (Fiangonana Loterana Malagasy). It produces A3 landscape format calendars combining liturgical information, agricultural activities, and lunar phases for the year 2025-2026.

The calendar displays:
- **Liturgical data**: Colors, Sunday names, biblical readings
- **Agricultural data**: Crop icons (rice, cassava, beans, corn) with action indicators (sowing, maintenance, harvest)
- **Astronomical data**: Precise lunar phases
- **Events**: Church programs and public holidays

The output is a 2-page PDF with 6 months per page, featuring a Luther Rose color palette and wave decorations.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Project Structure
The codebase follows a modular architecture separating concerns:

```
├── main.py              # Entry point - PDF generation orchestration
├── config/              # Configuration modules
│   ├── colors.py        # Color definitions (Luther Rose palette, liturgical colors)
│   ├── fonts.py         # Typography settings (font families, sizes)
│   └── page.py          # Page dimensions (A3 landscape, margins, spacing)
├── data/                # CSV data files
│   ├── global/          # Shared lookup tables (colors, cultures, actions, phases)
│   └── mois/            # Month-specific data (01-12 folders)
├── layout/              # Rendering components
│   ├── day_row.py       # Individual day row rendering logic
│   ├── header.py        # Page header rendering
│   ├── month_block.py   # Month column layout
│   └── page_block.py    # Full page composition
├── utils/               # Helper utilities
│   ├── csv_loader.py    # Data loading from CSV files
│   ├── date_utils.py    # Date calculations and French weekday names
│   └── icon_mapper.py   # Icon path resolution for lunar/agricultural icons
├── assets/              # Static resources
│   ├── images/          # Logos (church, agriculture)
│   └── icons/           # Icon files (lunar phases, crops, actions)
└── output/              # Generated PDF output directory
```

### Design Patterns

**Data-Driven Design**: All calendar content (events, colors, phases) is stored in CSV files, enabling non-technical users to update content without code changes. The system synchronizes IDs between global lookup tables and monthly data files.

**Component-Based Rendering**: Layout modules are separated by visual component (header, month block, day row), allowing independent testing and modification of each calendar section.

**Configuration Separation**: Visual settings (colors, fonts, page dimensions) are isolated in the `config/` directory, making theme changes straightforward.

### PDF Generation Approach

The project uses ReportLab's canvas-based approach for precise control over layout positioning. Key rendering features:
- Full-page HD background images with minimal overlay
- Wave decorations using mathematical sine functions
- Dynamic row height calculation based on content
- Liturgical color coding via left border indicators

### Data Flow

1. `main.py` loads global data (colors, icons) and iterates through months
2. For each month, `csv_loader.py` retrieves month-specific CSV data
3. `date_utils.py` generates day information for the month
4. `day_row.py` calculates heights and renders each day with appropriate styling
5. Icons are resolved through `icon_mapper.py` which maps IDs to file paths

## External Dependencies

### Python Libraries
- **ReportLab** (`reportlab`): Core PDF generation library using canvas and platypus modules
- **Pandas** (`pandas`): CSV data loading and manipulation
- **Pillow** (`pillow`): Image processing for logos and icons

### File-Based Data Sources
- CSV files in `data/global/` for lookup tables (liturgical colors, crop types, lunar phases)
- CSV files in `data/mois/XX/` for monthly content (Sunday readings, church programs, agricultural schedules)

### Static Assets
- Logo images: `assets/images/logo_eglise.png`, `assets/images/logo_agri.png`
- Icon sets: `assets/icons/` containing PNG files for lunar phases, crops, and agricultural actions

### Runtime Requirements
- Python 3.10+ (configured for 3.11 in pyrightconfig.json)
- No external APIs or database connections required
- All data is file-based within the repository