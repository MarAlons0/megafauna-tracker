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

    def chat(self, message, sightings_context=''):
        """
        Phase 3 chatbot — answer questions about recent sightings.

        Args:
            message: User question
            sightings_context: Recent sightings summary string

        Returns:
            str: AI response
        """
        if not self.client:
            return "AI assistant is not available."

        system = (
            "You are a wildlife expert assistant for an Alaska road-trip megafauna tracker. "
            "Answer questions about wildlife sightings, conditions, and species behavior. "
            "Be concise and practical — users are viewing this on a phone while traveling."
        )

        context = f"Recent sightings context:\n{sightings_context}\n\n" if sightings_context else ""
        prompt = f"{context}User question: {message}"

        try:
            response = self.client.messages.create(
                model=self.MODEL,
                max_tokens=400,
                system=system,
                messages=[{'role': 'user', 'content': prompt}],
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
