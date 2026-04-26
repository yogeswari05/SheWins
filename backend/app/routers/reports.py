from __future__ import annotations

from collections import Counter
import io
from datetime import date

from fastapi import APIRouter, Depends, Response
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet

from app.dependencies import get_user_id
from app.models import schemas
from app.services import db
from app.services.pcod_risk import compute_pcod_risk
from app.services import ml_predictor

router = APIRouter(prefix="/api/reports", tags=["reports"])


@router.get("/doctor", response_class=Response)
def doctor_pdf(user_id: str = Depends(get_user_id)):
    rows = sorted(
        db.list_cycles(user_id), key=lambda c: c.get("start_date", "")
    )
    lengths = schemas.cycle_lengths_from_rows(rows)
    risk = compute_pcod_risk(rows)
    pred = ml_predictor.predict_next_cycles(lengths)

    sym_counter: Counter[str] = Counter()
    for c in rows:
        for s in c.get("symptoms") or []:
            if isinstance(s, str) and s.strip():
                sym_counter[s.strip().lower()] += 1

    alerts: list[str] = []
    if risk.get("risk_score", 0) > 60:
        alerts.append(
            "Risk score > 60% — consider a gynecologist evaluation (non-diagnostic)."
        )
    for L in lengths:
        if L > 35:
            alerts.append(f"One recorded gap was {L} days (>35).")
            break
    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf,
        pagesize=letter,
        title="Elite Her — cycle report",
    )
    styles = getSampleStyleSheet()
    story = [
        Paragraph(
            "<b>Elite Her — Menstrual Health and PCOD Risk Report</b> (Non-diagnostic)",
            styles["Title"],
        ),
        Spacer(1, 12),
        Paragraph(
            f"<b>Report date</b> {date.today().isoformat()}<br/>"
            f"<b>User reference</b> (hashed) {user_id[:8]}…<br/>"
            f"<b>Disclaimer</b> This report is for discussion with a clinician and does not constitute a medical diagnosis.",
            styles["BodyText"],
        ),
        Spacer(1, 12),
    ]

    tdata = [
        [
            "Start",
            "End",
            "Flow",
            "Symptoms",
        ]
    ]
    for c in rows[-24:]:  # last 24 cycles
        tdata.append(
            [
                c.get("start_date", "")[:10],
                (c.get("end_date") or "")[:10] or "—",
                c.get("flow", ""),
                ", ".join(c.get("symptoms") or []),
            ]
        )
    if len(tdata) == 1:
        tdata.append(["(no data)", "—", "—", "—"])
    t = Table(tdata, repeatRows=1)
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#6b2d5c")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ]
        )
    )
    story.append(t)
    story.append(Spacer(1, 16))

    # Symptom summary (top 10)
    if sym_counter:
        story.append(Paragraph("<b>Symptom summary (top)</b>", styles["Heading2"]))
        sdata = [["Symptom", "Count"]]
        for k, v in sym_counter.most_common(10):
            sdata.append([k, str(v)])
        st = Table(sdata, repeatRows=1)
        st.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2a1b2d")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                    ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
                ]
            )
        )
        story.append(st)
        story.append(Spacer(1, 12))

    story.append(Paragraph(f"<b>PCOD/PCOS risk score (0-100):</b> {risk.get('risk_score', 0)}", styles["Heading2"]))
    story.append(Paragraph(f"<b>Level:</b> {risk.get('level', '')}", styles["BodyText"]))
    story.append(Paragraph(f"<b>Recommendation:</b> {risk.get('recommendation', '')}", styles["BodyText"]))
    story.append(Paragraph(
        f"<b>Observed cycle lengths (days, consecutive):</b> {lengths}",
        styles["BodyText"],
    ))

    if alerts:
        story.append(Spacer(1, 10))
        story.append(Paragraph("<b>Early-warning alerts</b> (non-diagnostic)", styles["Heading2"]))
        for a in alerts[:5]:
            story.append(Paragraph(f"• {a}", styles["BodyText"]))

    # ML prediction summary
    next_cycles = (pred or {}).get("next_cycles") or []
    if next_cycles:
        story.append(Spacer(1, 10))
        story.append(Paragraph("<b>Next cycle predictions</b> (estimates)", styles["Heading2"]))
        pdata = [["Cycle", "Predicted length (days)", "Interval", "Confidence"]]
        for c in next_cycles[:3]:
            lo = c.get("interval_low")
            hi = c.get("interval_high")
            interval = f"{lo}–{hi}" if lo is not None and hi is not None else "—"
            conf = c.get("confidence")
            pdata.append(
                [
                    str(c.get("cycle_index") or ""),
                    str(c.get("predicted_length_days") or ""),
                    interval,
                    str(conf) if conf is not None else "—",
                ]
            )
        pt = Table(pdata, repeatRows=1)
        pt.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2a1b2d")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                    ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
                ]
            )
        )
        story.append(pt)
    doc.build(story)
    buf.seek(0)
    return Response(
        content=buf.read(),
        media_type="application/pdf",
        headers={
            "Content-Disposition": "attachment; filename=elite-her-doctor-report.pdf"
        },
    )
