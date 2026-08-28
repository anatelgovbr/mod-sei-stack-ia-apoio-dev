#!/usr/bin/env bash

# Prepare the tasks phase for the current feature.
#
# Validates that the feature directory and plan.md exist, resolves the active
# tasks-template through the Spec Kit template stack (overrides > presets >
# extensions > core) and reports the documents available under FEATURE_DIR.
#
# Usage: ./setup-tasks.sh [--json]
#
# OUTPUTS:
#   JSON mode: {"FEATURE_DIR":"...","TASKS_TEMPLATE":"...","AVAILABLE_DOCS":["..."]}
#   Text mode: FEATURE_DIR:... \n TASKS_TEMPLATE:... \n AVAILABLE_DOCS: \n ✓/✗ file.md

set -e

JSON_MODE=false

for arg in "$@"; do
    case "$arg" in
        --json)
            JSON_MODE=true
            ;;
        --help|-h)
            echo "Usage: $0 [--json]"
            echo "  --json    Output results in JSON format"
            echo "  --help    Show this help message"
            exit 0
            ;;
        *)
            echo "ERROR: Unknown option '$arg'. Use --help for usage information." >&2
            exit 1
            ;;
    esac
done

# Source common functions
SCRIPT_DIR="$(CDPATH="" cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"

# Get feature paths and validate branch
_paths_output=$(get_feature_paths) || { echo "ERROR: Failed to resolve feature paths" >&2; exit 1; }
eval "$_paths_output"
unset _paths_output
check_feature_branch "$CURRENT_BRANCH" "$HAS_GIT" || exit 1

# Validate prerequisites
if [[ ! -d "$FEATURE_DIR" ]]; then
    echo "ERROR: Feature directory not found: $FEATURE_DIR" >&2
    echo "Run the specify phase first to create the feature structure." >&2
    exit 1
fi

if [[ ! -f "$IMPL_PLAN" ]]; then
    echo "ERROR: plan.md not found in $FEATURE_DIR" >&2
    echo "Run the plan phase first to create the implementation plan." >&2
    exit 1
fi

# Resolve the active tasks template (empty when none is installed)
TASKS_TEMPLATE=$(resolve_template "tasks-template" "$REPO_ROOT") || true
if [[ -n "$TASKS_TEMPLATE" ]] && [[ ! -f "$TASKS_TEMPLATE" ]]; then
    TASKS_TEMPLATE=""
fi

# Build list of available documents
docs=()
[[ -f "$RESEARCH" ]] && docs+=("research.md")
[[ -f "$DATA_MODEL" ]] && docs+=("data-model.md")
if [[ -d "$CONTRACTS_DIR" ]] && [[ -n "$(ls -A "$CONTRACTS_DIR" 2>/dev/null)" ]]; then
    docs+=("contracts/")
fi
[[ -f "$QUICKSTART" ]] && docs+=("quickstart.md")

# Output results
if $JSON_MODE; then
    if has_jq; then
        if [[ ${#docs[@]} -eq 0 ]]; then
            json_docs="[]"
        else
            json_docs=$(printf '%s\n' "${docs[@]}" | jq -R . | jq -s .)
        fi
        jq -cn \
            --arg feature_dir "$FEATURE_DIR" \
            --arg tasks_template "$TASKS_TEMPLATE" \
            --argjson docs "$json_docs" \
            '{FEATURE_DIR:$feature_dir,TASKS_TEMPLATE:$tasks_template,AVAILABLE_DOCS:$docs}'
    else
        if [[ ${#docs[@]} -eq 0 ]]; then
            json_docs="[]"
        else
            json_docs=$(for d in "${docs[@]}"; do printf '"%s",' "$(json_escape "$d")"; done)
            json_docs="[${json_docs%,}]"
        fi
        printf '{"FEATURE_DIR":"%s","TASKS_TEMPLATE":"%s","AVAILABLE_DOCS":%s}\n' \
            "$(json_escape "$FEATURE_DIR")" "$(json_escape "$TASKS_TEMPLATE")" "$json_docs"
    fi
else
    echo "FEATURE_DIR:$FEATURE_DIR"
    echo "TASKS_TEMPLATE:$TASKS_TEMPLATE"
    echo "AVAILABLE_DOCS:"
    check_file "$RESEARCH" "research.md"
    check_file "$DATA_MODEL" "data-model.md"
    check_dir "$CONTRACTS_DIR" "contracts/"
    check_file "$QUICKSTART" "quickstart.md"
fi
