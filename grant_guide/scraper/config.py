"""
Source configuration loader for the Grant Guide Scraper Engine.
"""
import os
from pathlib import Path
from typing import Optional
import yaml

from .models import SourceConfig, SourceType


class ConfigurationError(Exception):
    """Raised when source configuration is invalid."""
    pass


def load_sources(config_path: Optional[str] = None) -> list[SourceConfig]:
    """
    Load approved sources from YAML configuration file.
    
    Args:
        config_path: Path to sources.yaml file. If None, uses default location.
        
    Returns:
        List of SourceConfig objects for all configured sources.
        
    Raises:
        ConfigurationError: If configuration is invalid or missing required fields.
    """
    if config_path is None:
        config_path = Path(__file__).parent / "sources.yaml"
    
    if not os.path.exists(config_path):
        raise ConfigurationError(f"Configuration file not found: {config_path}")
    
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    if not config or 'sources' not in config:
        raise ConfigurationError("Configuration must contain 'sources' key")
    
    sources = []
    for source_data in config['sources']:
        try:
            source = _parse_source_config(source_data)
            sources.append(source)
        except (KeyError, ValueError) as e:
            raise ConfigurationError(
                f"Invalid source configuration for '{source_data.get('source_id', 'unknown')}': {e}"
            )
    
    return sources


def _parse_source_config(data: dict) -> SourceConfig:
    """Parse a single source configuration from dict."""
    required_fields = ['source_id', 'source_name', 'base_url', 'scrape_urls', 
                       'source_type', 'adapter_class']
    
    for field in required_fields:
        if field not in data:
            raise KeyError(f"Missing required field: {field}")
    
    return SourceConfig(
        source_id=data['source_id'],
        source_name=data['source_name'],
        base_url=data['base_url'],
        scrape_urls=data['scrape_urls'],
        source_type=SourceType(data['source_type']),
        adapter_class=data['adapter_class'],
        is_active=data.get('is_active', True),
        rate_limit_seconds=data.get('rate_limit_seconds', 2.0),
        last_scraped=None,
        needs_attention=False,
        consecutive_failures=0
    )


def get_source_by_id(source_id: str, sources: Optional[list[SourceConfig]] = None) -> Optional[SourceConfig]:
    """
    Get a source configuration by its ID.
    
    Args:
        source_id: The unique identifier of the source.
        sources: List of sources to search. If None, loads from default config.
        
    Returns:
        SourceConfig if found, None otherwise.
    """
    if sources is None:
        sources = load_sources()
    
    for source in sources:
        if source.source_id == source_id:
            return source
    return None


def get_active_sources(sources: Optional[list[SourceConfig]] = None) -> list[SourceConfig]:
    """
    Get all active sources.
    
    Args:
        sources: List of sources to filter. If None, loads from default config.
        
    Returns:
        List of active SourceConfig objects.
    """
    if sources is None:
        sources = load_sources()
    
    return [s for s in sources if s.is_active]


def is_approved_source(url: str, sources: Optional[list[SourceConfig]] = None) -> bool:
    """
    Check if a URL belongs to an approved source.
    
    Args:
        url: The URL to check.
        sources: List of sources to check against. If None, loads from default config.
        
    Returns:
        True if URL belongs to an approved source, False otherwise.
    """
    if sources is None:
        sources = load_sources()
    
    for source in sources:
        if url.startswith(source.base_url):
            return True
        for scrape_url in source.scrape_urls:
            if url.startswith(scrape_url.rsplit('/', 1)[0]):
                return True
    return False


# Approved source IDs for quick reference
APPROVED_SOURCE_IDS = [
    # Government
    'dtic', 'dsbd', 'tia', 'nyda', 'sefa', 'idc', 'nef',
    # Provincial
    'gep', 'ecdc', 'dedat',
    # SETA
    'services_seta', 'hwseta', 'ceta',
    # Corporate
    'sab_foundation',
    # International
    'aecf', 'tef'
]
