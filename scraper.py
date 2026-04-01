import os
import asyncio
from crawl4ai import AsyncWebCrawler
import google.generativeai as genai

# Setup Gemini
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

async def main():
    # 1. Target URL (Update this to your preferred job board)
    target_url = "https://news.ycombinator.com/jobs" 

    async with AsyncWebCrawler() as crawler:
        # 2. Scrape the page
        result = await crawler.arun(url=target_url)
        
        # 3. Use AI to extract and clean the data
        prompt = f"""
        Extract all job listings from the following text. 
        Focus on: Role Title, Company, and Link.
        Ignore anything that isn't a job posting.
        Format as a clean Markdown table.
        
        TEXT:
        {result.markdown[:5000]} 
        """
        
        response = model.generate_content(prompt)
        
        # 4. Save to a file for GitHub Actions to read
        with open("jobs_found.md", "w") as f:
            f.write(response.text)

if __name__ == "__main__":
    asyncio.run(main())
