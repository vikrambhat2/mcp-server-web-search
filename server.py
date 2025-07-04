import os
import requests
from typing import List, Set, Union
from dotenv import load_dotenv
from pydantic import BaseModel, HttpUrl
from typing import Dict, Any
from fastmcp import FastMCP
from bs4 import BeautifulSoup
import logging


# Load environment variables
load_dotenv()
PORT = os.environ.get("PORT",10000)
# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

try:
    mcp = FastMCP("Web Extraction Tools", host="0.0.0.0", port=PORT)
except Exception as e:
    logging.error(f"Failed to initialize FastMCP: {e}")
    raise


@mcp.tool()
def extract_text_from_url(input: Union[str, HttpUrl]) -> Dict[str, Any]:
    """
    Extracts text content from the given webpage URL. Filters out non-visible elements like <script>, <style>, and <noscript> tags. 
     Returns the cleaned text.
    Args:
        input (Union[str, HttpUrl]): The URL of the webpage to scrape.
    
    Returns:
        Dict[str, Any]: The response containing the cleaned text .
    """
    url = input if isinstance(input, str) else input.url
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    visible_text = soup.get_text(separator="\n", strip=True)
    visible_text = "\n".join(line for line in visible_text.splitlines() if line.strip())
    return_dict = {"response":visible_text}
    return return_dict


if __name__ == "__main__":
    try:
        logging.info("Launching Web Extraction MCP server...")
        
        mcp.run("streamable-http")
    except Exception as e:
        logging.error(f"Failed to run MCP server: {e}")
        raise
