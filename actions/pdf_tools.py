import os

def pdf_tools(parameters=None, player=None, speak=None, **kwargs):
    if not parameters:
        return "No se especificó la acción."
    action    = parameters.get("action", "read")
    file_path = parameters.get("file_path", "")
    pages_str = parameters.get("pages", "")

    if action == "read":
        try:
            import pdfplumber
            with pdfplumber.open(file_path) as pdf:
                text = "\n".join(p.extract_text() or "" for p in pdf.pages[:10])
            return text[:3000] if text else "PDF sin texto."
        except ImportError:
            try:
                import PyPDF2
                with open(file_path, "rb") as f:
                    r = PyPDF2.PdfReader(f)
                    text = "\n".join(p.extract_text() or "" for p in r.pages[:10])
                return text[:3000]
            except Exception as e:
                return f"Error: {e}"

    if action == "info":
        try:
            import PyPDF2
            with open(file_path, "rb") as f:
                r = PyPDF2.PdfReader(f)
                return (f"PDF: {file_path}\n"
                        f"Páginas: {len(r.pages)}\n"
                        f"Metadatos: {r.metadata}")
        except Exception as e:
            return f"Error: {e}"

    if action == "merge":
        files_str = parameters.get("files", "")
        out_name  = parameters.get("output_name", "merged.pdf")
        try:
            import PyPDF2
            writer = PyPDF2.PdfWriter()
            for fp in files_str.split(","):
                fp = fp.strip()
                if os.path.exists(fp):
                    with open(fp, "rb") as f:
                        reader = PyPDF2.PdfReader(f)
                        for page in reader.pages:
                            writer.add_page(page)
            out_path = os.path.join(os.path.dirname(file_path), out_name)
            with open(out_path, "wb") as f:
                writer.write(f)
            return f"PDFs combinados en: {out_path}"
        except Exception as e:
            return f"Error al combinar: {e}"

    if action == "split":
        try:
            import PyPDF2
            with open(file_path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                base   = os.path.splitext(file_path)[0]
                for i, page in enumerate(reader.pages):
                    writer = PyPDF2.PdfWriter()
                    writer.add_page(page)
                    out = f"{base}_page_{i+1}.pdf"
                    with open(out, "wb") as fout:
                        writer.write(fout)
            return f"PDF dividido en {len(reader.pages)} archivos."
        except Exception as e:
            return f"Error al dividir: {e}"

    return f"Acción PDF '{action}' no reconocida."
