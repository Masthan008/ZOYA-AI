"""
Handles web search functionality using DuckDuckGo for Zoya AI Assistant
"""

from utils import clean_text

# Try to import DDGS from ddgs
try:
    from ddgs import DDGS
    DDGS_AVAILABLE = True
except ImportError:
    print("Warning: ddgs not available. Web search will be disabled.")
    DDGS_AVAILABLE = False


def search_web(query, max_results=3):
    """
    Search the web using DuckDuckGo and return summarized results
    
    Args:
        query (str): Search query
        max_results (int): Maximum number of results to return
        
    Returns:
        str: Summarized search results or None if failed
    """
    if not DDGS_AVAILABLE:
        return None
        
    try:
        with DDGS() as ddgs:
            results = [r["body"] for r in ddgs.text(query, max_results=max_results)]
            combined_result = "\n".join(results) if results else ""
            
        if not combined_result:
            return None
            
        # Clean the result text
        cleaned_result = clean_text(combined_result)
        
        return cleaned_result.strip()
        
    except Exception as e:
        print(f"Web search error: {e}")
        return None