def format_requirements_file(input_file, output_file=None):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    formatted_lines = []
    
    for line in lines:
        # Strip leading/trailing whitespace from the line
        line = line.strip()
        
        # If the line is not empty, format it
        if line:
            parts = line.split()
            if len(parts) == 2:
                formatted_lines.append(f"{parts[0]}=={parts[1]}")
            else:
                formatted_lines.append(line)
    
    # Write the formatted content to the same or new file
    output_file = output_file if output_file else input_file
    with open(output_file, 'w') as file:
        file.write('\n'.join(formatted_lines))
    
    print(f"Requirements file '{output_file}' has been updated.")

# Example usage:
format_requirements_file('requirements.txt')
