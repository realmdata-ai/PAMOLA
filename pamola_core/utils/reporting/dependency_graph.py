"""
Module for working with task dependencies.

Functions for analyzing, validating and visualizing dependencies between tasks.
"""
import logging
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional

from pamola_core.utils.reporting.config import get_task_dependencies

# Logging setup
logger = logging.getLogger(__name__)


def get_all_tasks(task_reports: Dict[str, Dict[str, Any]]) -> List[str]:
    """
    Gets the list of all tasks from the reports.

    Parameters
    -----------
    task_reports : Dict[str, Dict[str, Any]]
        Dictionary {task_id: report}

    Returns
    --------
    List[str]
        List of task identifiers
    """
    return list(task_reports.keys())


def resolve_dependencies(task_dependencies: Dict[str, List[str]],
                         task_reports: Dict[str, Dict[str, Any]]) -> Dict[str, List[str]]:
    """
    Resolves task dependencies against the tasks present in the reports.

    Parameters
    -----------
    task_dependencies : Dict[str, List[str]]
        Dictionary {task: [dependencies]}
    task_reports : Dict[str, Dict[str, Any]]
        Dictionary {task_id: report}

    Returns
    --------
    Dict[str, List[str]]
        Updated dependency dictionary
    """
    resolved_dependencies = {}
    all_tasks = set(task_reports.keys())

    for task_id, deps in task_dependencies.items():
        if task_id in all_tasks:
            # Keep only dependencies that exist
            valid_deps = [dep for dep in deps if dep in all_tasks]
            resolved_dependencies[task_id] = valid_deps

    # Add tasks that are in the reports but not listed in the dependencies
    for task_id in all_tasks:
        if task_id not in resolved_dependencies:
            resolved_dependencies[task_id] = []

    return resolved_dependencies


def check_circular_dependencies(dependencies: Dict[str, List[str]]) -> List[Tuple[str, str]]:
    """
    Checks for circular dependencies.

    Parameters
    -----------
    dependencies : Dict[str, List[str]]
        Dictionary {task: [dependencies]}

    Returns
    --------
    List[Tuple[str, str]]
        List of task pairs that form circular dependencies
    """
    cycles = []
    visited = set()
    path = []

    def dfs(node):
        if node in path:
            # Found a cycle
            cycle_start = path.index(node)
            for i in range(cycle_start, len(path) - 1):
                cycles.append((path[i], path[i + 1]))
            cycles.append((path[-1], node))
            return

        if node in visited:
            return

        visited.add(node)
        path.append(node)

        for dep in dependencies.get(node, []):
            dfs(dep)

        path.pop()

    for node in dependencies:
        if node not in visited:
            dfs(node)

    return cycles


def topological_sort(dependencies: Dict[str, List[str]]) -> List[str]:
    """
    Performs a topological sort of the tasks.

    Parameters
    -----------
    dependencies : Dict[str, List[str]]
        Dictionary {task: [dependencies]}

    Returns
    --------
    List[str]
        List of tasks in execution order
    """
    # Create the result list
    result = []

    # Make a copy of the dependencies to modify
    deps_copy = {task: list(deps) for task, deps in dependencies.items()}

    # Find tasks without dependencies
    no_deps = [task for task, deps in deps_copy.items() if not deps]

    # While there are tasks without dependencies
    while no_deps:
        # Take the next task without dependencies
        current = no_deps.pop(0)
        result.append(current)

        # For every task that depends on the current one
        for task, deps in list(deps_copy.items()):
            if current in deps:
                # Remove the current task from its dependencies
                deps.remove(current)

                # If no dependencies remain, add it to the no-dependency list
                if not deps:
                    no_deps.append(task)

    # Unresolved dependencies left over mean there are cycles
    if any(deps for deps in deps_copy.values()):
        logger.warning("Circular dependencies detected. Returning a partial order.")

    return result


def get_dependent_tasks(task_id: str, dependencies: Dict[str, List[str]]) -> List[str]:
    """
    Gets the list of tasks that depend on the given task.

    Parameters
    -----------
    task_id : str
        Task identifier
    dependencies : Dict[str, List[str]]
        Dictionary {task: [dependencies]}

    Returns
    --------
    List[str]
        List of dependent task identifiers
    """
    dependent_tasks = []

    for task, deps in dependencies.items():
        if task_id in deps:
            dependent_tasks.append(task)

    return dependent_tasks


