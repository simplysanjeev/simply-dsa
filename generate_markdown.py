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

input_dir = "src/main/java"
output_dir = "docs"
mkdocs_config_path = "mkdocs.yml"

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

            target_dir = os.path.join(output_dir, relative_path)
            os.makedirs(target_dir, exist_ok=True)

            with open(os.path.join(root, file), "r") as f:
                java_code = f.read()

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

            md_content = f"# `{class_name}.java`\n\n" \
                         f"## Full Source\n\n" \
                         f"```java\n{java_code}\n```"

            if example_code:
                md_content += f"\n---\n\n## ✨ Example Usage\n\n```java\n{chr(10).join(example_code)}\n```"

            md_file_path = os.path.join(target_dir, f"{class_name}.md")
            with open(md_file_path, "w") as f:
                f.write(md_content)

            doc_rel_path = os.path.relpath(md_file_path, output_dir).replace(os.sep, "/")
            add_to_nav(path_parts + [class_name], doc_rel_path)

def build_nav(d):
    result = []
    for key, value in sorted(d.items()):
        if isinstance(value, dict):
            result.append({key: build_nav(value)})
        else:
            result.append({key: value})  # Removed 📄 to better suit vertical layout
    return result

nav_list = build_nav(nav_entries)

mkdocs_config = {
    'site_name': 'Simply DSA',
    'theme': {
        'name': 'material',
        'features': [
            'navigation.sections',
            'navigation.expand',
            'toc.integrate',
            'content.code.copy'
        ]
    },
    'nav': nav_list
}

with open(mkdocs_config_path, 'w') as f:
    yaml.dump(mkdocs_config, f, sort_keys=False)

print("✅ All Java files converted to Markdown with vertical sidebar navigation and styled examples!")
