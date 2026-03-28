import os
import win32com.client as win32

# Point this to your big folder
folder_path = r"C:\Users\Philip Lewis\Desktop\Local RAG\RAG - ALE ARCHITECTURE BOARD EXAM"

word = win32.gencache.EnsureDispatch('Word.Application')
word.Visible = False  # Keeps Word hidden while it works

print("Starting bulk conversion... go grab a coffee.")

for root, dirs, files in os.walk(folder_path):
    for file in files:
        if file.lower().endswith(".doc") and not file.startswith("~$"):
            doc_path = os.path.abspath(os.path.join(root, file))
            docx_path = doc_path + "x"

            # Skip if the .docx version already exists
            if not os.path.exists(docx_path):
                print(f"Converting: {file}")
                try:
                    doc = word.Documents.Open(doc_path)
                    # 16 = wdFormatXMLDocument (.docx)
                    doc.SaveAs2(docx_path, FileFormat=16)
                    doc.Close()
                except Exception as e:
                    print(f"Error converting {file}: {e}")

word.Quit()
print("Done! All your old .doc files now have modern .docx twins.")
