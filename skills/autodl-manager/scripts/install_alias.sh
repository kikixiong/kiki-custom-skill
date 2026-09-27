#!/bin/bash
# Install autodl alias for easy access

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLI_PATH="$SCRIPT_DIR/autodl_cli.py"

# Detect shell
if [ -n "$ZSH_VERSION" ]; then
    SHELL_RC="$HOME/.zshrc"
elif [ -n "$BASH_VERSION" ]; then
    SHELL_RC="$HOME/.bashrc"
else
    echo "Warning: Unknown shell, using ~/.bashrc"
    SHELL_RC="$HOME/.bashrc"
fi

# Create alias
ALIAS_LINE="alias autodl='python3 $CLI_PATH'"

# Check if alias already exists
if grep -q "alias autodl=" "$SHELL_RC" 2>/dev/null; then
    echo "⚠️  Alias 'autodl' already exists in $SHELL_RC"
    echo "   Remove old line and add new one? [y/N]"
    read -r response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        # Remove old alias
        if [[ "$OSTYPE" == "darwin"* ]]; then
            sed -i '' '/alias autodl=/d' "$SHELL_RC"
        else
            sed -i '/alias autodl=/d' "$SHELL_RC"
        fi
        # Add new alias
        echo "$ALIAS_LINE" >> "$SHELL_RC"
        echo "✅ Updated alias in $SHELL_RC"
    else
        echo "❌ Aborted"
        exit 1
    fi
else
    # Add alias
    echo "" >> "$SHELL_RC"
    echo "# AutoDL Manager alias" >> "$SHELL_RC"
    echo "$ALIAS_LINE" >> "$SHELL_RC"
    echo "✅ Added alias to $SHELL_RC"
fi

echo ""
echo "🎉 Installation complete!"
echo ""
echo "Reload your shell:"
echo "   source $SHELL_RC"
echo ""
echo "Or start a new terminal, then use:"
echo "   autodl --help"
echo "   autodl add <name> --host <host> --port <port>"
echo "   autodl list"
echo "   autodl status <name>"
echo "   autodl connect <name>"
