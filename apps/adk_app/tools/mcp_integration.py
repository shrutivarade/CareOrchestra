"""MCP (Model Context Protocol) integration layer for CareOrchestra.

This module loads and manages tools defined in mcp/toolbox/tools.yaml,
providing agents with access to database queries through a standardized interface.
"""

import logging
import os
import yaml
from typing import Optional, Dict, Any, List
from pathlib import Path
from .bigquery_tools.client import BigQueryClient

logger = logging.getLogger(__name__)


class MCPToolsManager:
    """Manages MCP tools and provides query execution interface."""
    
    def __init__(self, tools_yaml_path: Optional[str] = None, project_id: Optional[str] = None, dataset_id: str = "care_orchestra"):
        """
        Initialize MCP Tools Manager.
        
        Args:
            tools_yaml_path: Path to tools.yaml configuration file
            project_id: GCP project ID (if None, uses env variable)
            dataset_id: BigQuery dataset ID
        """
        self.tools_yaml_path = tools_yaml_path or self._find_tools_yaml()
        self.project_id = project_id or os.getenv("GCP_PROJECT_ID", "")
        self.dataset_id = dataset_id
        
        # Load tools configuration
        self.config = self._load_tools_config()
        
        # Initialize BigQuery client
        if self.project_id:
            self.bq_client = BigQueryClient(self.project_id, self.dataset_id)
        else:
            logger.warning("GCP_PROJECT_ID not configured. BigQuery operations will fail.")
            self.bq_client = None
        
        logger.info(f"MCPToolsManager initialized with {len(self.config.get('tools', {}))} tools")
    
    def _find_tools_yaml(self) -> str:
        """Find tools.yaml in the project structure."""
        # Try multiple common locations
        locations = [
            "mcp/toolbox/tools.yaml",
            "./mcp/toolbox/tools.yaml",
            "../../../mcp/toolbox/tools.yaml",
            os.path.expanduser("~/Downloads/GenAI/CareOrchestra/mcp/toolbox/tools.yaml"),
        ]
        
        for loc in locations:
            path = Path(loc).resolve()
            if path.exists():
                logger.info(f"Found tools.yaml at {path}")
                return str(path)
        
        raise FileNotFoundError("tools.yaml not found in expected locations")
    
    def _load_tools_config(self) -> Dict[str, Any]:
        """Load and parse tools.yaml configuration."""
        try:
            with open(self.tools_yaml_path, 'r') as f:
                config = yaml.safe_load(f)
            logger.info(f"Loaded tools configuration from {self.tools_yaml_path}")
            return config or {}
        except FileNotFoundError:
            logger.error(f"tools.yaml not found at {self.tools_yaml_path}")
            return {}
        except yaml.YAMLError as e:
            logger.error(f"Failed to parse tools.yaml: {e}")
            return {}
    
    def get_tool(self, tool_name: str) -> Optional[Dict[str, Any]]:
        """Get a tool definition by name."""
        tools = self.config.get("tools", {})
        tool = tools.get(tool_name)
        if tool:
            logger.debug(f"Retrieved tool definition: {tool_name}")
        else:
            logger.warning(f"Tool not found: {tool_name}")
        return tool
    
    def get_toolset(self, toolset_name: str) -> List[str]:
        """Get a list of tool names in a toolset."""
        toolsets = self.config.get("toolsets", {})
        toolset = toolsets.get(toolset_name, [])
        logger.debug(f"Retrieved toolset '{toolset_name}' with {len(toolset)} tools")
        return toolset
    
    async def execute_tool(self, tool_name: str, **kwargs) -> List[Dict[str, Any]]:
        """
        Execute a tool by name.
        
        Args:
            tool_name: Name of the tool to execute
            **kwargs: Optional parameters to pass to the query
            
        Returns:
            Query results as list of dictionaries
        """
        if not self.bq_client:
            raise RuntimeError("BigQueryClient not initialized. Check GCP_PROJECT_ID.")
        
        tool = self.get_tool(tool_name)
        if not tool:
            raise ValueError(f"Tool '{tool_name}' not found in configuration")
        
        tool_kind = tool.get("kind")
        
        if tool_kind == "bigquery-sql":
            sql = tool.get("statement", "")
            if not sql:
                raise ValueError(f"Tool '{tool_name}' has no SQL statement")
            
            logger.info(f"Executing tool '{tool_name}'")
            results = await self.bq_client.query(sql, parameters=kwargs if kwargs else None)
            return results
        else:
            raise ValueError(f"Unsupported tool kind: {tool_kind}")
    
    def list_tools(self) -> Dict[str, str]:
        """List all available tools with their descriptions."""
        tools = self.config.get("tools", {})
        result = {}
        for tool_name, tool_def in tools.items():
            description = tool_def.get("description", "No description").strip()
            result[tool_name] = description
        return result
    
    def list_toolsets(self) -> Dict[str, List[str]]:
        """List all available toolsets."""
        return self.config.get("toolsets", {})


# Global instance (lazy-loaded)
_mcp_manager: Optional[MCPToolsManager] = None


def get_mcp_manager(tools_yaml_path: Optional[str] = None) -> MCPToolsManager:
    """Get or create the global MCP manager instance."""
    global _mcp_manager
    if _mcp_manager is None:
        _mcp_manager = MCPToolsManager(tools_yaml_path=tools_yaml_path)
    return _mcp_manager


def reset_mcp_manager() -> None:
    """Reset the global MCP manager (useful for testing)."""
    global _mcp_manager
    _mcp_manager = None
