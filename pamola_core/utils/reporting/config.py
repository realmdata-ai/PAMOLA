"""
Configuration module for the reporting system.

Functions for working with the project configuration and report settings.
"""
import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List

# Logging setup
logger = logging.getLogger(__name__)

# Default values
DEFAULT_CONFIG = {
    "project": {
        "name": "PAMOLA.CORE (Privacy-Preserving AI Data Processors) Anonymization",
        "description": "Analysis and anonymization of resume data for de-identification",
        "version": "1.0.0",
        "created": datetime.now().strftime("%Y-%m-%d"),
        "updated": datetime.now().strftime("%Y-%m-%d")
    },
    "reporting": {
        "default_template": "default",
        "auto_open": True,
        "include_resources": False
    },
    "task_flow": {
        "dependencies": {}
    }
}


def get_config_path() -> Path:
    """
    Gets the path to the project configuration file.

    Returns
    --------
    Path
        Path to the configuration file
    """
    # Check the environment variable first
    if os.environ.get("PAMOLA_CONFIG_PATH"):
        return Path(os.environ["PAMOLA_CONFIG_PATH"])

    # Search the standard locations
    config_search_paths = [
        Path("prj_config.json"),
        Path("configs/prj_config.json"),
        Path("config/prj_config.json"),
        Path(os.path.expanduser("~")) / ".pamola_core" / "config.json"
    ]

    # Check the current project directory
    try:
        from pamola_core.utils.io import get_data_repository
        repo_dir = get_data_repository()
        config_search_paths.insert(0, repo_dir / "configs" / "prj_config.json")
    except (ImportError, Exception):
        logger.warning("Failed to get the data repository directory")

    # Look for the configuration in the listed locations
    for path in config_search_paths:
        if path.exists():
            return path

    # Return the default path if nothing was found
    return Path("prj_config.json")


def load_config() -> Dict[str, Any]:
    """
    Loads the project configuration.

    Returns
    --------
    Dict[str, Any]
        Dictionary with the project configuration
    """
    config_path = get_config_path()

    if not config_path.exists():
        logger.warning(f"Configuration file not found: {config_path}. Using default settings.")
        return DEFAULT_CONFIG

    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)

        # Add missing sections from the default configuration
        for section, defaults in DEFAULT_CONFIG.items():
            if section not in config:
                config[section] = defaults
            elif isinstance(defaults, dict):
                for key, value in defaults.items():
                    if key not in config[section]:
                        config[section][key] = value

        return config
    except Exception as e:
        logger.error(f"Error loading configuration: {e}")
        return DEFAULT_CONFIG


def save_config(config: Dict[str, Any]) -> bool:
    """
    Saves the project configuration.

    Parameters
    -----------
    config : Dict[str, Any]
        Configuration to save

    Returns
    --------
    bool
        True on success, False on error
    """
    config_path = get_config_path()

    try:
        # Update the modification date
        if "project" in config:
            config["project"]["updated"] = datetime.now().strftime("%Y-%m-%d")

        # Create the directory if it does not exist
        config_path.parent.mkdir(parents=True, exist_ok=True)

        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2) # type: ignore

        logger.info(f"Configuration saved to {config_path}")
        return True
    except Exception as e:
        logger.error(f"Error saving configuration: {e}")
        return False


def update_project_metadata(name: Optional[str] = None,
                            description: Optional[str] = None,
                            version: Optional[str] = None) -> bool:
    """
    Updates the project metadata in the configuration.

    Parameters
    -----------
    name : str, optional
        Project name
    description : str, optional
        Project description
    version : str, optional
        Project version

    Returns
    --------
    bool
        True on success, False on error
    """
    config = load_config()

    if "project" not in config:
        config["project"] = DEFAULT_CONFIG["project"]

    if name is not None:
        config["project"]["name"] = name

    if description is not None:
        config["project"]["description"] = description

    if version is not None:
        config["project"]["version"] = version

    # Update the modification date
    config["project"]["updated"] = datetime.now().strftime("%Y-%m-%d")

    return save_config(config)


def get_reporting_settings() -> Dict[str, Any]:
    """
    Gets the reporting system settings.

    Returns
    --------
    Dict[str, Any]
        Dictionary with the reporting settings
    """
    config = load_config()

    if "reporting" not in config:
        return DEFAULT_CONFIG["reporting"]

    # Ensure all required settings are present
    for key, value in DEFAULT_CONFIG["reporting"].items():
        if key not in config["reporting"]:
            config["reporting"][key] = value

    return config["reporting"]


def update_reporting_settings(template: Optional[str] = None,
                              auto_open: Optional[bool] = None,
                              include_resources: Optional[bool] = None) -> bool:
    """
    Updates the reporting system settings.

    Parameters
    -----------
    template : str, optional
        Name of the default report template
    auto_open : bool, optional
        Whether to open the report automatically after it is created
    include_resources : bool, optional
        Whether to include resources in the report

    Returns
    --------
    bool
        True on success, False on error
    """
    config = load_config()

    if "reporting" not in config:
        config["reporting"] = DEFAULT_CONFIG["reporting"]

    if template is not None:
        config["reporting"]["default_template"] = template

    if auto_open is not None:
        config["reporting"]["auto_open"] = auto_open

    if include_resources is not None:
        config["reporting"]["include_resources"] = include_resources

    return save_config(config)


