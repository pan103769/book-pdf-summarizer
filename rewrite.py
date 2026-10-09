from pypdf import PdfReader
import ollama

reader = PdfReader("./pdf_document/UnfairAdvantageDownload.pdf")

#extract text 
def extract_text():
    text = ""
    for i in range(0,len(reader.pages)):
        page_text = reader.pages[i].extract_text()
        if page_text :
            text += page_text +"\n"
    return text        
text = extract_text()
# print(extract_text())

#split text 
def split_text(chunk):
    chunk = 6000
    chunks_lib = []
    for i in range(0,len(text),6000):
        chunks_lib.append(text[i:i+chunk])
    return chunks_lib    
chunks_lib = split_text(chunk=6000)





#summarize chunk 
def summarize_chunk():
    summarized_chunks_lib = []
    for i in chunks_lib:
        response = ollama.generate(
            model = "llama3.2",
            prompt=f"summarize this part of document{i}"
        )
        summarized_chunks_lib.append(response["response"])
    return summarized_chunks_lib
summarized_chunk_lib = summarize_chunk()




#4.summarize document 
def summarize_ducument(summarized_chunk_lib):
    
    
    response = ollama.generate(
            model="llama3.2",
            prompt=f"summarize full document from the summarized parts of ducument{summarized_chunk_lib}"
        )
    return response["response"]    

print(summarize_ducument(summarized_chunk_lib))