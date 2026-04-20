from pathlib import Path
import re

from pypdf import PdfReader
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer


ROOT = Path(__file__).resolve().parent
SOURCE_PDF = ROOT / "main.pdf"
OUTPUT_PDF = ROOT / "MAAT_renewed_paper.pdf"

TITLE = "Physics-Aware Action-Conditioned World Modeling for Billiards"
SUBTITLE = "DiT + Diffusion Forcing on Large Synthetic Multi-Run Datasets"
AUTHOR = "Moin Arz Mattar"
DATE = "April 2026"


def extract_source_text() -> str:
    reader = PdfReader(str(SOURCE_PDF))
    pages = []
    for page in reader.pages:
        pages.append(page.extract_text() or "")
    return "\n".join(pages)


def normalize_text(text: str) -> str:
    text = text.replace("\u00ad", "")
    text = re.sub(r"\n\d+\n", "\n", text)
    text = text.replace("work such as Oasis [2, 1].", "work such as Oasis.")
    text = text.replace("Our approach builds on DDPM [5], DDIM [9], latent diffusion [8], DiT [7], and VAE latent modeling\n[6]. We also draw motivation from world models [3, 4] and action-conditioned diffusion gameplay\n1work such as Oasis [2, 1].",
                        "Our approach builds on DDPM, DDIM, latent diffusion, DiT, and VAE latent modeling. We also draw motivation from world models and action-conditioned diffusion gameplay work such as Oasis.")
    lines = [line.rstrip() for line in text.splitlines()]

    # Drop the stale title block from the previous PDF build.
    skip_prefixes = {
        TITLE,
        SUBTITLE,
        "Your Name",
        "CS89/189 Final Project",
        "March 3, 2026",
    }
    cleaned = []
    for line in lines:
        if line in skip_prefixes:
            continue
        if re.fullmatch(r"\d+\s*/\s*\d+", line):
            continue
        cleaned.append(line)

    text = "\n".join(cleaned)
    text = re.sub(r"([a-z])-\n([a-z])", r"\1\2", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r" +", " ", text)
    return text.strip()


def split_blocks(text: str):
    block = []
    for line in text.splitlines():
        if line.strip():
            block.append(line.strip())
        else:
            if block:
                yield " ".join(block)
                block = []
    if block:
        yield " ".join(block)


def classify_block(block: str):
    if re.fullmatch(r"(Abstract|[0-9]+ [A-Z].+|[0-9]+\.[0-9]+ .+)", block):
        return "heading"
    if block.startswith("•"):
        return "bullet"
    return "paragraph"


def build_pdf():
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "CustomTitle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=20,
        leading=24,
        spaceAfter=8,
    )
    subtitle_style = ParagraphStyle(
        "Subtitle",
        parent=styles["Heading2"],
        alignment=TA_CENTER,
        fontSize=12,
        leading=15,
        spaceAfter=4,
    )
    meta_style = ParagraphStyle(
        "Meta",
        parent=styles["Normal"],
        alignment=TA_CENTER,
        fontSize=10,
        leading=12,
        spaceAfter=16,
    )
    body_style = ParagraphStyle(
        "Body",
        parent=styles["BodyText"],
        alignment=TA_JUSTIFY,
        fontSize=10.5,
        leading=14,
        spaceAfter=8,
    )
    heading_style = ParagraphStyle(
        "Heading",
        parent=styles["Heading2"],
        fontSize=12,
        leading=14,
        spaceBefore=6,
        spaceAfter=6,
    )
    bullet_style = ParagraphStyle(
        "Bullet",
        parent=body_style,
        leftIndent=12,
        firstLineIndent=-8,
    )

    doc = SimpleDocTemplate(
        str(OUTPUT_PDF),
        pagesize=letter,
        rightMargin=0.9 * inch,
        leftMargin=0.9 * inch,
        topMargin=0.8 * inch,
        bottomMargin=0.8 * inch,
        title=TITLE,
        author=AUTHOR,
    )

    story = [
        Paragraph(TITLE, title_style),
        Paragraph(SUBTITLE, subtitle_style),
        Paragraph(f"{AUTHOR}<br/>{DATE}", meta_style),
        Spacer(1, 0.05 * inch),
    ]

    text = normalize_text(extract_source_text())
    for block in split_blocks(text):
        block_type = classify_block(block)
        safe = (
            block.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )
        if block_type == "heading":
            story.append(Paragraph(safe, heading_style))
        elif block_type == "bullet":
            story.append(Paragraph(safe.replace("•", "&#8226;"), bullet_style))
        else:
            story.append(Paragraph(safe, body_style))

    doc.build(story)


if __name__ == "__main__":
    build_pdf()
