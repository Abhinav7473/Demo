"""create principles table and seed Nielsen heuristics + Wickens principles

Revision ID: 0002
Revises: 0001
Create Date: 2026-10-15
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0002"
down_revision: Union[str, None] = "0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

N = "nielsen"
W = "wickens"

# (code, source, category, title, summary, example)
SEED = [
    ("N1", N, "Usability heuristic", "Visibility of system status",
     "Keep people informed about what is going on through timely, appropriate feedback.",
     "A progress bar with a percentage while a file uploads."),
    ("N2", N, "Usability heuristic", "Match between system and the real world",
     "Use words, concepts and conventions familiar to the user rather than internal jargon, and follow real-world order.",
     "A shopping app that uses a cart icon and says \"Checkout\", not \"Commit order transaction\"."),
    ("N3", N, "Usability heuristic", "User control and freedom",
     "People make mistakes; give them a clearly marked way out of unwanted states without a long detour.",
     "An \"Undo\" toast after archiving an email."),
    ("N4", N, "Usability heuristic", "Consistency and standards",
     "Don't make users wonder whether different words, situations or actions mean the same thing; follow platform conventions.",
     "The primary button is always on the right and always the same color across every dialog."),
    ("N5", N, "Usability heuristic", "Error prevention",
     "Better than a good error message is a design that prevents the problem in the first place.",
     "A date picker that greys out past dates when booking a flight."),
    ("N6", N, "Usability heuristic", "Recognition rather than recall",
     "Minimize memory load by making objects, actions and options visible instead of making users remember them.",
     "Showing recent searches when the search box is focused."),
    ("N7", N, "Usability heuristic", "Flexibility and efficiency of use",
     "Provide accelerators that speed up expert use without getting in the way of novices.",
     "Keyboard shortcuts listed next to menu items."),
    ("N8", N, "Usability heuristic", "Aesthetic and minimalist design",
     "Interfaces shouldn't contain information that is irrelevant or rarely needed; every extra unit competes with what matters.",
     "A checkout page that hides the promo-code field behind a small link."),
    ("N9", N, "Usability heuristic", "Help users recognize, diagnose, and recover from errors",
     "Error messages should use plain language, state the problem precisely, and suggest a solution.",
     "\"Password must be at least 12 characters\" shown next to the field, instead of \"Error 422\"."),
    ("N10", N, "Usability heuristic", "Help and documentation",
     "Ideally no docs are needed, but help should be easy to search, focused on the task, and list concrete steps.",
     "Inline \"?\" tooltips that explain a setting in one sentence."),
    ("W1", W, "Perceptual", "Make displays legible (audible)",
     "A display must be readable under the actual viewing conditions: contrast, size, lighting, glare, vibration.",
     "Dashboard warnings sized to be read from the driver's seat at night."),
    ("W2", W, "Perceptual", "Avoid absolute judgment limits",
     "Don't ask users to judge a variable from a single sensory cue (color, size, loudness) with many levels.",
     "Using labeled numbers rather than eight shades of blue to encode severity."),
    ("W3", W, "Perceptual", "Top-down processing",
     "People perceive what they expect; signals that contradict expectations need extra physical evidence.",
     "An unusual instruction like \"Do NOT turn left\" is made louder and repeated."),
    ("W4", W, "Perceptual", "Redundancy gain",
     "Presenting the same message in several forms makes it more likely to be understood correctly.",
     "A traffic light that encodes stop by both color (red) and position (top)."),
    ("W5", W, "Perceptual", "Discriminability",
     "Similar-looking signals get confused; remove needless shared features and highlight the distinguishing ones.",
     "Tall-man lettering on drug labels: hydrOXYzine vs hydrALAzine."),
    ("W6", W, "Mental model", "Principle of pictorial realism",
     "A display should look like the variable it represents.",
     "A thermometer shown as a vertical bar where higher means hotter."),
    ("W7", W, "Mental model", "Principle of the moving part",
     "Moving elements should move in the same direction and pattern as the user's mental model of the real system.",
     "An altimeter indicator that rises as the aircraft climbs."),
    ("W8", W, "Attention", "Minimize information access cost",
     "Keep frequently used information close at hand; every glance, scroll or click costs time and effort.",
     "Pinning the account balance at the top of a banking app."),
    ("W9", W, "Attention", "Proximity compatibility",
     "Information that must be mentally combined should be close together or linked by color, lines or shape.",
     "Placing a chart's legend labels directly on the lines they describe."),
    ("W10", W, "Attention", "Multiple resources",
     "Spreading information across modalities (visual and auditory) lets people process more at once.",
     "Turn-by-turn navigation that speaks directions while the map stays on screen."),
    ("W11", W, "Memory", "Replace memory with visual information (knowledge in the world)",
     "Don't rely on people remembering; put the needed information in the world, balanced against clutter.",
     "A checklist on screen for a multi-step setup process."),
    ("W12", W, "Memory", "Principle of predictive aiding",
     "Displays that predict what will happen let people act proactively instead of reactively.",
     "A GPS showing estimated arrival time and the upcoming turn."),
    ("W13", W, "Memory", "Principle of consistency",
     "Old habits transfer to new displays; keep designs consistent with other displays the user knows.",
     "Using the same icons for save and delete across every app in a suite."),
]


def upgrade() -> None:
    table = op.create_table(
        "principles",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("code", sa.String(length=8), nullable=False, unique=True),
        sa.Column("source", sa.String(length=20), nullable=False),
        sa.Column("category", sa.String(length=60), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("example", sa.Text(), nullable=False),
    )
    keys = ("code", "source", "category", "title", "summary", "example")
    op.bulk_insert(table, [dict(zip(keys, row)) for row in SEED])


def downgrade() -> None:
    op.drop_table("principles")
