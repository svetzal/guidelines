#!/bin/zsh
# Common utilities for agentic shell scripts
# Source this file at the top of your scripts:
#   source "$(dirname "$0")/common.sh"

# Find project root by looking for .git
find_project_root() {
    local dir="${1:-$(pwd)}"
    while [[ "$dir" != "/" ]]; do
        if [[ -d "$dir/.git" ]]; then
            echo "$dir"
            return 0
        fi
        dir="$(dirname "$dir")"
    done
    return 1
}

# Set PROJECT_ROOT - can be called from anywhere
SCRIPT_DIR="$(cd "$(dirname "${0}")" && pwd)"
PROJECT_ROOT="$(find_project_root "$SCRIPT_DIR")"

if [[ -z "$PROJECT_ROOT" ]]; then
    echo "Error: Could not find project root" >&2
    exit 1
fi

AUDIT_DIR="$PROJECT_ROOT/agentic/audit"
mkdir -p "$AUDIT_DIR"

export PROJECT_ROOT
export SCRIPT_DIR
export AUDIT_DIR

# Iterate: assess, name, plan, and execute improvements
# Usage: iterate <agent> <folder>
#   agent  - Claude agent name (e.g., elixir-phoenix-craftsperson)
#   folder - project folder to assess (e.g., apps/web)
iterate() {
    local agent="$1"
    local folder="$2"

    if [[ -z "$agent" || -z "$folder" ]]; then
        echo "Usage: iterate <agent> <folder>" >&2
        return 1
    fi

    # Read-only tools for assessment/planning steps
    local readonly_tools="Read Glob Grep WebFetch WebSearch"

    echo "==> Assessing $folder with $agent..."
    local assessment=$(claude --dangerously-skip-permissions --agent "$agent" --model opus --print --allowedTools $readonly_tools << EOF
Assess the project in $folder against your principles. Identify the principle that it
is most violating, and describe how we should correct it.
EOF
    )

    echo "==> Generating filename..."
    local raw_name=$(claude --dangerously-skip-permissions --agent "$agent" --model haiku --print --allowedTools $readonly_tools << EOF
Output ONLY a short kebab-case filename (no extension) summarizing the main issue.
Rules: lowercase, hyphens only, no spaces, no backticks, no explanation, max 50 chars.
Example: fix-duplicate-api-helpers

Assessment:
$assessment
EOF
    )
    # Sanitize: extract first valid kebab-case word, strip anything else
    local name=$(echo "$raw_name" | grep -oE '[a-z0-9-]+' | head -1 | cut -c1-50)
    if [[ -z "$name" ]]; then
        name="assessment-$(date +%Y%m%d-%H%M%S)"
    fi

    echo "$assessment" > "$AUDIT_DIR/$name.md"
    echo "    Saved: $AUDIT_DIR/$name.md"

    echo "==> Creating plan..."
    local plan=$(claude --dangerously-skip-permissions --agent "$agent" --model opus --print --allowedTools $readonly_tools << EOF
Based on the following assessment, create a step-by-step plan to address the issues
identified. Make sure each step is clear and actionable.

Assessment:
$assessment
EOF
    )

    echo "$plan" > "$AUDIT_DIR/$name-plan.md"
    echo "    Saved: $AUDIT_DIR/$name-plan.md"

    echo "==> Executing plan..."
    local execute=$(claude --dangerously-skip-permissions --agent "$agent" --model sonnet << EOF
Execute the following plan to improve the project in $folder.

Plan:
$plan
EOF
    )

    echo "$execute" > "$AUDIT_DIR/$name-actions.md"
    echo "    Saved: $AUDIT_DIR/$name-actions.md"

    echo "==> Complete: $name"
}

export PROJECT_ROOT
export SCRIPT_DIR
export AUDIT_DIR