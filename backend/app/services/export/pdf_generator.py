from pathlib import Path
import json
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

BASE_DIR = Path(__file__).resolve().parents[3]
FONT_DIR = BASE_DIR / "fonts"
print("BASE_DIR:", BASE_DIR)
print("FONT_DIR:", FONT_DIR)
print(FONT_DIR)
print((FONT_DIR / "NotoSansDevanagari-Regular.ttf").exists())
print((FONT_DIR / "NotoSansGujarati-Regular.ttf").exists())

pdfmetrics.registerFont(
    TTFont(
        "HindiFont",
        str(FONT_DIR / "NotoSansDevanagari-Regular.ttf")
    )
)

pdfmetrics.registerFont(
    TTFont(
        "GujaratiFont",
        str(FONT_DIR / "NotoSansGujarati-Regular.ttf")
    )
)

def load_json(value):
    if not value:
        return []

    if isinstance(value, list):
        return value

    try:
        return json.loads(value)
    except:
        return []


def add_heading(story, text, styles):
    story.append(Spacer(1, 0.18 * inch))
    story.append(Paragraph(f"<b>{text}</b>", styles["Heading2"]))
    story.append(Spacer(1, 0.05 * inch))


def add_list(story, items, styles):
    if not items:
        return

    for item in items:

        if isinstance(item, dict):

            task = item.get("task", "")
            owner = item.get("owner", "")
            deadline = item.get("deadline", "")

            line = f"• <b>{task}</b>"

            if owner:
                line += f"<br/>Owner: {owner}"

            if deadline:
                line += f"<br/>Deadline: {deadline}"

            story.append(Paragraph(line, styles["BodyText"]))
            story.append(Spacer(1, 0.05 * inch))

        else:
            story.append(
                Paragraph(f"• {item}", styles["BodyText"])
            )


def generate_pdf(meeting):

    pdf_path = OUTPUT_DIR / f"meeting_{meeting.id}.pdf"

    doc = SimpleDocTemplate(
        str(pdf_path),
        rightMargin=40,
        leftMargin=40,
        topMargin=45,
        bottomMargin=45
    )

    styles = getSampleStyleSheet()
    transcript_style = ParagraphStyle(
    "TranscriptStyle",
    parent=styles["BodyText"],
    fontName="HindiFont",
    fontSize=10,
    leading=16,
)

    styles["Title"].alignment = TA_CENTER

    story = []

    # TITLE

    story.append(
        Paragraph(
            "<b>MEETING MINUTES</b>",
            styles["Title"]
        )
    )

    story.append(Spacer(1, 0.25 * inch))

    # BASIC DETAILS

    story.append(
        Paragraph(
            f"<b>Meeting Title:</b> {meeting.title}",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Meeting Type:</b> {meeting.meeting_type or 'N/A'}",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Sentiment:</b> {meeting.sentiment or 'N/A'}",
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 0.25 * inch))

    # SUMMARY

    add_heading(story, "Executive Summary", styles)

    summary = meeting.summary

    try:
        if isinstance(summary, str):
            summary = json.loads(summary)
    except Exception:
        pass

    if isinstance(summary, dict):

        if summary.get("meeting_objective"):
            story.append(
                Paragraph(
                    f"<b>Meeting Objective:</b><br/>{summary['meeting_objective']}",
                    styles["BodyText"],
                )
            )
            story.append(Spacer(1, 0.1 * inch))

        if summary.get("main_discussion"):
            story.append(
                Paragraph(
                    f"<b>Main Discussion:</b><br/>{summary['main_discussion']}",
                    styles["BodyText"],
                )
            )
            story.append(Spacer(1, 0.1 * inch))

        conclusions = summary.get("important_conclusions", [])

        if conclusions:
            story.append(
                Paragraph("<b>Important Conclusions:</b>", styles["BodyText"])
            )

            if isinstance(conclusions, list):
                for item in conclusions:
                    story.append(
                        Paragraph(f"• {item}", styles["BodyText"])
                    )
            else:
                story.append(
                    Paragraph(conclusions, styles["BodyText"])
                )

            story.append(Spacer(1, 0.1 * inch))

        if summary.get("final_outcome"):
            story.append(
                Paragraph(
                    f"<b>Final Outcome:</b><br/>{summary['final_outcome']}",
                    styles["BodyText"],
                )
            )

    else:

        story.append(
            Paragraph(str(summary), styles["BodyText"])
        )

    # PARTICIPANTS

    participants = load_json(meeting.participants)

    if participants:
        add_heading(story, "Participants", styles)
        add_list(story, participants, styles)

    # KEY POINTS

    key_points = load_json(meeting.key_points)

    if key_points:
        add_heading(story, "Key Discussion Points", styles)
        add_list(story, key_points, styles)

    # DECISIONS

    decisions = load_json(meeting.decisions)

    if decisions:
        add_heading(story, "Decisions Made", styles)
        add_list(story, decisions, styles)

    # ACTION ITEMS

    action_items = load_json(meeting.action_items)

    if action_items:
        add_heading(story, "Action Items", styles)
        add_list(story, action_items, styles)

    # RISKS

    risks = load_json(meeting.risks)

    if risks:
        add_heading(story, "Risks & Concerns", styles)
        add_list(story, risks, styles)

    # QUESTIONS

    questions = load_json(meeting.questions)

    if questions:
        add_heading(story, "Open Questions", styles)
        add_list(story, questions, styles)

    # NEXT STEPS

    next_steps = load_json(meeting.next_steps)

    if next_steps:
        add_heading(story, "Next Steps", styles)
        add_list(story, next_steps, styles)

    # TRANSCRIPT

    transcript = meeting.speaker_transcript or meeting.transcript

    if transcript.strip():

        add_heading(story, "Complete Meeting Transcript", styles)

        transcript = transcript.replace("\n", "<br/>")

        story.append(
    Paragraph(
        transcript,
        transcript_style
    )
)

    doc.build(story)

    return str(pdf_path)