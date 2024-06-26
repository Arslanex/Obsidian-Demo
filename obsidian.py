import streamlit as st
import pandas as pd
import os

# Configuration
vault_path = "/Users/enesarslan/Documents/Deneme/"

def create_obsidian_page(name, surname, selected_columns, linked_columns, row, unique_id):
    # Create page content based on selected columns
    content = f"# {name} {surname}\n\n"
    for col in selected_columns:
        value = f"[[{row[col]}]]" if col in linked_columns else row[col]
        content += f"- **{col}**: {value}\n"

    # Define file path with unique identifier
    file_path = os.path.join(vault_path, f"{name} {surname} {unique_id}.md")

    # Write content to file
    try:
        with open(file_path, 'w') as file:
            file.write(content)
    except Exception as e:
        st.error(f"Error writing to file {file_path}: {e}")
        return False

    return True

def main():
    st.title("Obsidian Page Generator from CSV")

    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

    if uploaded_file is not None:
        try:
            data = pd.read_csv(uploaded_file)
            st.write("CSV file loaded successfully")
            st.dataframe(data)
        except Exception as e:
            st.error(f"Error reading the CSV file: {e}")
            return

        # Get list of columns
        columns = list(data.columns)

        # Ensure required columns are present
        if 'Name' not in columns or 'Surname' not in columns:
            st.error("CSV file must contain 'Name' and 'Surname' columns.")
            return

        selected_columns = st.multiselect("Select columns to include in the Obsidian pages", columns, default=columns)
        linked_columns = st.multiselect("Select columns to add as linked values", selected_columns, default=[])

        if st.button("Generate Obsidian Pages"):
            total_rows = len(data)
            progress_bar = st.progress(0)
            for i, (index, row) in enumerate(data.iterrows()):
                name, surname = row['Name'], row['Surname']
                unique_id = index  # Use row index as a unique identifier
                success = create_obsidian_page(name, surname, selected_columns, linked_columns, row, unique_id)
                if success:
                    st.success(f"Successfully created page for {name} {surname}")
                else:
                    st.error(f"Failed to create page for {name} {surname}")
                progress_bar.progress((i + 1) / total_rows)

            st.write("Script completed.")

if __name__ == "__main__":
    main()
