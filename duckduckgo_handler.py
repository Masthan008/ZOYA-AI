"""
Handles web search functionality using DuckDuckGo for Zoya AI Assistant
"""

from utils import clean_text

# Try to import DDGS
try:
    from duckduckgo_search import DDGS
    DDGS_AVAILABLE = True
except ImportError:
    print("Warning: duckduckgo-search not available. Web search will be disabled.")
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
        ddgs = DDGS()
        results = ddgs.text(query, max_results=max_results)
        
        if not results:
            return None
            
        # Combine the top results
        combined_result = ""
        for result in results:
            if 'body' in result:
                combined_result += result['body'] + " "
                
        # Clean the result text
        cleaned_result = clean_text(combined_result)
        
        return cleaned_result.strip()
        
    except Exception as e:
        print(f"Web search error: {e}")
        return None