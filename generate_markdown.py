# Directory Structure:
# simply-dsa/
# ├── pom.xml             # Maven project file
# ├── src/
# │   └── main/
# │       └── java/       # Your Java source files (can have subfolders)
# ├── docs/               # Auto-generated markdown files (mirrors Java package structure)
# ├── mkdocs.yml          # MkDocs config
# └── generate_markdown.py

import os
import yaml

# Updated input directory for Maven project structure
input_dir = "src/main/java"
output_dir = "docs"
mkdocs_config_path = "mkdocs.yml"

# Collect paths for mkdocs nav
nav_entries = {}

def add_to_nav(path_parts, file_path):
    ref = nav_entries
    for part in path_parts[:-1]:
        ref = ref.setdefault(part, {})
    ref[path_parts[-1]] = file_path

for root, dirs, files in os.walk(input_dir):
    for file in files:
        if file.endswith(".java"):
            relative_path = os.path.relpath(root, input_dir)
            path_parts = relative_path.split(os.sep) if relative_path != '.' else []
            class_name = file.replace(".java", "")

            # Create corresponding directory in docs
            target_dir = os.path.join(output_dir, relative_path)
            os.makedirs(target_dir, exist_ok=True)

            # Read Java code
            with open(os.path.join(root, file), "r") as f:
                java_code = f.read()

            # Extract example block
            example_code = []
            inside_example = False
            for line in java_code.splitlines():
                if line.strip().startswith("// Example Start"):
                    inside_example = True
                    continue
                elif line.strip().startswith("// Example End"):
                    inside_example = False
                    continue
                if inside_example:
                    example_code.append(line)

            # Write to markdown
            md_content = f"# {class_name}.java\n\n```java\n{java_code}\n```"
            if example_code:
                md_content += f"\n\n### Example\n\n```java\n{chr(10).join(example_code)}\n```"

            md_file_path = os.path.join(target_dir, f"{class_name}.md")
            with open(md_file_path, "w") as f:
                f.write(md_content)

            # Record for mkdocs nav
            doc_rel_path = os.path.relpath(md_file_path, output_dir).replace(os.sep, "/")
            add_to_nav(path_parts + [class_name], doc_rel_path)

# Build the mkdocs nav section
nav_list = []

def build_nav(d):
    result = []
    for key, value in sorted(d.items()):
        if isinstance(value, dict):
            result.append({key: build_nav(value)})
        else:
            result.append({key: value})
    return result

nav_list = build_nav(nav_entries)

# Update mkdocs.yml
mkdocs_config = {
    'site_name': 'Simply DSA',
    'theme': {
        'name': 'material'
    },
    'nav': nav_list
}

with open(mkdocs_config_path, 'w') as f:
    yaml.dump(mkdocs_config, f, sort_keys=False)

print("✅ All Java files converted to Markdown with examples and mkdocs.yml updated with navigation!")
