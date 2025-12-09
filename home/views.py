from django.shortcuts import render, redirect, get_object_or_404
from .forms import PromptSubmissionForm
from .models import PromptSubmission

#Render homepage
def home(request):
    return render(request, 'home/home.html')

#Render
def team(request):
    return render(request, 'home/team.html')

#Render homepage
def hr(request):
    if request.method == "POST":
        form = PromptSubmissionForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            prompt = form.cleaned_data["prompt"]
            score = score_prompt(prompt)["total"]
            
            submission = form.save(commit=False)
            submission.score = score
            submission.save()
            
            return redirect("result", pk=submission.pk)
    else:
        form = PromptSubmissionForm()

    return render(request, "home/hr.html", {"form": form})

#Render homepage
def da(request):
    if request.method == "POST":
        form = PromptSubmissionForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            prompt = form.cleaned_data["prompt"]
            score = score_prompt(prompt)["total"]
            
            submission = form.save(commit=False)
            submission.score = score
            submission.save()
            return redirect("result", pk=submission.pk)
    else:
        form = PromptSubmissionForm()

    return render(request, "home/da.html", {"form": form})

#Render homepage
def ms(request):
    if request.method == "POST":
        form = PromptSubmissionForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            prompt = form.cleaned_data["prompt"]
            score = score_prompt(prompt)["total"]
            
            submission = form.save(commit=False)
            submission.score = score
            submission.save()
            return redirect("result", pk=submission.pk)
    else:
        form = PromptSubmissionForm()

    return render(request, "home/ms.html", {"form": form})

#Render homepage
def pd(request):
    if request.method == "POST":
        form = PromptSubmissionForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            prompt = form.cleaned_data["prompt"]
            score = score_prompt(prompt)["total"]
            
            submission = form.save(commit=False)
            submission.score = score
            submission.save()
            return redirect("result", pk=submission.pk)
    else:
        form = PromptSubmissionForm()

    return render(request, "home/pd.html", {"form": form})

def cs(request):
    if request.method == "POST":
        form = PromptSubmissionForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            prompt = form.cleaned_data["prompt"]
            score = score_prompt(prompt)["total"]
            
            submission = form.save(commit=False)
            submission.score = score
            submission.save()
            return redirect("result", pk=submission.pk)
    else:
        form = PromptSubmissionForm()

    return render(request, "home/cs.html", {"form": form})

def cw(request):
    if request.method == "POST":
        form = PromptSubmissionForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            prompt = form.cleaned_data["prompt"]
            score = score_prompt(prompt)["total"]
            
            submission = form.save(commit=False)
            submission.score = score
            submission.save()
            return redirect("result", pk=submission.pk)
    else:
        form = PromptSubmissionForm()

    return render(request, "home/cw.html", {"form": form})

def it(request):
    if request.method == "POST":
        form = PromptSubmissionForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            prompt = form.cleaned_data["prompt"]
            score = score_prompt(prompt)["total"]
            
            submission = form.save(commit=False)
            submission.score = score
            submission.save()
            return redirect("result", pk=submission.pk)
    else:
        form = PromptSubmissionForm()

    return render(request, "home/it.html", {"form": form})

# views.py
import random
from django.shortcuts import redirect

def random_role(request):
    routes = [
        'hr',
        'da',
        'ms',
        'pd',
        'cs',
        'cw',
        'it',
    ]

    selected = random.choice(routes)
    return redirect(selected)


import re

MAX_SUBSCORE = 250


def _clamp01(x: float) -> float:
    return max(0.0, min(1.0, x))