def enrich_tasks_with_dependencies(task_reports: Dict[str, Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    """
    Enriches task reports with dependency information.

    Parameters
    -----------
    task_reports : Dict[str, Dict[str, Any]]
        Dictionary {task_id: report}

    Returns
    --------
    Dict[str, Dict[str, Any]]
        Updated report dictionary
    """
    # Get dependencies from the configuration
    config_dependencies = get_task_dependencies()

    # Resolve dependencies
    dependencies = resolve_dependencies(config_dependencies, task_reports)

    # Update the reports
    for task_id, report in task_reports.items():
        # Add dependencies
        report["dependencies"] = dependencies.get(task_id, [])

        # Add dependent tasks
        report["dependents"] = get_dependent_tasks(task_id, dependencies)

    return task_reports


def create_dependency_graph_data(task_reports: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    """
    Creates data for visualizing the dependency graph.

    Parameters
    -----------
    task_reports : Dict[str, Dict[str, Any]]
        Dictionary {task_id: report}

    Returns
    --------
    Dict[str, Any]
        Graph visualization data
    """
    # Get dependencies from the configuration
    config_dependencies = get_task_dependencies()

    # Resolve dependencies
    dependencies = resolve_dependencies(config_dependencies, task_reports)

    # Create nodes
    nodes = []
    for task_id, report in task_reports.items():
        nodes.append({
            "id": task_id,
            "name": report.get("task_description", task_id),
            "status": report.get("status", "unknown")
        })

    # Create edges
    edges = []
    for task_id, deps in dependencies.items():
        for dep in deps:
            edges.append({
                "source": dep,
                "target": task_id,
                "label": ""
            })

    return {
        "nodes": nodes,
        "edges": edges
    }


def check_missing_dependencies(task_reports: Dict[str, Dict[str, Any]]) -> Dict[str, List[str]]:
    """
    Checks for missing dependencies.

    Parameters
    -----------
    task_reports : Dict[str, Dict[str, Any]]
        Dictionary {task_id: report}

    Returns
    --------
    Dict[str, List[str]]
        Dictionary {task: [missing_dependencies]}
    """
    # Get dependencies from the configuration
    config_dependencies = get_task_dependencies()

    # Get the list of all tasks
    all_tasks = set(task_reports.keys())

    # Check for missing dependencies
    missing_dependencies = {}

    for task_id, deps in config_dependencies.items():
        if task_id in all_tasks:
            missing = [dep for dep in deps if dep not in all_tasks]
            if missing:
                missing_dependencies[task_id] = missing

    return missing_dependencies


def suggest_dependencies(task_reports: Dict[str, Dict[str, Any]]) -> Dict[str, List[str]]:
    """
    Suggests possible dependencies based on task execution times.

    Parameters
    -----------
    task_reports : Dict[str, Dict[str, Any]]
        Dictionary {task_id: report}

    Returns
    --------
    Dict[str, List[str]]
        Dictionary {task: [suggested_dependencies]}
    """
    # Get existing dependencies
    config_dependencies = get_task_dependencies()

    # Sort tasks by start time
    tasks_by_time = [(task_id, report.get("start_time", ""))
                     for task_id, report in task_reports.items()]
    tasks_by_time.sort(key=lambda x: x[1])

    # Build the list of tasks in execution order
    task_sequence = [task_id for task_id, _ in tasks_by_time]

    # Suggest dependencies
    suggestions = {}

    for i in range(1, len(task_sequence)):
        current_task = task_sequence[i]
        prev_task = task_sequence[i - 1]

        # Skip the current task if it already has dependencies
        if current_task in config_dependencies and config_dependencies[current_task]:
            continue

        # Suggest the previous task as a dependency
        suggestions[current_task] = [prev_task]

    return suggestions


def create_dependency_graph_svg(task_reports: Dict[str, Dict[str, Any]],
                                output_path: Optional[Path] = None) -> Optional[str]:
    """
    Creates an SVG image of the dependency graph.

    Parameters
    -----------
    task_reports : Dict[str, Dict[str, Any]]
        Dictionary {task_id: report}
    output_path : Path, optional
        Path to save the SVG to (if not specified, the SVG is not saved)

    Returns
    --------
    str or None
        SVG markup, or None on error
    """
    try:
        # Try to import graphviz
        import graphviz
    except ImportError:
        logger.warning("The graphviz module is not installed. Cannot create SVG.")
        return None

    try:
        # Create the graph
        dot = graphviz.Digraph("dependency_graph", format="svg")

        # Configure the graph style
        dot.attr("graph", rankdir="LR", nodesep="0.5", ranksep="1")
        dot.attr("node", shape="box", style="filled", fontname="Arial", fontsize="12")
        dot.attr("edge", fontname="Arial", fontsize="10")

        # Get the graph data
        graph_data = create_dependency_graph_data(task_reports)

        # Add nodes
        for node in graph_data["nodes"]:
            # Pick a color based on the status
            fillcolor = "#FFFFFF"  # White by default
            if node["status"] == "completed":
                fillcolor = "#D1E7DD"  # Green
            elif node["status"] == "error" or node["status"] == "failed":
                fillcolor = "#F8D7DA"  # Red
            elif node["status"] == "running":
                fillcolor = "#FFF3CD"  # Yellow

            # Add the node
            dot.node(node["id"], label=node["name"], fillcolor=fillcolor)

        # Add edges
        for edge in graph_data["edges"]:
            dot.edge(edge["source"], edge["target"], label=edge["label"])

        # Render SVG
        svg_data = dot.pipe().decode("utf-8")

        # Save the SVG if a path was given
        if output_path:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(svg_data)
            logger.info(f"SVG graph saved to {output_path}")

        return svg_data
    except Exception as e:
        logger.error(f"Error creating SVG graph: {e}")
        return None