"""
JSON exporter for outputting scraped records.
"""
import json
import sys
from datetime import date
from decimal import Decimal
from pathlib import Path
from typing import Optional, TextIO

from .models import NormalisedOpportunity


class JsonExporter:
    """Exports normalised records to JSON format."""
    
    def export(
        self,
        records: list[NormalisedOpportunity],
        output_path: Optional[str] = None
    ) -> str:
        """
        Export records to JSON.
        
        Args:
            records: List of normalised opportunities to export.
            output_path: File path to write JSON. If None, returns JSON string.
            
        Returns:
            JSON string of exported records.
        """
        json_records = [self._record_to_dict(r) for r in records]
        json_str = json.dumps(json_records, indent=2, default=self._json_serializer)
        
        if output_path:
            Path(output_path).write_text(json_str)
        
        return json_str
    
    def export_to_stream(
        self,
        records: list[NormalisedOpportunity],
        stream: TextIO = sys.stdout
    ) -> None:
        """
        Export records to a stream (stdout or file handle).
        
        Args:
            records: List of normalised opportunities to export.
            stream: Output stream (default: stdout).
        """
        json_str = self.export(records)
        stream.write(json_str)
        stream.write('\n')
    
    def _record_to_dict(self, record: NormalisedOpportunity) -> dict:
        """Convert normalised record to JSON-serializable dict."""
        return {
            "record_type": record.record_type.value,
            "title": record.title,
            "funder_name": record.funder_name,
            "funder_type": record.funder_type.value if record.funder_type else None,
            "funding_type": record.funding_type.value if record.funding_type else None,
            "description_short": record.description_short,
            "industry_tags": record.industry_tags,
            "province_tags": record.province_tags,
            "business_stage": record.business_stage.value if record.business_stage else None,
            "eligibility_bullets": record.eligibility_bullets,
            "funding_amount_min": float(record.funding_amount_min) if record.funding_amount_min else None,
            "funding_amount_max": float(record.funding_amount_max) if record.funding_amount_max else None,
            "deadline_date": record.deadline_date.isoformat() if record.deadline_date else None,
            "is_rolling": record.is_rolling,
            "required_documents_bullets": record.required_documents_bullets,
            "application_steps": record.application_steps,
            "official_apply_url": record.official_apply_url,
            "source_url": record.source_url,
            "source_name": record.source_name,
            "last_verified_date": record.last_verified_date.isoformat() if record.last_verified_date else None,
            "status": record.status.value if record.status else None,
            "raw_content_hash": record.raw_content_hash,
        }
    
    def _json_serializer(self, obj):
        """Custom JSON serializer for non-standard types."""
        if isinstance(obj, date):
            return obj.isoformat()
        if isinstance(obj, Decimal):
            return float(obj)
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


# JSON Schema for validation
JSON_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "array",
    "items": {
        "type": "object",
        "required": [
            "record_type", "title", "funder_name", "funding_type",
            "description_short", "industry_tags", "province_tags", "business_stage",
            "eligibility_bullets", "is_rolling", "required_documents_bullets",
            "application_steps", "official_apply_url", "source_url", "source_name",
            "last_verified_date", "status", "raw_content_hash"
        ],
        "properties": {
            "record_type": {
                "type": "string",
                "enum": ["FundingOpportunity", "FundingProduct"]
            },
            "title": {"type": "string", "maxLength": 255},
            "funder_name": {"type": "string", "maxLength": 255},
            "funder_type": {
                "type": ["string", "null"],
                "enum": ["Gov", "DFI", "Private", "NGO-Donor", "Mixed", None]
            },
            "funding_type": {
                "type": ["string", "null"],
                "enum": ["Grant", "Loan", "Equity", "Mixed", "CompetitionPrize", None]
            },
            "description_short": {"type": "string", "maxLength": 300},
            "industry_tags": {
                "type": "array",
                "items": {"type": "string"}
            },
            "province_tags": {
                "type": "array",
                "items": {"type": "string"}
            },
            "business_stage": {
                "type": ["string", "null"],
                "enum": ["Startup", "SME", "Established", "Any", None]
            },
            "eligibility_bullets": {
                "type": "array",
                "items": {"type": "string"}
            },
            "funding_amount_min": {"type": ["number", "null"]},
            "funding_amount_max": {"type": ["number", "null"]},
            "deadline_date": {
                "type": ["string", "null"],
                "format": "date"
            },
            "is_rolling": {"type": "boolean"},
            "required_documents_bullets": {
                "type": "array",
                "items": {"type": "string"}
            },
            "application_steps": {
                "type": "array",
                "items": {"type": "string"}
            },
            "official_apply_url": {"type": "string"},
            "source_url": {"type": "string"},
            "source_name": {"type": "string"},
            "last_verified_date": {"type": ["string", "null"], "format": "date"},
            "status": {
                "type": ["string", "null"],
                "enum": ["Active", "Expired", "DraftNeedsReview", None]
            },
            "raw_content_hash": {"type": "string"}
        }
    }
}
