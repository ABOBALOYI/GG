import requests
import time
import hashlib
import json
import logging
import io
from typing import List, Dict, Any, Optional
from bs4 import BeautifulSoup
import PyPDF2
import google.generativeai as genai
from django.conf import settings
from datetime import date

logger = logging.getLogger('opportunities.scraper')

class BaseScraper:
    SOURCE_NAME = ""
    SEED_URLS = []
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'GrantGuideSA-Scraper/1.0 (Polite Scraper for Business Funding Opportunities)'
        })
        self.api_key = getattr(settings, 'GEMINI_API_KEY', None)
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
        else:
            self.model = None
            logger.warning("GEMINI_API_KEY not found in settings. AI extraction will be disabled.")

    def fetch_url(self, url: str) -> Optional[str]:
        """Fetch URL content with rate limiting and error handling."""
        try:
            time.sleep(1)  # Polite delay
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return response.text
        except Exception as e:
            logger.error(f"Error fetching {url}: {e}")
            return None

    def extract_pdf_text(self, pdf_url: str) -> str:
        """Download and extract text from a PDF."""
        try:
            response = self.session.get(pdf_url, timeout=60)
            response.raise_for_status()
            pdf_file = io.BytesIO(response.content)
            reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            logger.error(f"Error extracting PDF {pdf_url}: {e}")
            return ""

    def get_content_hash(self, text: str) -> str:
        """Generate a hash for change detection."""
        return hashlib.sha256(text.encode('utf-8')).hexdigest()

    def ai_extract_structured_data(self, raw_content: str, source_url: str) -> List[Dict[str, Any]]:
        """Use Gemini to extract funding opportunities from raw content."""
        if not self.model:
            return []

        prompt = f"""
        Extract business funding opportunities from the following content provided from {source_url}.
        The content might contain multiple opportunities.
        
        Rules:
        1. Respect legal/ethical boundaries (don't guess if not present).
        2. No personal data collection.
        3. Never guess. If fields are missing, set to null/unknown.
        
        Required JSON format per record:
        {{
          "record_type": "FundingOpportunity" or "FundingProduct",
          "title": "Full name of the grant/loan",
          "funder_name": "Organization name",
          "funder_type": "Gov / DFI / Private / NGO-Donor",
          "funding_type": "Grant / Loan / Equity / Mixed / CompetitionPrize",
          "description_short": "max 300 chars, original wording",
          "industry_tags": ["list", "of", "industries"],
          "province_tags": ["list", "of", "provinces" or "National"],
          "business_stage": "Startup / SME / Established / Any",
          "eligibility_bullets": ["bullet 1", "bullet 2"],
          "funding_amount_min": number or null,
          "funding_amount_max": number or null,
          "deadline_date": "YYYY-MM-DD" or null,
          "is_rolling": boolean,
          "required_documents_bullets": ["doc 1", "doc 2"],
          "application_steps": ["Step 1: ...", "Step 2: ..."],
          "official_apply_url": "URL to apply",
          "source_url": "{source_url}"
        }}

        Return a JSON list of objects. If no opportunities are found, return [].
        
        Content:
        {raw_content[:15000]}  # Truncate to avoid token limits
        """

        try:
            response = self.model.generate_content(prompt)
            # Find the JSON part in the response
            content = response.text
            json_start = content.find("[")
            json_end = content.rfind("]") + 1
            if json_start != -1 and json_end != -1:
                data = json.loads(content[json_start:json_end])
                
                # Add metadata
                for record in data:
                    record['source_name'] = self.SOURCE_NAME
                    record['last_verified_date'] = date.today().isoformat()
                    record['raw_content_hash'] = self.get_content_hash(raw_content)
                    
                    # Basic validation or post-processing
                    if not record.get('official_apply_url'):
                        record['official_apply_url'] = source_url
                        
                    # Status logic
                    if not record.get('deadline_date') and not record.get('is_rolling'):
                        record['status'] = 'DraftNeedsReview'
                    else:
                        record['status'] = 'Active'
                        
                return data
        except Exception as e:
            logger.error(f"AI Extraction error for {source_url}: {e}")
            return []

    def scrape(self) -> List[Dict[str, Any]]:
        """Main entry point for scraping. Should be overridden by subclasses."""
        results = []
        for url in self.SEED_URLS:
            content = self.fetch_url(url)
            if content:
                # Basic implementation: Extract everything from the seed page
                # Subclasses might crawl child pages
                extracted = self.ai_extract_structured_data(content, url)
                results.extend(extracted)
        return results
