"""
Module for creating HTML reports.

Functions for creating HTML reports from task reports.
"""
import json
import logging
import os
import webbrowser
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, Union, Tuple

from pamola_core.utils.reporting.config import (
    get_reports_dir,
    get_reporting_settings,
    categorize_tasks,
)
from pamola_core.utils.reporting.dependency_graph import (
    enrich_tasks_with_dependencies,
    create_dependency_graph_data,
    check_missing_dependencies,
)
from pamola_core.utils.reporting.template_engine import (
    render_template,
    copy_static_resources,
    include_external_resources,
    get_relative_artifact_path,
)

# Logging setup
logger = logging.getLogger(__name__)


def prepare_task_reports(task_reports: Dict[str, Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    """
    Prepares task reports for display.

    Parameters
    -----------
    task_reports : Dict[str, Dict[str, Any]]
        Dictionary {task_id: report}

    Returns
    --------
    Dict[str, Dict[str, Any]]
        Prepared report dictionary
    """
    # Enrich reports with dependencies
    enriched_reports = enrich_tasks_with_dependencies(task_reports)

    # Check for missing dependencies
    missing_deps = check_missing_dependencies(enriched_reports)

    # Add information about missing dependencies
    for task_id, missing in missing_deps.items():
        if task_id in enriched_reports:
            enriched_reports[task_id]["missing_dependencies"] = missing

    return enriched_reports


def prepare_artifacts_for_report(task_reports: Dict[str, Dict[str, Any]],
                                 report_dir: Path) -> Dict[str, Dict[str, Any]]:
    """
    Prepares artifacts for the report by adding relative paths.

    Parameters
    -----------
    task_reports : Dict[str, Dict[str, Any]]
        Dictionary {task_id: report}
    report_dir : Path
        Report directory

    Returns
    --------
    Dict[str, Dict[str, Any]]
        Prepared report dictionary
    """
    for task_id, report in task_reports.items():
        if "artifacts" in report:
            for artifact in report["artifacts"]:
                # Add the relative path to the artifact
                artifact_path = artifact.get("path")
                if artifact_path:
                    artifact["relative_path"] = get_relative_artifact_path(artifact_path, report_dir)

                # If this is JSON, render a preview
                if artifact.get("type") == "json" and os.path.exists(artifact.get("path", "")):
                    try:
                        with open(artifact["path"], 'r', encoding='utf-8') as f:
                            data = json.load(f)

                        # Create an HTML preview for the JSON
                        preview = create_json_preview(data)
                        artifact["preview"] = preview
                    except Exception as e:
                        logger.warning(f"Failed to create a preview for {artifact['path']}: {e}")

    return task_reports


def create_json_preview(data: Any, max_depth: int = 2) -> str:
    """
    Creates an HTML preview of JSON data.

    Parameters
    -----------
    data : Any
        JSON data
    max_depth : int
        Maximum nesting depth to display

    Returns
    --------
    str
        Preview HTML markup
    """
    html = ['<div class="json-preview">']

    def _process_item(item, depth=0):
        indent = '  ' * depth

        if isinstance(item, dict):
            if depth >= max_depth:
                return f"{indent}{{...}}"

            result = []
            for key, value in item.items():
                if isinstance(value, (dict, list, tuple)) and depth == max_depth - 1:
                    result.append(f"{indent}<strong>{key}</strong>: {{...}}")
                else:
                    processed_value = _process_item(value, depth + 1)
                    result.append(f"{indent}<strong>{key}</strong>: {processed_value}")

            return "{\n" + ",\n".join(result) + f"\n{indent}}}"

        elif isinstance(item, (list, tuple)):
            if depth >= max_depth:
                return f"{indent}[...]"

            result = []
            for value in item[:5]:  # Limit the number of items
                processed_value = _process_item(value, depth + 1)
                result.append(processed_value)

            if len(item) > 5:
                result.append(f"{indent}...")

            return "[\n" + ",\n".join([f"{indent}{val}" for val in result]) + f"\n{indent}]"

        elif isinstance(item, str):
            return f'"{item}"'

        elif item is None:
            return "null"

        else:
            return str(item)

    html.append(_process_item(data))
    html.append('</div>')

    return ''.join(html)


def create_dashboard_data(task_reports: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    """
    Creates data for the dashboard.

    Parameters
    -----------
    task_reports : Dict[str, Dict[str, Any]]
        Dictionary {task_id: report}

    Returns
    --------
    Dict[str, Any]
        Dashboard data
    """
    # Status statistics
    status_count = {
        "completed": 0,
        "failed": 0,
        "running": 0,
        "other": 0
    }

    # Total number of artifacts
    total_artifacts = 0
    artifacts_by_type = {}

    # Total execution time
    total_execution_time = 0

    # Total number of operations
    total_operations = 0
    operations_by_status = {
        "success": 0,
        "error": 0,
        "warning": 0,
        "other": 0
    }

    # Task categorization
    tasks_by_category = categorize_tasks(list(task_reports.keys()))

    # Process each report
    for task_id, report in task_reports.items():
        # Status
        status = report.get("status", "other")
        if status in status_count:
            status_count[status] += 1
        else:
            status_count["other"] += 1

        # Artifacts
        artifacts = report.get("artifacts", [])
        total_artifacts += len(artifacts)

        for artifact in artifacts:
            artifact_type = artifact.get("type", "other")
            artifacts_by_type[artifact_type] = artifacts_by_type.get(artifact_type, 0) + 1

        # Execution time
        execution_time = report.get("execution_time_seconds", 0)
        if execution_time:
            total_execution_time += execution_time

        # Operations
        operations = report.get("operations", [])
        total_operations += len(operations)

        for operation in operations:
            operation_status = operation.get("status", "other")
            if operation_status in operations_by_status:
                operations_by_status[operation_status] += 1
            else:
                operations_by_status["other"] += 1

    return {
        "status_count": status_count,
        "total_tasks": len(task_reports),
        "total_artifacts": total_artifacts,
        "artifacts_by_type": artifacts_by_type,
        "total_execution_time": total_execution_time,
        "total_operations": total_operations,
        "operations_by_status": operations_by_status,
        "tasks_by_category": tasks_by_category
    }


def create_html_report(task_reports: Dict[str, Dict[str, Any]],
                       output_path: Optional[Path] = None,
                       template_name: Optional[str] = None) -> Tuple[Path, bool]:
    """
    Creates an HTML report from task reports.

    Parameters
    -----------
    task_reports : Dict[str, Dict[str, Any]]
        Dictionary {task_id: report}
    output_path : Path, optional
        Path to save the report to (the default path is used if not specified)
    template_name : str, optional
        Template name (the default template is used if not specified)

    Returns
    --------
    Tuple[Path, bool]
        Path to the created report and a success flag
    """
    # If no path is given, use the default directory
    if output_path is None:
        reports_dir = get_reports_dir()
        output_path = reports_dir / f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"

    # Create the report directory if it does not exist
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Get the reporting settings
    settings = get_reporting_settings()

    # If no template is given, use the default template
    if template_name is None:
        template_name = settings.get("default_template", "default")

    try:
        # Prepare the reports
        prepared_reports = prepare_task_reports(task_reports)

        # Prepare the artifacts
        prepared_reports = prepare_artifacts_for_report(prepared_reports, output_path.parent)

        # Create the dashboard data
        dashboard_data = create_dashboard_data(prepared_reports)

        # Categorize the tasks
        tasks_by_category = dashboard_data["tasks_by_category"]

        # Create the dependency graph data
        dependency_data = create_dependency_graph_data(prepared_reports)

        # Check for local resources and try to download them if needed
        include_resources = settings.get("include_resources", False)
        resource_files_exist = False

        if include_resources:
            # Try to copy the static resources
            copy_static_resources(output_path.parent, template_name)

            # Define the required resource files
            required_resources = [
                output_path.parent / "scripts" / "bootstrap.bundle.min.js",
                output_path.parent / "scripts" / "chart.min.js",
                output_path.parent / "scripts" / "d3.min.js",
                output_path.parent / "scripts" / "dagre-d3.min.js"
            ]

            # Check that all resources are present
            missing_resources = [res for res in required_resources if not res.exists()]

            if missing_resources:
                logger.info("Some local resources are missing. Downloading them...")
                include_external_resources(output_path.parent)

                # Check again after downloading
                missing_resources = [res for res in required_resources if not res.exists()]
                resource_files_exist = len(missing_resources) == 0

                if not resource_files_exist:
                    logger.warning("Unable to download all required resources. CDN links will be used.")
            else:
                resource_files_exist = True

        # Build the template context
        context = {
            "title": "Project Report: PAMOLA.CORE (Privacy-Preserving AI Data Processors) - Data Anonymization",
            "page_title": "Project Report",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "tasks": list(prepared_reports.values()),
            "tasks_by_category": {category: [prepared_reports[task_id] for task_id in tasks]
                                  for category, tasks in tasks_by_category.items()},
            "has_dependencies": bool(dependency_data["edges"]),
            "dependency_data": json.dumps(dependency_data),
            "dashboard": dashboard_data,
            "project_info": {
                "name": "PAMOLA.CORE (Privacy-Preserving AI Data Processors) - Data Anonymization",
                "description": "Analysis and anonymization of resume data for de-identification",
                "version": "1.0.0",
                "created": datetime.now().strftime("%Y-%m-%d"),
                "updated": datetime.now().strftime("%Y-%m-%d")
            },
            "include_resources": include_resources,
            "resource_files_exist": resource_files_exist  # Add the resource-availability flag to the context
        }

        # Render the template
        html = render_template("base.html", context, template_name)

        # Save the HTML
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)

        logger.info(f"HTML report created: {output_path}")

        # Open the report in the browser if the settings say so
        if settings.get("auto_open", True):
            webbrowser.open(f"file://{output_path}")

        return output_path, True
    except Exception as e:
        logger.error(f"Error creating HTML report: {e}")
        return output_path, False


def load_task_report(report_path: Union[str, Path]) -> Dict[str, Any]:
    """
    Loads a task report from a JSON file.

    Parameters
    -----------
    report_path : str or Path
        Path to the report file

    Returns
    --------
    Dict[str, Any]
        The loaded report, or an empty dictionary on error
    """
    try:
        with open(report_path, "r", encoding="utf-8") as f:
            report = json.load(f)
        return report
    except Exception as e:
        logger.error(f"Error loading report {report_path}: {e}")
        return {}


def load_all_task_reports(reports_dir: Optional[Path] = None) -> Dict[str, Dict[str, Any]]:
    """
    Loads all task reports from a directory.

    Parameters
    -----------
    reports_dir : Path, optional
        Path to the reports directory (the default directory is used if not specified)

    Returns
    --------
    Dict[str, Dict[str, Any]]
        Dictionary {task_id: report}
    """
    if reports_dir is None:
        # Use the directory from the data repository
        try:
            from pamola_core.utils.io import get_data_repository
            repo_dir = get_data_repository()
            reports_dir = repo_dir / "reports"
        except (ImportError, Exception):
            logger.warning("Failed to get the data repository directory. Using the current directory.")
            reports_dir = Path("data/reports")

    # Check that the directory exists
    if not reports_dir.exists():
        logger.warning(f"Reports directory not found: {reports_dir}")
        return {}

    # Load all reports
    task_reports = {}

    for report_file in reports_dir.glob("*_report.json"):
        try:
            # Extract the task identifier from the file name
            task_id = report_file.stem.split("_")[0]

            # Load the report
            report = load_task_report(report_file)

            if report:
                task_reports[task_id] = report
        except Exception as e:
            logger.error(f"Error processing file {report_file}: {e}")

    return task_reports