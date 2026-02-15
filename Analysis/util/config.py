# ============================================================================
# Visualization Configuration
# ============================================================================

# Color Palette
COLORS_3 = ["#4C78A8", "#F58518", "#54A24B"]
COLORS_4 = ["#4C78A8", "#F58518", "#54A24B", "#B279A2"]

# Three-Level Chart Colors (increasing complexity)
COLORS_BUILD_RUN_EXPLOIT = ["#54A24B", "#F58518", "#E45756"]  # Green, Orange, Red

# Figure Sizes (width, height)
FIGURE_SIZE_WIDE = (9, 5)
FIGURE_SIZE_MEDIUM = (7.5, 5)
FIGURE_SIZE_PLOT = (7, 5)
FIGURE_SIZE_BOX = (6.5, 4.8)

# Bar and Chart Settings
BAR_WIDTH = 0.18
GROUP_SPACING = 0.4
BAR_ALPHA = 0.8
SCATTER_ALPHA = 0.8
SCATTER_EDGE_COLOR = "black"
SCATTER_EDGE_WIDTH = 0.3
HIST_ALPHA = 0.6

# Font and Text Settings
FONT_FAMILY = "serif"
FONT_SERIF = ["Times New Roman", "Times", "DejaVu Serif"]
FONT_TITLE_SIZE = 14
FONT_AXES_LABEL_SIZE = 16
FONT_TICK_SIZE = 16
FONT_LEGEND_SIZE = 14
FONT_DATA_LABEL_SIZE = 10

# Legend Settings
LEGEND_COLUMNS_DEFAULT = 2
LEGEND_COLUMNS_SCATTER = 2
LEGEND_TICKER_SIZE = 8

# Boxplot Settings
BOXPLOT_SHOW_FLIERS = True

# Histogram Settings
HISTOGRAM_BINS = 12

# ============================================================================
# Default Titles
# ============================================================================

TITLE_FUNCTIONAL_SUCCESS = "Functional Success by Type and Dataset"
TITLE_IMPACT_VS_AUTOMATION = "TotalImpact vs TotalAutomation per CVE"
TITLE_PAIRED_DELTA = "Figure 6 — Paired Comparison (Differential Effort)"
TITLE_BOXPLOT_IMPACT = "TotalImpact by Type"
TITLE_BOXPLOT_AUTOMATION = "TotalAutomation by Type"
TITLE_OVERALL_SUCCESS = "Figure 1 — Overall Functional Success Rates"
TITLE_SERVICES_SUCCESS = "Figure 2a — Functional Success for Services"
TITLE_WEB_SUCCESS = "Figure 2b — Functional Success for Web Applications"
TITLE_CHANGECLASS_IMPACT = "Figure 3 — Distribution of Change Impact Classes"
TITLE_AUTOMATION_CHALLENGE = "Figure 4 — Distribution of Automation Challenge Classes"
TITLE_ERROR_CATEGORY_STAGE = "Figure 7 — Error Taxonomy and Frequency by Stage"

# ============================================================================
# Figure Filenames
# ============================================================================

# Main paper figures
OVERALL_SUCCESS_FIGURE = "fig_results_overall_success.png"
SERVICES_SUCCESS_FIGURE = "fig_results_services_success.png"
WEB_SUCCESS_FIGURE = "fig_results_web_success.png"
CHANGECLASS_IMPACT_FIGURE = "fig_results_changeclass_impact_distribution.png"
AUTOMATION_CHALLENGE_FIGURE = "fig_results_automation_challenge_distribution.png"
IMPACT_VS_AUTOMATION_FIGURE = "fig_results_impact_vs_automation_scatter.png"
PAIRED_DELTA_FIGURE = "fig_results_paired_delta_histogram.png"
ERROR_CATEGORY_BUILD_FIGURE = "fig_results_error_category_build.png"
ERROR_CATEGORY_RUN_FIGURE = "fig_results_error_category_run.png"
ERROR_CATEGORY_EXPLOIT_FIGURE = "fig_results_error_category_exploit.png"

# Auxiliary figures
FUNCTIONAL_SUCCESS_FIGURE = "fig_aux_functional_success_by_type.png"
CHANGECLASS_DISTRIBUTION_FIGURE = "fig_aux_changeclass_distribution_by_type.png"
AUTOMATION_DISTRIBUTION_FIGURE = "fig_aux_automation_distribution_by_type.png"
BOXPLOT_IMPACT_FIGURE = "fig_aux_boxplot_totalimpact_by_type.png"
BOXPLOT_AUTOMATION_FIGURE = "fig_aux_boxplot_totalautomation_by_type.png"

# ============================================================================
# Changeclass and Automation Weights
# ============================================================================

CHANGECLASS_WEIGHTS = {"c0": 1, "c1": 2, "c2": 6}
CHANGECLASS_COLORS = {"c0": "#54A24B", "c1": "#F58518", "c2": "#E45756"}  # Green, Orange, Red
AUTOMATION_WEIGHTS = {"a0": 0, "a1": 1, "a2": 2}
AUTOMATION_COLORS = {"a0": "#54A24B", "a1": "#F58518", "a2": "#E45756"}  # Green, Orange, Red

GREEN_COLOR = "#54A24B"
ORANGE_COLOR = "#F58518"
RED_COLOR = "#E45756"

# ============================================================================
# BAR CHART CONFIGURATION
# ============================================================================

GAP_BETWEEN_GROUPS = 0.9