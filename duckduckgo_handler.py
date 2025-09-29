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


def search_web(query, max_results=2):
    """
    Search DuckDuckGo and return short, readable summaries.
    
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
            results = list(ddgs.text(query, max_results=max_results))
            
            if not results:
                return "I couldn't find anything for that."

            # Extract short snippets
            clean_results = []
            for r in results:
                snippet = r.get("body", "")
                if len(snippet.split()) > 30:  # shorten long snippets
                    snippet = " ".join(snippet.split()[:30]) + "..."
                clean_results.append(snippet)

            # Combine top results
            combined_result = " ".join(clean_results)
            
        if not combined_result:
            return None
            
        # Clean the result text
        cleaned_result = clean_text(combined_result)
        
        return cleaned_result.strip()
        
    except Exception as e:
        print(f"Web search error: {e}")
        return "Something went wrong during live search."