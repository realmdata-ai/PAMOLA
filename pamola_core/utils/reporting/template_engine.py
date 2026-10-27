"""
Module for working with report templates.

Functions for loading, rendering and copying templates using Jinja2.
"""

import json
import logging
import os
import shutil
from pathlib import Path
from typing import Dict, Any, Optional, List, Union

import jinja2

from pamola_core.utils.reporting.config import (
    get_template_path,
    get_templates_dir,
)
from pamola_core.errors.exceptions import ValidationError

# Logging setup
logger = logging.getLogger(__name__)


def get_jinja_environment(template_name: Optional[str] = None) -> jinja2.Environment:
    """
    Creates and configures the Jinja2 environment.

    Parameters
    -----------
    template_name : str, optional
        Template name (the default template is used if not specified)

    Returns
    --------
    jinja2.Environment
        Configured Jinja2 environment
    """
    template_path = get_template_path(template_name)

    # Check that the template directory exists
    if not template_path.exists():
        logger.warning(f"Template directory not found: {template_path}")
        template_path.mkdir(parents=True, exist_ok=True)

    # Create the file loader
    file_system_loader = jinja2.FileSystemLoader(template_path)

    # Create the environment
    env = jinja2.Environment(
        loader=file_system_loader,
        autoescape=jinja2.select_autoescape(["html", "xml"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )

    # Add custom filters
    env.filters["format_size"] = format_file_size
    env.filters["to_json"] = to_json

    return env


def render_template(
    template_name: str, context: Dict[str, Any], template_dir: Optional[str] = None
) -> str:
    """
    Renders a template with the given context.

    Parameters
    -----------
    template_name : str
        Template file name (e.g. base.html)
    context : Dict[str, Any]
        Rendering context
    template_dir : str, optional
        Template directory name (the default template is used if not specified)

    Returns
    --------
    str
        Rendered HTML markup
    """
    try:
        env = get_jinja_environment(template_dir)
        template = env.get_template(template_name)
        return template.render(**context)
    except jinja2.exceptions.TemplateNotFound:
        logger.error(f"Template not found: {template_name} in directory {template_dir}")
        return f"<p>Error: template {template_name} not found</p>"
    except Exception as e:
        logger.error(f"Error rendering template {template_name}: {e}")
        return f"<p>Error rendering template: {str(e)}</p>"


def copy_static_resources(
    target_dir: Path, template_name: Optional[str] = None
) -> bool:
    """
    Copies the template's static resources (CSS, JS) to the report directory.

    Parameters
    -----------
    target_dir : Path
        Target directory
    template_name : str, optional
        Template name (the default template is used if not specified)

    Returns
    --------
    bool
        True on success, False on error
    """
    template_path = get_template_path(template_name)

    # Copy CSS files
    styles_dir = template_path / "styles"
    if styles_dir.exists():
        target_styles_dir = target_dir / "styles"
        target_styles_dir.mkdir(exist_ok=True)

        for file in styles_dir.glob("*.css"):
            try:
                shutil.copy2(file, target_styles_dir / file.name)
            except Exception as e:
                logger.error(f"Error copying {file.name}: {e}")
                return False

    # Copy JS files
    scripts_dir = template_path / "scripts"
    if scripts_dir.exists():
        target_scripts_dir = target_dir / "scripts"
        target_scripts_dir.mkdir(exist_ok=True)

        for file in scripts_dir.glob("*.js"):
            try:
                shutil.copy2(file, target_scripts_dir / file.name)
            except Exception as e:
                logger.error(f"Error copying {file.name}: {e}")
                return False

    # Copy images
    images_dir = template_path / "images"
    if images_dir.exists():
        target_images_dir = target_dir / "images"
        target_images_dir.mkdir(exist_ok=True)

        for file in images_dir.glob("*.*"):
            try:
                shutil.copy2(file, target_images_dir / file.name)
            except Exception as e:
                logger.error(f"Error copying {file.name}: {e}")
                return False

    return True


def include_external_resources(target_dir: Path) -> bool:
    """
    Downloads and saves external resources (Bootstrap, Chart.js, etc.).

    Parameters
    -----------
    target_dir : Path
        Target directory

    Returns
    --------
    bool
        True on success, False on error
    """
    try:
        import requests

        # Create resource directories
        styles_dir = target_dir / "styles"
        styles_dir.mkdir(exist_ok=True)

        scripts_dir = target_dir / "scripts"
        scripts_dir.mkdir(exist_ok=True)

        # External resources to download
        resources = [
            {
                "url": "https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css",
                "path": styles_dir / "bootstrap.min.css",
            },
            {
                "url": "https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js",
                "path": scripts_dir / "bootstrap.bundle.min.js",
            },
            {
                "url": "https://cdn.jsdelivr.net/npm/chart.js",
                "path": scripts_dir / "chart.min.js",
            },
            {
                "url": "https://cdnjs.cloudflare.com/ajax/libs/d3/7.0.0/d3.min.js",
                "path": scripts_dir / "d3.min.js",
            },
            {
                "url": "https://cdnjs.cloudflare.com/ajax/libs/dagre-d3/0.6.4/dagre-d3.min.js",
                "path": scripts_dir / "dagre-d3.min.js",
            },
        ]

        # Download each resource
        for resource in resources:
            response = requests.get(resource["url"], timeout=10)

            if response.status_code == 200:
                with open(resource["path"], "wb") as f:
                    f.write(response.content)
                logger.info(f"Downloaded resource: {resource['url']}")
            else:
                logger.error(
                    f"Error downloading resource {resource['url']}: {response.status_code}"
                )
                return False

        return True
    except ImportError:
        logger.warning(
            "The requests module is not installed. Cannot include external resources."
        )
        return False
    except Exception as e:
        logger.error(f"Error including external resources: {e}")
        return False


def check_template_exists(template_name: Optional[str] = None) -> bool:
    """
    Checks whether a template exists.

    Parameters
    -----------
    template_name : str, optional
        Template name (the default template is used if not specified)

    Returns
    --------
    bool
        True if the template exists and contains the required files
    """
    template_path = get_template_path(template_name)

    # Check for the template's core files
    required_files = ["base.html", "partials/header.html", "partials/sidebar.html"]

    for file in required_files:
        if not (template_path / file).exists():
            return False

    return True


def initialize_template(template_name: str) -> bool:
    """
    Initializes a template by copying the standard files into the template directory.

    Parameters
    -----------
    template_name : str
        Name of the new template

    Returns
    --------
    bool
        True on success, False on error
    """
    try:
        template_path = get_template_path(template_name)
        default_template_path = get_template_path("default")

        # If the directory already exists and is not empty, do not overwrite it
        if template_path.exists() and any(template_path.iterdir()):
            logger.warning(
                f"Template directory {template_name} already exists and is not empty"
            )
            return False

        # If the default directory does not exist, create it and the base files
        if not default_template_path.exists():
            logger.warning("Default template directory does not exist, creating it...")
            create_default_template()

        # Copy files from the default template
        for item in default_template_path.glob("**/*"):
            if item.is_file():
                # Build the relative path
                rel_path = item.relative_to(default_template_path)
                # Build the target path
                target_path = template_path / rel_path
                # Create the parent directory if it does not exist
                target_path.parent.mkdir(parents=True, exist_ok=True)
                # Copy the file
                shutil.copy2(item, target_path)

        logger.info(f"Template {template_name} initialized")
        return True
    except Exception as e:
        logger.error(f"Error initializing template {template_name}: {e}")
        return False


def list_available_templates() -> List[str]:
    """
    Gets the list of available templates.

    Returns
    --------
    List[str]
        List of available template names
    """
    templates_dir = get_templates_dir()

    # Collect the subdirectories of the templates directory
    templates = []
    for item in templates_dir.iterdir():
        if item.is_dir() and check_template_exists(item.name):
            templates.append(item.name)

    return templates


def create_default_template() -> bool:
    """
    Creates the default template with base files.

    Returns
    --------
    bool
        True on success, False on error
    """
    try:
        template_path = get_template_path("default")

        # Create the directory structure
        dirs = [
            template_path,
            template_path / "partials",
            template_path / "styles",
            template_path / "scripts",
            template_path / "images",
        ]

        for directory in dirs:
            directory.mkdir(parents=True, exist_ok=True)

        # The base template files could be created here
        # That would require a substantial amount of code
        # In a real application these files could be loaded from package resources

        return True
    except Exception as e:
        logger.error(f"Error creating default template: {e}")
        return False


def format_file_size(size_bytes: int) -> str:
    """
    Formats a file size in human-readable form.

    Parameters
    -----------
    size_bytes : int
        Size in bytes

    Returns
    --------
    str
        Formatted size string
    """
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.1f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"


def to_json(data: Any) -> str:
    """
    Converts data to a JSON string.

    Parameters
    -----------
    data : Any
        Data to convert

    Returns
    --------
    str
        JSON string
    """
    return json.dumps(data, ensure_ascii=False)


def create_empty_report(output_path: Path, title: str = "Empty Report") -> bool:
    """
    Creates an empty report for cases where there is no data.

    Parameters
    -----------
    output_path : Path
        Path to save the report to
    title : str
        Report title

    Returns
    --------
    bool
        True on success, False on error
    """
    try:
        context = {
            "title": title,
            "timestamp": "",
            "tasks": [],
            "tasks_by_category": {},
            "has_dependencies": False,
            "dependency_data": "{}",
        }

        html = render_template("base.html", context)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)

        return True
    except Exception as e:
        logger.error(f"Error creating empty report: {e}")
        return False


def get_relative_artifact_path(
    artifact_path: Union[str, Path], html_report_dir: Path
) -> str:
    """
    Computes the artifact path relative to the report directory.

    Parameters
    -----------
    artifact_path : str or Path
        Absolute path to the artifact
    html_report_dir : Path
        Path to the report directory

    Returns
    --------
    str
        Relative path to the artifact
    """
    artifact_path = Path(artifact_path)

    try:
        # Try to compute the relative path
        rel_path = os.path.relpath(artifact_path, html_report_dir)
        return rel_path.replace("\\", "/")  # For URL compatibility in HTML
    except (ValidationError, ValueError):
        # On error (e.g. different drives on Windows)
        logger.warning(f"Failed to compute a relative path for {artifact_path}")
        return str(artifact_path)
