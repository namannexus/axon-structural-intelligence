from fpdf import FPDF
import datetime

class StructuralReport(FPDF):
    def header(self):
        self.set_font("Arial", "B", 16)
        self.set_text_color(25, 118, 210) 
        self.cell(0, 10, "AXON: Structural Intelligence Report", ln=True, align="C")
        self.set_font("Arial", "I", 10)
        self.set_text_color(100)
        self.cell(0, 10, f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True, align="C")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")

def generate_pdf_report(analysis_results, output_path):
    pdf = StructuralReport()
    pdf.add_page()
    
    # Executive Summary
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "1. Executive Summary", ln=True)
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 7, analysis_results.get('explanation', {}).get('summary', "N/A"))
    pdf.ln(5)

    # Risk Assessment
    pdf.set_fill_color(255, 243, 224) 
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "2. Safety & Risk Assessment", ln=True, fill=True)
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 7, analysis_results.get('explanation', {}).get('structural_risks', "N/A"), fill=True)
    pdf.ln(10)

    # Materials Table
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "3. Material Recommendations", ln=True)
    pdf.set_font("Arial", "B", 10)
    pdf.set_fill_color(240, 240, 240)
    pdf.cell(60, 10, "Element", border=1, fill=True)
    pdf.cell(80, 10, "Material", border=1, fill=True)
    pdf.cell(50, 10, "Match Score", border=1, fill=True)
    pdf.ln()

    recs = analysis_results.get('materials', {}).get('recommendations', [])
    pdf.set_font("Arial", "", 10)
    for rec in recs:
        top_mat = rec.get('recommended_materials', [{}])[0]
        pdf.cell(60, 10, str(rec.get('element', 'N/A')), border=1)
        pdf.cell(80, 10, str(top_mat.get('material', 'N/A')), border=1)
        pdf.cell(50, 10, f"{top_mat.get('score', 0)*100:.0f}%", border=1)
        pdf.ln()

    pdf.output(output_path)
    return output_path