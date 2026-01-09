# Fleet Dashboard - Solar Energy Monitoring Platform

## Phase 1: Core Layout, Header & Navigation ✅
- [x] Create dark-themed base layout with sidebar navigation
- [x] Build top header with site name, date range pickers, and weather display
- [x] Add site info bar (AC/DC capacity, lat/lon, status badges, client, inception date)
- [x] Implement tab navigation (Executive Summary, Priority View, Equipment Heatmap)
- [x] Set up state management for data loading and active tab selection

## Phase 2: Executive Summary Tab with KPI Cards & Charts ✅
- [x] Build Operational Summary section with Performance, Availability, Contractual Availability, Potential LDs cards
- [x] Add Energy metrics grid (Measured Energy, Modeled Energy, Modeled/Measured Insolation)
- [x] Create Expected Energy, Curtailed Energy, Total Lost Energy, Excused Energy cards
- [x] Build Primary Loss Drivers panel with MWh/% toggle
- [x] Add Energy Waterfall & Loss Profile chart (waterfall visualization)
- [x] Create dynamic performance summary text block

## Phase 3: Priority View, Equipment Heatmap & Key Metrics ✅
- [x] Build Outstanding Issues cards (Inverter, Transformer, Breaker, Tracker Controller counts)
- [x] Create High Frequency Equipment Failures table with sorting
- [x] Build Open Work Orders table with status indicators
- [x] Implement Equipment Heatmap tab with inverter/tracker/transformer grid visualizations
- [x] Add heatmap statistics cards (Total Failures, Most Problematic, Avg Failures/Unit)
- [x] Create Key Metrics Overview table with site data and expandable rows

## Phase 4: Fleet Dashboard Overview Page ✅
- [x] Create new Fleet Overview page as the main landing page with route "/"
- [x] Build fleet-level KPI cards (Total Sites, Availability %, Performance %, Total Measured Energy, Total Lost Energy)
- [x] Add Site Distribution donut chart (Critical/Warning/Healthy breakdown)
- [x] Add Fleet Loss Breakdown donut chart (Derated/Plant Offline/Inverters Offline/Underperforming)
- [x] Build enhanced Key Metrics table with all sites, sortable columns, and search
- [x] Add site name click to navigate to individual site dashboards
- [x] Move existing site dashboard to "/site/[site_name]" route

## Phase 5: Enhanced Fleet Dashboard & Data Integration ✅
- [x] Add SAN DIEGO, CA weather widget with temperature (14°C) and conditions
- [x] Add FROM/TO date picker in header with FILTERS button
- [x] Build complete sidebar navigation with MONITORING & ANALYTICS and SYSTEM sections
- [x] Generate 64 sites with random data for demonstration
- [x] Show donut chart values outside chart (14 Critical, 12 Warning, 38 Healthy)
- [x] Make site rows clickable with hover effects and zap icon
- [x] Add search functionality for Key Metrics table