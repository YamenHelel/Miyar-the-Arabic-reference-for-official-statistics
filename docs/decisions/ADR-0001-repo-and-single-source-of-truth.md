# ADR-0001: A GitHub repository as the single source of truth

- **Date:** 2026-11-03 · **Status:** accepted

## Context
The content must feed several channels: a public Arabic website (main channel), Claude and Codex skills, and later an MCP server. It must keep an audit trail, which official statisticians expect, and accept contributions.

## Decision
All knowledge lives as structured text files (YAML and Markdown) in one Git repository. Every channel is generated from it. No channel stores its own copy of the content.

## Consequences
- Version history, review through pull requests, and citable permalinks.
- Plain-text files cost few tokens for AI agents to read and are easy to validate.
- Non-technical contributors need a form-based path (see `05-ideas-backlog.md` I-031).