def get_task_dependencies() -> Dict[str, List[str]]:
    """
    Gets task dependencies from the configuration.

    Returns
    --------
    Dict[str, List[str]]
        Dictionary {task: [dependencies]}
    """
    config = load_config()

    if "task_flow" not in config or "dependencies" not in config["task_flow"]:
        return {}

    return config["task_flow"]["dependencies"]


def update_task_dependencies(dependencies: Dict[str, List[str]]) -> bool:
    """
    Updates task dependencies in the configuration.

    Parameters
    -----------
    dependencies : Dict[str, List[str]]
        Dictionary {task: [dependencies]}

    Returns
    --------
    bool
        True on success, False on error
    """
    config = load_config()

    if "task_flow" not in config:
        config["task_flow"] = DEFAULT_CONFIG["task_flow"]

    config["task_flow"]["dependencies"] = dependencies

    return save_config(config)


def add_task_dependency(task_id: str, dependency_id: str) -> bool:
    """
    Adds a dependency between tasks.

    Parameters
    -----------
    task_id : str
        Identifier of the dependent task
    dependency_id : str
        Identifier of the task it depends on

    Returns
    --------
    bool
        True on success, False on error
    """
    dependencies = get_task_dependencies()

    if task_id not in dependencies:
        dependencies[task_id] = []

    if dependency_id not in dependencies[task_id]:
        dependencies[task_id].append(dependency_id)

    return update_task_dependencies(dependencies)


def remove_task_dependency(task_id: str, dependency_id: str) -> bool:
    """
    Removes a dependency between tasks.

    Parameters
    -----------
    task_id : str
        Identifier of the dependent task
    dependency_id : str
        Identifier of the task it depends on

    Returns
    --------
    bool
        True on success, False on error
    """
    dependencies = get_task_dependencies()

    if task_id not in dependencies:
        return True

    if dependency_id in dependencies[task_id]:
        dependencies[task_id].remove(dependency_id)

    return update_task_dependencies(dependencies)


def get_templates_dir() -> Path:
    """
    Gets the report templates directory.

    Returns
    --------
    Path
        Path to the templates directory
    """
    try:
        from pamola_core.utils.io import get_data_repository
        repo_dir = get_data_repository()
        templates_dir = repo_dir / "templates"
    except (ImportError, Exception):
        logger.warning("Failed to get the data repository directory. Using the current directory.")
        templates_dir = Path("data/templates")

    if not templates_dir.exists():
        templates_dir.mkdir(parents=True, exist_ok=True)

    return templates_dir


def get_template_path(template_name: Optional[str] = None) -> Path:
    """
    Gets the path to a report template.

    Parameters
    -----------
    template_name : str, optional
        Template name (the default template is used if not specified)

    Returns
    --------
    Path
        Path to the template directory
    """
    if template_name is None:
        settings = get_reporting_settings()
        template_name = settings["default_template"]

    template_dir = get_templates_dir() / template_name

    if not template_dir.exists():
        template_dir.mkdir(parents=True, exist_ok=True)

    return template_dir


def get_reports_dir() -> Path:
    """
    Gets the directory for storing reports.

    Returns
    --------
    Path
        Path to the reports directory
    """
    try:
        from pamola_core.utils.io import get_data_repository
        repo_dir = get_data_repository()
        reports_dir = repo_dir / "reports" / "html"
    except (ImportError, Exception):
        logger.warning("Failed to get the data repository directory. Using the current directory.")
        reports_dir = Path("data/reports/html")

    if not reports_dir.exists():
        reports_dir.mkdir(parents=True, exist_ok=True)

    return reports_dir


def detect_task_type(task_id: str) -> str:
    """
    Determines the task type from its identifier.

    Parameters
    -----------
    task_id : str
        Task identifier

    Returns
    --------
    str
        Task type (profiling, cleaning, anonymization, etc.)
    """
    task_types = {
        "profile": "Profiling",
        "clean": "Cleaning",
        "anonymize": "Anonymization",
        "evaluate": "Evaluation",
        "transform": "Transformation",
        "export": "Export",
        "import": "Import",
        "test": "Testing"
    }

    for prefix, task_type in task_types.items():
        if task_id.startswith(prefix) or f"_{prefix}" in task_id:
            return task_type

    # Special cases
    if "ident" in task_id or "identification" in task_id:
        return "Profiling"
    elif "details" in task_id:
        return "Profiling"
    elif "contacts" in task_id:
        return "Profiling"

    # Default
    return "Other"


def categorize_tasks(task_ids: List[str]) -> Dict[str, List[str]]:
    """
    Categorizes tasks by type.

    Parameters
    -----------
    task_ids : List[str]
        List of task identifiers

    Returns
    --------
    Dict[str, List[str]]
        Dictionary {category: [tasks]}
    """
    categories = {}

    for task_id in task_ids:
        task_type = detect_task_type(task_id)

        if task_type not in categories:
            categories[task_type] = []

        categories[task_type].append(task_id)

    return categories