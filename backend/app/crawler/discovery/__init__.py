"""Discovery adapters. Adding a site means adding one small adapter/parser."""

from app.crawler.discovery.base import CrawlContext, DiscoveredItem, RobotsDisallowed, discover

__all__ = ["CrawlContext", "DiscoveredItem", "RobotsDisallowed", "discover"]
