from openai import OpenAI
import PyPDF2

client = OpenAI(
    api_key="YOUR API KEY"
)

def extract_text_from_pdf(pdf_path):
    """
    Extract all text from a PDF file.
    """
    text = ""
    with open(pdf_path, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()

def generate_flashcards(note_text):
    
    # The prompt instructs the model to return flashcards in plain text using the following format:
    
    #   Q: <question text>
    #   A: <answer text>
    
    # Each flashcard is separated by an empty line.
    
    # Returns a list of dictionaries where each dictionary has 'question' and 'answer' keys.
    prompt = (
        "Extract flashcards from the following notes. For each flashcard, generate a question and an answer. "
        "Return the flashcards in plain text using the following format:\n\n"
        "Q: <question text>\n"
        "A: <answer text>\n\n"
        "Separate each flashcard with an empty line.\n\n"
        "Notes:\n" + note_text
    )

    response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ],)
    
    generated_text = response.choices[0].message.content.strip()
    
    # Parse the plain text output into flashcards.
    flashcards = []
    blocks = generated_text.split("\n\n")
    for block in blocks:
        lines = block.strip().splitlines()
        if len(lines) >= 2:
            # Expect the first line to be the question and the second to be the answer.
            question_line = lines[0].strip()
            answer_line = lines[1].strip()
            if question_line.lower().startswith("q:"):
                question = question_line[2:].strip()
            else:
                question = question_line
            if answer_line.lower().startswith("a:"):
                answer = answer_line[2:].strip()
            else:
                answer = answer_line
            if question and answer:
                flashcards.append({"question": question, "answer": answer})
    return flashcards

# if __name__ == "__main__":
#     pdf_path = "dummy.pdf"
#     note_text = extract_text_from_pdf(pdf_path)
#     flashcards = generate_flashcards(note_text)
#     print("Generated Flashcards:")
#     for fc in flashcards:
#         print("Q:", fc.get("question"))
#         print("A:", fc.get("answer"))
#         print("-" * 40)