def score_prompt(prompt: str) -> dict:
    """
    Score a prompt across:
      - persona
      - task
      - context
      - format

    Each subscore is 0–250, total is 0–1000.
    Uses simple heuristics (no external NLP libs).
    """
    text = (prompt or "").strip()
    if not text:
        return {
            "persona": 0,
            "task": 0,
            "context": 0,
            "format": 0,
            "total": 0,
        }

    lower = text.lower()
    tokens = re.findall(r"\b\w+\b", lower)
    num_tokens = max(len(tokens), 1)  # avoid divide-by-zero

    # --------------------------------------------------
    # 1) Persona score
    # --------------------------------------------------
    persona_score = 0.0

    # Strong persona markers (EN + CY)
    persona_markers = [
        # English
        "you are",
        "act as",
        "pretend to be",
        "take the role of",
        "from the perspective of",
        "as an hr manager",
        "as a data analyst",
        "as a marketing strategist",
        "as a product designer",
        "as a customer support agent",
        "as a copywriter",
        "as an it specialist",
    ]
    welsh_persona_markers = [
        # “you are / act as / take the role…”
        "rwyt ti'n", "rwyt ti yn",
        "rydych chi'n", "rydych chi yn",
        "gweithredu fel",
        "ymddwyn fel",
        "cymryd rôl",
        "cymryd y rôl",
        "o safbwynt",
        # specific roles
        "fel rheolwr adnoddau dynol",
        "fel dadansoddwr data",
        "fel strategaethydd marchnata",
        "fel dylunydd cynnyrch",
        "fel asiant cymorth cwsmeriaid",
        "fel ysgrifennwr copi",
        "fel arbenigwr tg",
    ]
    persona_markers += welsh_persona_markers

    if any(m in lower for m in persona_markers):
        persona_score += 0.6

    # Role-like words (weak evidence) EN + CY
    role_keywords = [
        # English
        "manager",
        "analyst",
        "strategist",
        "designer",
        "support",
        "agent",
        "copywriter",
        "developer",
        "specialist",
        "engineer",
        "team lead",
        "stakeholder",
        "executive",
        # Welsh
        "rheolwr",
        "dadansoddwr",
        "strategaethydd",
        "dylunydd",
        "cymorth",
        "asiant",
        "datblygwr",
        "arbenigwr",
        "peiriannydd",
        "arweinydd tîm",
        "rhanddeiliad",
        "uwch dîm",
    ]
    role_hits = sum(1 for w in role_keywords if w in lower)
    persona_score += min(role_hits / 5.0, 0.3)  # cap at +0.3

    # Audience hints (“for my team”, “for customers”, etc.) EN + CY
    audience_markers = [
        # English
        "for my team",
        "for our team",
        "for stakeholders",
        "for executives",
        "for leadership",
        "for customers",
        "for clients",
        "for users",
        "for non-technical",
        # Welsh
        "ar gyfer fy nhîm",
        "ar gyfer ein tîm",
        "ar gyfer rhanddeiliaid",
        "ar gyfer uwch dîm",
        "ar gyfer arweinwyr",
        "ar gyfer cwsmeriaid",
        "ar gyfer cleientiaid",
        "ar gyfer defnyddwyr",
        "ar gyfer pobl ddi-dechnegol",
        "ar gyfer cynulleidfa nad yw'n dechnegol",
    ]
    if any(m in lower for m in audience_markers):
        persona_score += 0.1

    persona_score = _clamp01(persona_score)
    persona_points = int(round(persona_score * MAX_SUBSCORE))

    # --------------------------------------------------
    # 2) Task score
    # --------------------------------------------------
    task_score = 0.0

    # Imperative verbs / task verbs EN + CY
    task_verbs = [
        # English
        "write",
        "draft",
        "summarise",
        "summarize",
        "explain",
        "create",
        "generate",
        "outline",
        "describe",
        "compose",
        "produce",
        "design",
        # Welsh
        "ysgrifennu",
        "ysgrifennwch",
        "drafftio",
        "esbonio",
        "creu",
        "cynhyrchu",
        "amlinellu",
        "disgrifio",
        "dylunio",
    ]
    task_targets = [
        # English
        "email",
        "report",
        "summary",
        "landing page",
        "post",
        "announcement",
        "plan",
        "proposal",
        "presentation",
        "dashboard explanation",
        # Welsh
        "e-bost",
        "adroddiad",
        "crynodeb",
        "tudalen lanio",
        "cyhoeddiad",
        "cynllun",
        "cynnig",
        "cyflwyniad",
        "esboniad dangosfwrdd",
        "dangosfwrdd",
    ]

    verb_hits = sum(1 for v in task_verbs if v in lower)
    target_hits = sum(1 for t in task_targets if t in lower)

    task_score += min(verb_hits / 3.0, 0.6)    # clear instruction verbs
    task_score += min(target_hits / 2.0, 0.3)  # specific deliverables

    # Presence of “so that…”, “in order to…” (EN + CY) often clarifies purpose
    if (
        "so that" in lower
        or "in order to" in lower
        or "fel bod" in lower
        or "er mwyn" in lower
    ):
        task_score += 0.1

    task_score = _clamp01(task_score)
    task_points = int(round(task_score * MAX_SUBSCORE))

    # --------------------------------------------------
    # 3) Context score
    # --------------------------------------------------
    context_score = 0.0

    # Length: very short prompts rarely have much context
    length_factor = min(num_tokens / 200.0, 1.0)  # 0–1
    context_score += 0.4 * length_factor

    # Numbers, dates, timeframes = more concrete context
    has_number = bool(re.search(r"\d", text))
    time_markers = [
        # English
        "today",
        "tomorrow",
        "next week",
        "this month",
        "next month",
        "q1",
        "q2",
        "q3",
        "q4",
        "in two weeks",
        "by the end of",
        # Welsh
        "heddiw",
        "yfory",
        "wythnos nesaf",
        "y mis hwn",
        "y mis nesaf",
        "mewn pythefnos",
        "erbyn diwedd",
    ]
    if has_number:
        context_score += 0.15
    if any(m in lower for m in time_markers):
        context_score += 0.15

    # Domain-ish words (very rough heuristic) EN + a few CY
    domain_keywords = [
        # English
        "saas",
        "dashboard",
        "onboarding",
        "campaign",
        "kpi",
        "metrics",
        "dataset",
        "survey",
        "workshop",
        "stakeholders",
        "leadership team",
        "customer segment",
        "conversion",
        "churn",
        "ux",
        "ui",
        "vpn",
        "two-factor",
        "authentication",
        "file storage",
        # Welsh domain-ish
        "holiadur",
        "gweithdy",
        "rhanddeiliaid",
        "segment cwsmer",
        "tîm arweinyddiaeth",
    ]
    domain_hits = sum(1 for w in domain_keywords if w in lower)
    context_score += min(domain_hits / 5.0, 0.3)

    context_score = _clamp01(context_score)
    context_points = int(round(context_score * MAX_SUBSCORE))

    # --------------------------------------------------
    # 4) Format score
    # --------------------------------------------------
    format_score = 0.0

    # Structural hints: bullet lists, numbered steps
    has_bullets = any(line.strip().startswith(("-", "*", "•")) for line in text.splitlines())
    has_numbered_list = any(re.match(r"^\s*\d+[\).]", line) for line in text.splitlines())
    if has_bullets:
        format_score += 0.25
    if has_numbered_list:
        format_score += 0.25

    # Explicit format instructions EN + CY
    format_markers = [
        # English
        "use bullet points",
        "use numbered steps",
        "output as",
        "format as",
        "structure it as",
        "in this format:",
        "table with",
        "json",
        "markdown",
        "sections:",
        "headline, subheading",
        # Welsh
        "defnyddio bwled",
        "defnyddio pwyntiau bwled",
        "camau wedi'u rhifo",
        "fformatio fel",
        "trefnu fel",
        "yn y fformat hwn",
        "tabl gyda",
        "adrannau:",
    ]
    if any(m in lower for m in format_markers):
        format_score += 0.3

    # Tone / style constraints (still a kind of formatting) EN + CY
    tone_markers = [
        # English
        "tone should be",
        "in a professional tone",
        "in a friendly tone",
        "in a formal tone",
        "keep the tone",
        "make the tone",
        "concise",
        "no jargon",
        "avoid buzzwords",
        "limit the length to",
        "no longer than",
        # Welsh
        "dylai'r naws fod",
        "mewn naws broffesiynol",
        "mewn naws gyfeillgar",
        "mewn naws ffurfiol",
        "cadw'r naws",
        "gwnewch y naws",
        "cryno",
        "heb jargon",
        "osgoi geiriau ffansi",
        "cyfyngu hyd y testun i",
        "dim hirach na",
    ]
    if any(m in lower for m in tone_markers):
        format_score += 0.2

    format_score = _clamp01(format_score)
    format_points = int(round(format_score * MAX_SUBSCORE))

    # --------------------------------------------------
    # Total
    # --------------------------------------------------
    total = persona_points + task_points + context_points + format_points

    return {
        "total": total,
    }
    
def leaderboard(request):
    # Order by score (high → low), then newest first if tied
    entries = (
        PromptSubmission.objects
        .order_by("-score", "-id")[:20]
    )

    return render(request, "home/leaderboard.html", {"entries": entries})

def result(request, pk):
    submission = get_object_or_404(PromptSubmission, pk=pk)
    scores = score_prompt(submission.prompt)

    return render(request, "home/result.html", {
        "submission": submission,
        "scores": scores,
    })