import pypdf
import os
import sys

def extract_title(page):
  """
    Extracts a potential title from a PDF page.
    Heuristic: Assumes the first non-empty, stripped line is the title.
    Returns None if no text or title found.
    """
  try:
    text = page.extract_text()
    if not text:
      return None
    lines = text.splitlines()
    for line in lines:
      stripped_line = line.strip()
      if stripped_line:
        # Simple cleaning: remove multiple spaces
        return ' '.join(stripped_line.split())
    return None # No non-empty lines found
  except Exception as e:
    # Handle potential errors during text extraction if needed
    # print(f"  Debug: Error extracting text for title: {e}")
    return None

def extract_final_slides_by_title(input_pdf_path, output_pdf_path):
  """
    Extracts the final version of incrementally built slides from a PDF
    by comparing the titles of consecutive pages.

    Args:
        input_pdf_path (str): Path to the input PDF file.
        output_pdf_path (str): Path to save the output PDF file.
    """
  final_pages_indices = []

  try:
    reader = pypdf.PdfReader(input_pdf_path)
    num_pages = len(reader.pages)

    if num_pages == 0:
      print("Input PDF has no pages.")
      return

    print(f"Processing {num_pages} pages from '{input_pdf_path}'...")

    i = 0
    while i < num_pages:
      current_page = reader.pages[i]
      current_title = extract_title(current_page)

      if current_title is None:
        print(f"Warning: Could not determine title for page {i+1}. Adding page as is.")
        final_pages_indices.append(i)
        i += 1
        continue

      print(f"Page {i+1}: Found potential title: '{current_title}'")

      # Look ahead to find the last page with the same title
      last_page_in_sequence = i
      for j in range(i + 1, num_pages):
        next_page = reader.pages[j]
        next_title = extract_title(next_page)

        # Compare titles
        if next_title == current_title:
          # Titles match, this page is part of the sequence
          # print(f"  Page {j+1}: Title matches. Continuing sequence.")
          last_page_in_sequence = j
        else:
          # Titles differ (or next title couldn't be extracted), sequence ends
          # print(f"  Page {j+1}: Title '{next_title}' differs. Ending sequence.")
          break
      else:
        # Inner loop finished without break (reached end of PDF)
        pass

      print(f"-> Logical slide ending on page {last_page_in_sequence + 1} (Title: '{current_title}')")
      final_pages_indices.append(last_page_in_sequence)
      i = last_page_in_sequence + 1 # Move to the page *after* the identified final slide

    if not final_pages_indices:
      print("No final slides identified based on the title logic.")
      return

    # Create the output PDF
    writer = pypdf.PdfWriter()
    print(f"\nAdding {len(final_pages_indices)} final pages to output PDF...")
    for page_index in final_pages_indices:
      writer.add_page(reader.pages[page_index])

    # Write the output file
    with open(output_pdf_path, "wb") as output_file:
      writer.write(output_file)

    print(f"Successfully created '{output_pdf_path}'")

  except FileNotFoundError:
    print(f"Error: Input file not found at '{input_pdf_path}'")
  except pypdf.errors.PdfReadError as e:
    print(f"Error reading PDF file '{input_pdf_path}': {e}")
  except Exception as e:
    print(f"An unexpected error occurred: {e}")
    import traceback
    traceback.print_exc()


# --- Main execution ---
if __name__ == "__main__":
  if len(sys.argv) < 2:
    print("Usage: python extract_slides_title.py <input_pdf_file>")
    # Example usage if no arguments provided:
    input_file = "presentation_with_transitions.pdf"
    output_file = "presentation_final_slides.pdf"
    print(f"\nNo input file specified. Trying default:")
    print(f"Input:  {input_file}")
    print(f"Output: {output_file}\n")
  elif len(sys.argv) == 2:
    input_file = sys.argv[1]
    base_name, ext = os.path.splitext(input_file)
    output_file = f"{base_name}_final_slides{ext}"
    print(f"Input:  {input_file}")
    print(f"Output: {output_file}\n")
  else:
     print("Usage: python extract_slides_title.py <input_pdf_file>")
     sys.exit(1)


  # Check if the default input exists if we're using it
  if len(sys.argv) < 2 and not os.path.exists(input_file):
      print(f"Default input file '{input_file}' not found.")
      print("Please provide the path to your input PDF.")
      sys.exit(1)

  extract_final_slides_by_title(input_file, output_file)
