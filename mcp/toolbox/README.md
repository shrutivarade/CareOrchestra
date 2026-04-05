# MCP Toolbox for CareOrchestra

Placeholder for Model Context Protocol (MCP) toolbox configuration.

## Purpose

MCP Toolbox will expose BigQuery and other database tools to agents via the Model Context Protocol standard, enabling:

- Agents to query patient data dynamically
- Standardized tool interface across agents
- Better integration with advanced language models
- Cleaner separation between agent logic and data access

## Planned Configuration

The `config.json` file will define:

```json
{
  "version": "1.0",
  "tools": [
    {
      "name": "bigquery",
      "type": "database",
      "capabilities": ["query", "insert", "update"],
      "config": {
        "project_id": "${GCP_PROJECT_ID}",
        "dataset": "care_orchestra"
      }
    }
  ]
}
```

## Implementation

Planned for Phase 2 of development.

Currently, agents use direct service layer calls for data access.

## Integration Points

- Agent tool definitions will reference MCP toolbox
- Agents will use MCP SDK to call registered tools
- Supports tool composition and chaining

## References

- [MCP Protocol](https://modelcontextprotocol.io/)
- MCP SDK Documentation

## Testing

MCP tools will be tested with:
- Tool validation tests
- Integration tests with agents
- Performance benchmarks
