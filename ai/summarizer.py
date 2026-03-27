"""
Claude AI summarization for megafauna tracker.

Three tasks:
1. Bear forecast: weir count + date/season → 2-sentence bear activity prediction
2. Report summarization: raw ADF&G HTML text → structured JSON
3. Chatbot (Phase 3): conversational interface with sighting context
"""

import logging
import os
from datetime import datetime

logger = logging.getLogger(__name__)


class MegafaunaSummarizer:
    """Claude-powered summarization for wildlife conditions."""

    MODEL = 'claude-sonnet-4-6'

    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
        self.client = None
        self._init_client()

    def _init_client(self):
        if not self.api_key:
            logger.warning("ANTHROPIC_API_KEY not set — AI features disabled")
            return
        try:
            from anthropic import Anthropic
            self.client = Anthropic(api_key=self.api_key)
            logger.info("Claude client initialized")
        except ImportError:
            logger.error("anthropic package not installed")
        except Exception as e:
            logger.error(f"Claude init error: {e}")

    @property
    def is_available(self):
        return self.client is not None

    def bear_forecast(self, weir_count, escapement_goal, run_name, date=None):
        """
        Generate a 2-sentence bear activity forecast based on salmon run data.

        Args:
            weir_count: Current daily weir count (int)
            escapement_goal: Season escapement goal (int)
            run_name: e.g. 'Russian River Early-Run Sockeye'
            date: datetime object (defaults to today)

        Returns:
            str: 2-sentence forecast, or None on error
        """
        if not self.client:
            return None

        date = date or datetime.utcnow()
        month_name = date.strftime('%B')

        prompt = (
            f"You are a wildlife biologist advising visitors to the Russian River, Alaska. "
            f"Today is {date.strftime('%B %d, %Y')}. "
            f"The {run_name} current daily weir count is {weir_count:,} fish. "
            f"The season escapement goal is {escapement_goal:,}. "
            f"In 2 sentences, give a practical bear activity forecast for anglers and hikers. "
            f"Be direct — mention likely bear density and whether to expect crowded bear activity."
        )

        try:
            response = self.client.messages.create(
                model=self.MODEL,
                max_tokens=200,
                system="You are a wildlife biologist providing concise, practical safety information.",
                messages=[{'role': 'user', 'content': prompt}],
            )
            return self._extract_text(response)
        except Exception as e:
            logger.error(f"Bear forecast error: {e}")
            return None

    def summarize_report(self, raw_text):
        """
        Summarize raw ADF&G report text into structured JSON.

        Args:
            raw_text: Raw HTML-stripped report text

        Returns:
            dict: {'alerts': [], 'sightings': [], 'conditions_summary': ''}
            or None on error
        """
        if not self.client:
            return None

        prompt = (
            f"Extract wildlife and fishing conditions from this ADF&G report. "
            f"Return ONLY valid JSON in exactly this format:\n"
            f'{{"alerts": [], "sightings": [], "conditions_summary": ""}}\n\n'
            f"alerts: list of closures, restrictions, or safety warnings.\n"
            f"sightings: list of notable wildlife sightings mentioned.\n"
            f"conditions_summary: 1-2 sentence plain-English summary.\n\n"
            f"Report text:\n{raw_text[:3000]}"
        )

        try:
            import json
            response = self.client.messages.create(
                model=self.MODEL,
                max_tokens=600,
                system="You are a data extractor. Return only valid JSON, no prose.",
                messages=[{'role': 'user', 'content': prompt}],
            )
            text = self._extract_text(response) or ''
            # Strip markdown code fences if present
            text = text.strip()
            if text.startswith('```'):
                text = text.split('\n', 1)[-1]
                text = text.rsplit('```', 1)[0]
            return json.loads(text.strip())
        except Exception as e:
            logger.error(f"Report summarization error: {e}")
            return None

    def analyze_observations(self, location_name, radius_miles, days,
                              observations, bucket_data, adfg_context=None):
        """
        Generate a wildlife intelligence briefing from iNaturalist observations.

        Args:
            location_name: Human-readable location string
            radius_miles: Search radius in miles
            days: Time window in days
            observations: List of observation dicts from iNaturalist
            bucket_data: List of {period, species: {name: count}} dicts (recent first)
            adfg_context: Optional ADF&G conditions summary string

        Returns:
            str: Markdown-formatted briefing, or None on error
        """
        if not self.client:
            return None

        today = datetime.utcnow().strftime('%B %d, %Y')
        month = datetime.utcnow().strftime('%B')

        # Species totals
        species_counts = {}
        for obs in observations:
            name = obs.get('common_name') or obs.get('species_name', 'Unknown')
            species_counts[name] = species_counts.get(name, 0) + 1

        species_lines = '\n'.join(
            f"  {name}: {count}"
            for name, count in sorted(species_counts.items(), key=lambda x: -x[1])
        )

        # Time-bucketed trends
        bucket_lines = []
        for bucket in bucket_data:
            if bucket.get('species'):
                top = sorted(bucket['species'].items(), key=lambda x: -x[1])
                species_str = ', '.join(f"{s} ({c})" for s, c in top[:8])
                bucket_lines.append(f"  {bucket['period']}: {species_str}")
        trend_text = '\n'.join(bucket_lines) if bucket_lines else '  No time-bucketed data available.'

        adfg_section = f"\nADF&G CONDITIONS REPORT:\n{adfg_context}\n" if adfg_context else ""

        prompt = f"""Today is {today}. Analyze iNaturalist wildlife observations within {radius_miles} miles of {location_name} over the past {days} days.

SPECIES TOTALS ({len(observations)} observations):
{species_lines}

OBSERVATIONS BY PERIOD (most recent first):
{trend_text}
{adfg_section}
Write a wildlife intelligence briefing with exactly these five sections. Be specific — cite actual species names and counts from the data. Avoid generic statements.

**Overview**
2–3 sentences on overall activity level and the dominant species defining this area right now.

**Trends**
Which species are increasing or decreasing recently? Highlight accelerations, sudden appearances, or notable absences. If a species appeared heavily in older periods but not recent ones, flag it.

**Notable Sightings**
Unusual, rare, or geographically interesting records worth highlighting. If nothing stands out, say so briefly.

**Seasonal Context**
Is this pattern expected for {month}? What does the data suggest about the current season?

**Field Notes**
Practical guidance for a visitor: safety-relevant activity (bears especially), best viewing opportunities, anything to be aware of."""

        try:
            response = self.client.messages.create(
                model=self.MODEL,
                max_tokens=1500,
                system=(
                    "You are an expert wildlife naturalist providing concise, data-driven field "
                    "intelligence briefings. No introductory or closing pleasantries. "
                    "Stay grounded in the actual observation data provided."
                ),
                messages=[{'role': 'user', 'content': prompt}],
            )
            return self._extract_text(response)
        except Exception as e:
            logger.error(f"Analysis error: {e}")
            return None

    def chat(self, message, history, observations_context, location_name):
        """
        Multi-turn chat grounded in current observation data.

        Args:
            message: Current user message
            history: List of {role, content} dicts for prior turns (session only)
            observations_context: Pre-formatted string summary of observations
            location_name: Human-readable location string

        Returns:
            str: AI response
        """
        if not self.client:
            return "AI assistant is not available — check ANTHROPIC_API_KEY."

        system = (
            f"You are an expert wildlife naturalist assistant. "
            f"The user is analyzing megafauna observations near {location_name}.\n\n"
            f"Current observation data:\n{observations_context}\n\n"
            "Answer questions based on the observations and your wildlife expertise. "
            "Be practical and concise — the user may be in the field. "
            "When answering beyond the observation data, note that you're drawing on general knowledge."
        )

        messages = list(history) + [{'role': 'user', 'content': message}]

        try:
            response = self.client.messages.create(
                model=self.MODEL,
                max_tokens=600,
                system=system,
                messages=messages,
            )
            return self._extract_text(response)
        except Exception as e:
            logger.error(f"Chat error: {e}")
            return "Unable to respond at this time."

    def _extract_text(self, response):
        if not response or not response.content:
            return None
        parts = []
        for block in response.content:
            if hasattr(block, 'text'):
                parts.append(block.text)
        return '\n'.join(parts).strip()


# Singleton
_summarizer = None


def get_summarizer():
    global _summarizer
    if _summarizer is None:
        _summarizer = MegafaunaSummarizer()
    return _summarizer
