from pypdf import PdfReader
from openai import OpenAI

client = OpenAI()


def extract_text(pdf_path):
    reader = PdfReader(pdf_path)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text: # This checks whether anything was actually extracted.(page text  = true)
            text += page_text + "\n" #text = "Hello\nHow are you?\nGoodbye\n"

    return text


def split_text(text, chunk_size=6000): #(0,15000,6000)
    chunks = []

    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i + chunk_size]) #0 to 6000, then 6000 to 12000 , 

    return chunks


def summarize_chunk(chunk): #
    response = client.responses.create(
        model="gpt-5-mini",
        input=f"""
Summarize the following section of a document.

Keep the important facts, arguments, names, numbers,
and conclusions. Do not add information that is not
present in the text.

DOCUMENT SECTION:

{chunk}
"""
    )

    return response.output_text


def summarize_document(pdf_path):
    text = extract_text(pdf_path)

    chunks = split_text(text)

    summaries = []

    for chunk in chunks:
        summary = summarize_chunk(chunk)
        summaries.append(summary)

    combined = "\n\n".join(summaries)

    response = client.responses.create(
        model="gpt-5-mini",
        input=f"""
Create a coherent final summary from these section summaries.

Remove repetition and preserve the important information.

SECTION SUMMARIES:

{combined}
"""
    )

    return response.output_text


pdf_path = r"C:\Users\user\Desktop\build an ai text summarizer\UnfairAdvantageDownload.pdf"

summary = summarize_document(pdf_path)

print(summary)