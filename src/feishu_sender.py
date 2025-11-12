"""Feishu (Lark) sender for delivering digest summaries via webhook."""

from __future__ import annotations

import base64
import hashlib
import hmac
import time
from datetime import datetime
from typing import Any, Dict, List, Optional

import httpx


class FeishuSender:
    """Send arxiv digest summaries to a Feishu bot via webhook."""

    def __init__(
        self,
        webhook_url: str,
        secret: Optional[str] = None,
        max_papers: int = 5,
        timeout: float = 10.0
    ):
        """Initialise the Feishu sender."""

        self.webhook_url = webhook_url.strip()
        self.secret = (secret or "").strip()
        self.max_papers = max(1, max_papers)
        self.timeout = timeout

    def send_digest(self, papers: List[Dict[str, Any]]) -> bool:
        """Send the digest message to Feishu."""

        message = self._build_message(papers)
        payload = self._build_payload(message)

        try:
            response = httpx.post(
                self.webhook_url,
                json=payload,
                timeout=self.timeout
            )
            response.raise_for_status()

            # Feishu returns {"StatusCode":0,"StatusMessage":"success"}
            # for incoming webhook requests.
            data = response.json()
            status_code = data.get("StatusCode", data.get("code", -1))

            if status_code == 0:
                print("Feishu notification sent successfully")
                return True

            message = data.get("msg") or data.get("StatusMessage")
            print(
                "Failed to send Feishu notification: "
                f"status={status_code}, message={message}"
            )
        except Exception as exc:  # pragma: no cover - network issues
            print(f"Failed to send Feishu notification: {exc}")

        return False

    def _build_payload(self, message: str) -> Dict[str, Any]:
        """Construct the webhook payload."""

        payload: Dict[str, Any] = {
            "msg_type": "text",
            "content": {"text": message}
        }

        if self.secret:
            timestamp = str(int(time.time()))
            payload.update(
                {
                    "timestamp": timestamp,
                    "sign": self._sign(timestamp)
                }
            )

        return payload

    def _build_message(self, papers: List[Dict[str, Any]]) -> str:
        """Create a human readable message for Feishu."""

        date_str = datetime.now().strftime("%Y-%m-%d")

        if not papers:
            return (
                f"ArXiv Daily Digest - {date_str}\n\n"
                "No papers matched your interests today."
            )

        lines = [
            f"ArXiv Daily Digest - {date_str}",
            "",
            f"Top {min(len(papers), self.max_papers)} relevant paper(s):"
        ]

        for index, paper in enumerate(papers[: self.max_papers], start=1):
            score = paper.get("relevance_score")
            reason = paper.get("relevance_reason")
            score_str = f" ({score:.1f}/10)" if isinstance(score, (int, float)) else ""

            lines.extend(
                [
                    "",
                    f"{index}. {paper['title']}{score_str}",
                    paper.get("pdf_url") or paper.get("url", ""),
                ]
            )

            if reason:
                lines.append(f"Reason: {reason}")

        lines.append("")
        lines.append("This message was generated automatically.")

        return "\n".join(lines)

    def _sign(self, timestamp: str) -> str:
        """Generate signature for the webhook payload."""

        string_to_sign = f"{timestamp}\n{self.secret}".encode("utf-8")
        secret = self.secret.encode("utf-8")
        digest = hmac.new(secret, string_to_sign, digestmod=hashlib.sha256).digest()
        return base64.b64encode(digest).decode("utf-8")
